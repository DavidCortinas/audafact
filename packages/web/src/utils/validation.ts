import { z } from 'zod';
import type { 
  Genre, 
  MoodTheme, 
  Tag, 
  AnalysisResponse 
} from '../types/api';

// Validation schemas
export const genreSchema = z.object({
  id: z.string(),
  name: z.string(),
  confidence: z.number().min(0).max(1)
}).strict();

export const moodThemeSchema = z.object({
  id: z.string(),
  name: z.string(),
  confidence: z.number().min(0).max(1),
  category: z.enum(['mood', 'theme'])
}).strict();

export const tagSchema = z.object({
  id: z.string(),
  name: z.string(),
  confidence: z.number().min(0).max(1),
  category: z.string()
}).strict();

export const analysisResponseSchema = z.object({
  success: z.boolean(),
  message: z.string().optional(),
  genres: z.array(genreSchema),
  moodThemes: z.array(moodThemeSchema),
  tags: z.array(tagSchema)
}).strict();

// Validation functions with type assertions
export const validateGenre = (data: unknown): Genre => {
  const validated = genreSchema.parse(data);
  return validated as Genre;
};

export const validateMoodTheme = (data: unknown): MoodTheme => {
  const validated = moodThemeSchema.parse(data);
  return validated as MoodTheme;
};

export const validateTag = (data: unknown): Tag => {
  const validated = tagSchema.parse(data);
  return validated as Tag;
};

export const validateAnalysisResponse = (data: unknown): AnalysisResponse => {
  const validated = analysisResponseSchema.parse(data);
  return validated as AnalysisResponse;
};

// Helper function to validate arrays
export const validateGenreArray = (data: unknown[]): Genre[] => {
  return data.map(item => validateGenre(item));
};

export const validateMoodThemeArray = (data: unknown[]): MoodTheme[] => {
  return data.map(item => validateMoodTheme(item));
};

export const validateTagArray = (data: unknown[]): Tag[] => {
  return data.map(item => validateTag(item));
};
