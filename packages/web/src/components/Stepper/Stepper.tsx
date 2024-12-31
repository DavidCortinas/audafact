import React, { useState } from 'react';
import { Box, Stepper as MUIStepper, Step, StepLabel, Button } from '@mui/material';
import { StepContent } from './StepContent';

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

  const handleNext = () => {
    setActiveStep((prevStep) => Math.min(prevStep + 1, steps.length - 1));
  };

  const handleBack = () => {
    setActiveStep((prevStep) => Math.max(prevStep - 1, 0));
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
        />
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
        <Button
          disabled={activeStep === 0}
          onClick={handleBack}
        >
          Back
        </Button>
        <Button
          variant="contained"
          onClick={handleNext}
          disabled={activeStep === steps.length - 1}
        >
          {activeStep === steps.length - 2 ? 'Finish' : 'Next'}
        </Button>
      </Box>
    </Box>
  );
};