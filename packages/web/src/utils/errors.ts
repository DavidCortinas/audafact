import type { ApiError } from '../types/api';

export const isApiError = (error: unknown): error is ApiError => {
  return error instanceof Error && 'statusCode' in error;
};

export class AnalysisError extends Error implements ApiError {
  code?: string;
  statusCode?: number;
  details?: Record<string, any>;

  constructor(message: string, statusCode?: number, code?: string) {
    super(message);
    this.name = 'AnalysisError';
    this.statusCode = statusCode;
    this.code = code;
  }
}
