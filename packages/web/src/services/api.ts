import axios, {
  AxiosRequestConfig,
  AxiosResponse,
  AxiosInstance,
  AxiosError,
} from "axios";
import {
  ApiResponse,
  GenreAnalysisResponse,
  MoodThemeAnalysisResponse,
  TagAnalysisResponse,
  AnalysisResponse,
  ApiError,
  UploadProgress,
} from "../types/api";
import { withRetry } from "../utils/retry";
import { validateAnalysisResponse } from "../utils/validation";
import { transformAnalysisResponse } from "./transforms";
import { TokenService } from "./token";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  timeout: 120000,
  headers: {
    "Content-Type": "application/json",
  },
});

interface RawAnalysisResponse {
  genres: any[];
  moodThemes: any[];
  tags: any[];
}

interface VerificationResponse {
  success: boolean;
  message?: string;
  error?: string;
}

interface SendVerificationRequest {
  email: string;
  trackName?: string;
  artistName?: string;
  selections?: {
    genres: string[];
    moods: string[];
    tags: string[];
  };
}

export class ApiService {
  private static instance: AxiosInstance;
  private static isRefreshing = false;
  private static refreshSubscribers: ((token: string) => void)[] = [];

  private static getInstance(): AxiosInstance {
    if (!this.instance) {
      this.instance = axios.create({
        baseURL: process.env.NEXT_PUBLIC_API_URL,
        headers: {
          "Content-Type": "application/json",
        },
      });

      // Add request interceptor
      this.instance.interceptors.request.use(
        (config) => {
          const token = TokenService.getAccessToken();
          if (token) {
            config.headers.Authorization = `Bearer ${token}`;
          }
          return config;
        },
        (error) => Promise.reject(error)
      );

      // Add response interceptor
      this.instance.interceptors.response.use(
        (response) => response,
        async (error: AxiosError) => {
          const originalRequest = error.config;

          if (error.response?.status === 401 && !originalRequest._retry) {
            if (this.isRefreshing) {
              // Wait for the token to be refreshed
              try {
                const token = await new Promise<string>((resolve) => {
                  this.refreshSubscribers.push((token: string) => {
                    resolve(token);
                  });
                });
                originalRequest.headers.Authorization = `Bearer ${token}`;
                return this.instance(originalRequest);
              } catch (err) {
                return Promise.reject(err);
              }
            }

            originalRequest._retry = true;
            this.isRefreshing = true;

            try {
              const refreshToken = TokenService.getRefreshToken();
              if (!refreshToken) {
                throw new Error("No refresh token available");
              }

              const response = await this.instance.post("/auth/refresh", {
                refresh_token: refreshToken,
              });

              const { access_token, refresh_token } = response.data;
              TokenService.setTokens({
                access_token,
                refresh_token,
                token_type: "bearer",
              });

              // Notify all subscribers about the new token
              this.refreshSubscribers.forEach((callback) =>
                callback(access_token)
              );
              this.refreshSubscribers = [];

              return this.instance(originalRequest);
            } catch (err) {
              // If refresh fails, log out the user
              TokenService.clearTokens();
              window.location.href = "/";
              return Promise.reject(err);
            } finally {
              this.isRefreshing = false;
            }
          }

          return Promise.reject(error);
        }
      );
    }

    return this.instance;
  }

  static async analyzeGenres(
    file: File,
    onProgress?: (progress: UploadProgress) => void
  ) {
    const formData = new FormData();
    formData.append("file", file);
    const response = await this.uploadFile(
      "/genres/file",
      formData,
      onProgress
    );
    return response.data?.genres || [];
  }

  static async analyzeMoodThemes(
    file: File,
    onProgress?: (progress: UploadProgress) => void
  ) {
    const formData = new FormData();
    formData.append("file", file);
    const response = await this.uploadFile(
      "/mood-themes/file",
      formData,
      onProgress
    );
    return response.data?.mood_themes || [];
  }

  static async analyzeTags(
    file: File,
    onProgress?: (progress: UploadProgress) => void
  ) {
    const formData = new FormData();
    formData.append("file", file);
    const response = await this.uploadFile("/tags/file", formData, onProgress);
    return {
      mtg_jamendo_general: response.data?.mtg_jamendo_general || {},
      mtg_jamendo_track: response.data?.mtg_jamendo_track || {},
    };
  }

  static async analyzeGenresUrl(url: string) {
    const response = await api.get("/genres/url", { params: { url } });
    return response.data?.genres || [];
  }

  static async analyzeMoodThemesUrl(url: string) {
    const response = await api.get("/mood-themes/url", { params: { url } });
    return response.data?.mood_themes || [];
  }

  static async analyzeTagsUrl(url: string) {
    const response = await api.get("/tags/url", { params: { url } });
    return response.data?.predictions || [];
  }

  static async analyzeFile(
    file: File,
    onProgress?: (progress: UploadProgress) => void
  ): Promise<AnalysisResponse> {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const result = await withRetry(async () => {
        const [genresRes, moodThemesRes, tagsRes] = await Promise.all([
          this.uploadFile("/genres/file", formData, onProgress),
          this.uploadFile("/mood-themes/file", formData, onProgress),
          this.uploadFile("/tags/file", formData, onProgress),
        ]);

        return {
          genres: genresRes.data || [],
          moodThemes: moodThemesRes.data || [],
          tags: tagsRes.data || [],
        };
      });

      const transformedResponse = transformAnalysisResponse({
        success: true,
        ...result,
      });

      return validateAnalysisResponse(transformedResponse);
    } catch (error) {
      throw this.handleError(error);
    }
  }

  static async analyzeFileQuick(
    file: File,
    onProgress?: (progress: UploadProgress) => void
  ): Promise<AnalysisResponse> {
    try {
      // Sequential analysis
      const genres = await this.analyzeGenres(file, onProgress);
      const moodThemes = await this.analyzeMoodThemes(file, onProgress);
      const tags = await this.analyzeTags(file, onProgress);

      const result = {
        genres,
        moodThemes,
        tags,
      };

      const transformedResponse = transformAnalysisResponse({
        success: true,
        ...result,
      });

      return validateAnalysisResponse(transformedResponse);
    } catch (error) {
      throw this.handleError(error);
    }
  }

  static async analyzeUrl(url: string): Promise<AnalysisResponse> {
    try {
      const result = await withRetry(async () => {
        const [genresRes, moodThemesRes, tagsRes] = await Promise.all([
          api.get("/genres/url", { params: { url } }),
          api.get("/mood-themes/url", { params: { url } }),
          api.get("/tags/url", { params: { url } }),
        ]);

        return {
          genres: genresRes.data || [],
          moodThemes: moodThemesRes.data || [],
          tags: tagsRes.data || [],
        };
      });

      const transformedResponse = transformAnalysisResponse({
        success: true,
        ...result,
      });

      return validateAnalysisResponse(transformedResponse);
    } catch (error) {
      throw this.handleError(error);
    }
  }

  static async analyzeUrlQuick(url: string): Promise<AnalysisResponse> {
    try {
      // Sequential analysis
      const genres = await this.analyzeGenresUrl(url);
      const moodThemes = await this.analyzeMoodThemesUrl(url);
      const tags = await this.analyzeTagsUrl(url);

      const result = {
        genres,
        moodThemes,
        tags,
      };

      const transformedResponse = transformAnalysisResponse({
        success: true,
        ...result,
      });

      return validateAnalysisResponse(transformedResponse);
    } catch (error) {
      throw this.handleError(error);
    }
  }

  static async searchSpotify(genres: string[] | string) {
    // Ensure genres is always an array
    const genreArray = Array.isArray(genres) ? genres : [genres];

    const results = await Promise.all(
      genreArray.map(async (genre) => {
        const params = new URLSearchParams();
        params.append("genres", genre);
        params.append("types", "artist");
        params.append("types", "playlist");
        params.append("limit", "50");

        const response = await api.get(`/spotify/search?${params.toString()}`);
        return response.data.results[0];
      })
    );
    console.log("search results by genre:", results);

    return results;
  }

  static async verifyCode(
    email: string,
    code: string
  ): Promise<VerificationResponse> {
    try {
      const response = await this.getInstance().post("/auth/verify", {
        email,
        code,
      });

      if (response.data.success) {
        TokenService.setTokens({
          access_token: response.data.access_token,
          refresh_token: response.data.refresh_token,
          token_type: "bearer",
        });
      }

      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  static async resendVerificationCode(
    email: string
  ): Promise<VerificationResponse> {
    try {
      const response = await api.post("/auth/resend-code", {
        email,
      });
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.message || "Failed to resend verification code"
      );
    }
  }

  static async sendVerificationEmail(
    data: SendVerificationRequest
  ): Promise<VerificationResponse> {
    try {
      const response = await api.post("/auth/send-verification", data);
      return response.data;
    } catch (error) {
      throw new Error(
        error.response?.data?.message || "Failed to send verification email"
      );
    }
  }

  private static async uploadFile(
    endpoint: string,
    formData: FormData,
    onProgress?: (progress: UploadProgress) => void
  ) {
    const config: AxiosRequestConfig = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      timeout: 120000,
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress({
            loaded: progressEvent.loaded,
            total: progressEvent.total,
            progress,
          });
        }
      },
    };

    return api.post(endpoint, formData, config);
  }

  private static handleError(error: any) {
    if (error.response) {
      return error.response.data;
    }
    return { success: false, error: error.message };
  }
}
