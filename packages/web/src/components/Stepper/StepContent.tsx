import React from 'react';
import { UploadStep } from './Steps/UploadStep';
import { AnalysisStep } from './Steps/AnalysisStep';
import { GenreSelectionStep } from './Steps/GenreSelectionStep';
import { ReportStep } from './Steps/ReportStep';
import { StepContentProps } from '../../types/components';

export const StepContent: React.FC<StepContentProps> = ({ 
  step, 
  onNext, 
  onBack,
  onSearchComplete,
  results = [] 
}) => {
  switch (step) {
    case 0:
      return <UploadStep onNext={onNext} />;
    case 1:
      return <AnalysisStep onNext={onNext} onBack={onBack} />;
    case 2:
      return <GenreSelectionStep onNext={onSearchComplete} onBack={onBack} />;
    case 3:
      return <ReportStep onBack={onBack} results={results} />;
    default:
      return null;
  }
};