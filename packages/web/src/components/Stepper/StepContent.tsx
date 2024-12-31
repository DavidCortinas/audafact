import React from 'react';
import { UploadStep } from './Steps/UploadStep';

interface StepContentProps {
  step: number;
  onNext: () => void;
  onBack: () => void;
}

export const StepContent: React.FC<StepContentProps> = ({ step, onNext, onBack }) => {
  switch (step) {
    case 0:
      return <UploadStep onNext={onNext} />;
    case 1:
      return <div>Analysis Step</div>;
    case 2:
      return <div>Genre Selection Step</div>;
    case 3:
      return <div>Report Step</div>;
    default:
      return null;
  }
};