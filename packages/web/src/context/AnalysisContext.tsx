import React, { createContext, useContext, useReducer } from 'react';
import type { AnalysisResponse, AnalysisMetadata } from '../types/api';

interface AnalysisState {
  status: 'idle' | 'loading' | 'success' | 'error';
  error: string | null;
  results: AnalysisResponse | null;
  metadata: {
    trackName: string;
    artistName: string;
  };
  selections: {
    genres: Set<string>;
    moods: Set<string>;
    tags: Set<string>;
  };
}

const initialState: AnalysisState = {
  status: 'idle',
  error: null,
  results: null,
  metadata: {
    trackName: '',
    artistName: '',
  },
  selections: {
    genres: new Set(),
    moods: new Set(),
    tags: new Set(),
  },
};

type AnalysisAction =
  | { type: 'ANALYSIS_START' }
  | { type: 'ANALYSIS_SUCCESS'; payload: AnalysisResponse }
  | { type: 'ANALYSIS_ERROR'; payload: string }
  | { type: 'UPDATE_METADATA'; payload: { trackName: string; artistName: string } }
  | { type: 'UPDATE_SELECTIONS'; payload: { type: 'genres' | 'moods' | 'tags'; selections: Set<string> } };

function analysisReducer(state: AnalysisState, action: AnalysisAction): AnalysisState {
  switch (action.type) {
    case 'ANALYSIS_START':
      return { ...state, status: 'loading', error: null };
    case 'ANALYSIS_SUCCESS':
      return { ...state, status: 'success', results: action.payload };
    case 'ANALYSIS_ERROR':
      return { ...state, status: 'error', error: action.payload };
    case 'UPDATE_METADATA':
      return { ...state, metadata: action.payload };
    case 'UPDATE_SELECTIONS':
      return {
        ...state,
        selections: {
          ...state.selections,
          [action.payload.type]: action.payload.selections
        }
      };
    default:
      return state;
  }
}

const AnalysisContext = createContext<{
  state: AnalysisState;
  dispatch: React.Dispatch<AnalysisAction>;
} | undefined>(undefined);

export const AnalysisProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(analysisReducer, initialState);

  return (
    <AnalysisContext.Provider value={{ state, dispatch }}>
      {children}
    </AnalysisContext.Provider>
  );
};

export const useAnalysis = () => {
  const context = useContext(AnalysisContext);
  if (!context) {
    throw new Error('useAnalysis must be used within an AnalysisProvider');
  }
  return context;
};
