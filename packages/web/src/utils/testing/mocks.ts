import type { AnalysisResponse } from '../../types/api';

export const mockAnalysisResponse: AnalysisResponse = {
  success: true,
  genres: [
    { id: '1', name: 'Rock', confidence: 0.85 },
    { id: '2', name: 'Alternative', confidence: 0.75 }
  ],
  moodThemes: [
    { id: '1', name: 'Energetic', confidence: 0.9, category: 'mood' },
    { id: '2', name: 'Urban', confidence: 0.8, category: 'theme' }
  ],
  tags: [
    { id: '1', name: 'Guitar', confidence: 0.95, category: 'instrument' },
    { id: '2', name: 'Fast', confidence: 0.85, category: 'tempo' }
  ]
};
