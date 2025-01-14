// Base response interface
export interface ApiResponse {
  success: boolean;
  message?: string;
}

// Genre related interfaces
export interface Genre {
  id: string;
  name: string;
  confidence: number;
}

export interface GenreAnalysisResponse extends ApiResponse {
  genres: Genre[];
}

// Mood/Theme related interfaces
export interface MoodTheme {
  id: string;
  name: string;
  confidence: number;
  category: "mood" | "theme";
}

export interface MoodThemeAnalysisResponse extends ApiResponse {
  moodThemes: MoodTheme[];
}

// Tag related interfaces
export interface Tag {
  id: string;
  name: string;
  confidence: number;
  category: string;
}

export interface TagAnalysisResponse extends ApiResponse {
  tags: Tag[];
}

export interface AnalysisMetadata {
  trackName: string;
  artistName: string;
}

// Combined analysis response
export interface AnalysisResponse {
  success: boolean;
  message?: string;
  genres: Genre[];
  moodThemes: MoodTheme[];
  tags: Tag[];
  metadata?: AnalysisMetadata;
}

// Audio metadata interface
export interface AudioMetadata {
  duration: number;
  sampleRate: number;
  bitrate: number;
  format: string;
  title?: string;
  artist?: string;
  album?: string;
}

// Upload progress interface
export interface UploadProgress {
  loaded: number;
  total: number;
  progress: number;
}

// Error response interface
export interface ApiError extends Error {
  code?: string;
  statusCode?: number;
  details?: Record<string, any>;
}
