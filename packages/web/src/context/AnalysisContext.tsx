import React, { createContext, useContext, useReducer } from 'react';
import type { AnalysisResponse } from '../types/api';

interface AnalysisState {
  results: AnalysisResponse | null;
  loading: boolean;
  error: Error | null;
}

type AnalysisAction = 
  | { type: 'START_ANALYSIS' }
  | { type: 'ANALYSIS_SUCCESS'; payload: AnalysisResponse }
  | { type: 'ANALYSIS_ERROR'; payload: Error }
  | { type: 'RESET_ANALYSIS' };

const analysisReducer = (state: AnalysisState, action: AnalysisAction): AnalysisState => {
  switch (action.type) {
    case 'START_ANALYSIS':
      return {
        ...state,
        loading: true,
        error: null
      };
    
    case 'ANALYSIS_SUCCESS':
      return {
        results: action.payload,
        loading: false,
        error: null
      };
    
    case 'ANALYSIS_ERROR':
      return {
        ...state,
        loading: false,
        error: action.payload
      };
    
    case 'RESET_ANALYSIS':
      return {
        results: null,
        loading: false,
        error: null
      };
    
    default:
      return state;
  }
};

const AnalysisContext = createContext<{
  state: AnalysisState;
  dispatch: React.Dispatch<AnalysisAction>;
} | undefined>(undefined);

const initialState: AnalysisState = {
  results: null,
  loading: false,
  error: null
};

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
