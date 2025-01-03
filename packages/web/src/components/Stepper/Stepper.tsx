import React, { useState } from 'react';
import { Box, Stepper as MUIStepper, Step, StepLabel } from '@mui/material';
import { StepContent } from './StepContent';
import { SpotifySearchResult } from '../../types/spotify';

const steps = [
  {
    label: 'Upload Audio',
    description: 'Upload a file or provide a streaming URL'
  },
  {
    label: 'Analysis',
    description: 'View audio analysis results'
  },
  {
    label: 'Genre Selection',
    description: 'Review and select genres'
  },
  {
    label: 'Report',
    description: 'View final analysis report'
  }
];

export const Stepper = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [searchResults, setSearchResults] = useState<SpotifySearchResult[]>([]);

  const handleNext = () => {
    setActiveStep((prevStep) => Math.min(prevStep + 1, steps.length - 1));
  };

  const handleBack = () => {
    setActiveStep((prevStep) => Math.max(prevStep - 1, 0));
  };

  const handleSearchComplete = (results: SpotifySearchResult[]) => {
    console.log('Setting search results:', results);
    setSearchResults(results);
    handleNext();
  };

  return (
    <Box sx={{ width: '100%', padding: 3 }}>
      <MUIStepper activeStep={activeStep} alternativeLabel>
        {steps.map((step, index) => (
          <Step key={step.label}>
            <StepLabel>{step.label}</StepLabel>
          </Step>
        ))}
      </MUIStepper>
      
      <Box sx={{ mt: 4 }}>
        <StepContent 
          step={activeStep}
          onNext={handleNext}
          onBack={handleBack}
          onSearchComplete={handleSearchComplete}
          results={searchResults}
        />
      </Box>
    </Box>
  );
};