import type { 
  Genre, 
  MoodTheme, 
  Tag, 
  AnalysisResponse 
} from '../types/api';

export const transformGenre = (data: any): Genre => ({
  id: data.id || String(Math.random()),
  name: data.name?.toLowerCase() || '',
  confidence: Number(data.confidence) || 0
});

export const transformMoodTheme = (data: any): MoodTheme => ({
  id: data.id || String(Math.random()),
  name: data.name?.toLowerCase() || '',
  confidence: Number(data.confidence) || 0,
  category: data.category?.toLowerCase() === 'mood' ? 'mood' : 'theme'
});

export const transformTag = (data: any): Tag => ({
  id: data.id || String(Math.random()),
  name: data.name?.toLowerCase() || '',
  confidence: Number(data.confidence) || 0,
  category: data.category?.toLowerCase() || 'general'
});

export const transformAnalysisResponse = (data: any): AnalysisResponse => ({
  success: Boolean(data.success),
  genres: Array.isArray(data.genres) ? data.genres.map(transformGenre) : [],
  moodThemes: Array.isArray(data.moodThemes) ? data.moodThemes.map(transformMoodTheme) : [],
  tags: Array.isArray(data.tags) ? data.tags.map(transformTag) : []
});
