import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
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

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  timeout: 120000,
  headers: {
    "Content-Type": "application/json",
  }
});

interface RawAnalysisResponse {
  genres: any[];
  moodThemes: any[];
  tags: any[];
}

export class ApiService {
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
          this.uploadFile("/tags/file", formData, onProgress)
        ]);

        return {
          genres: genresRes.data || [],
          moodThemes: moodThemesRes.data || [],
          tags: tagsRes.data || []
        };
      });

      const transformedResponse = transformAnalysisResponse({
        success: true,
        ...result
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
      const formData = new FormData();
      formData.append("file", file);

      const result = await withRetry(async () => {
        const [genresRes, moodThemesRes, tagsRes] = await Promise.all([
          this.uploadFile("/genres/file/quick", formData, onProgress),
          this.uploadFile("/mood-themes/file", formData, onProgress),
          this.uploadFile("/tags/file/quick", formData, onProgress)
        ]);

        return {
          genres: genresRes.data?.genres || [],
          moodThemes: moodThemesRes.data || [],
          tags: tagsRes.data?.predictions || []
        };
      });

      const transformedResponse = transformAnalysisResponse({
        success: true,
        ...result
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
          api.get("/tags/url", { params: { url } })
        ]);

        return {
          genres: genresRes.data || [],
          moodThemes: moodThemesRes.data || [],
          tags: tagsRes.data || []
        };
      });

      const transformedResponse = transformAnalysisResponse({
        success: true,
        ...result
      });

      return validateAnalysisResponse(transformedResponse);
    } catch (error) {
      throw this.handleError(error);
    }
  }

  static async analyzeUrlQuick(url: string): Promise<AnalysisResponse> {
    try {
      const result = await withRetry(async () => {
        const response = await api.get("/analysis/url/quick", { params: { url } });
        return response.data;
      });

      const transformedResponse = transformAnalysisResponse({
        success: true,
        ...result
      });

      return validateAnalysisResponse(transformedResponse);
    } catch (error) {
      throw this.handleError(error);
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

  private static handleError(error: unknown): ApiError {
    if (axios.isAxiosError(error)) {
      const apiError = new Error(
        error.response?.data?.message || error.message
      ) as ApiError;

      apiError.code = error.code;
      apiError.statusCode = error.response?.status;
      apiError.details = error.response?.data;

      return apiError;
    }

    return new Error("An unexpected error occurred") as ApiError;
  }
}
