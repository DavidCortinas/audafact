import React, { useState } from 'react';
import { Box, Stepper as MUIStepper, Step, StepLabel } from '@mui/material';
import { StepContent } from './StepContent';
import { SpotifySearchResult } from '../../types/spotify';
import { UploadStep } from './Steps/UploadStep';
import { AnalysisStep } from './Steps/AnalysisStep';
import { useAnalysis } from '../../context/AnalysisContext';
import { ResultSelectionsStep } from './Steps/ResultSelectionsStep';

const steps = [
  'Analyze Audio',
  'Analysis Results',
  'Result Selections',
  'Market Report'
];

export const Stepper = () => {
  const { state, dispatch } = useAnalysis();
  const [activeStep, setActiveStep] = useState(0);
  const [searchResults, setSearchResults] = useState<SpotifySearchResult[]>([]);
  const [metadataSaved, setMetadataSaved] = useState(false);

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

  const handleSaveMetadata = () => {
    if (state.metadata.trackName.trim() || state.metadata.artistName.trim()) {
      // Add API call here if needed
      dispatch({
        type: 'UPDATE_METADATA',
        payload: {
          trackName: state.metadata.trackName,
          artistName: state.metadata.artistName
        }
      });
      setMetadataSaved(true);
      setTimeout(() => setMetadataSaved(false), 2000);
    }
  };

  const handleMetadataChange = (field: 'trackName' | 'artistName', value: string) => {
    dispatch({
      type: 'UPDATE_METADATA',
      payload: {
        ...state.metadata,
        [field]: value
      }
    });
  };

  const metadataProps = {
    trackName: state.metadata.trackName,
    artistName: state.metadata.artistName,
    onTrackNameChange: (value: string) => handleMetadataChange('trackName', value),
    onArtistNameChange: (value: string) => handleMetadataChange('artistName', value),
    onSave: handleSaveMetadata,
    metadataSaved,
  };

  const renderStep = () => {
    switch (activeStep) {
      case 0:
        return <UploadStep onNext={handleNext} {...metadataProps} />;
      case 1:
        return <AnalysisStep onNext={handleNext} onBack={handleBack} {...metadataProps} />;
      case 2:
        return <ResultSelectionsStep onNext={handleNext} onBack={handleBack} {...metadataProps} />;
      case 3:
        return <MarketReportStep onBack={handleBack} {...metadataProps} />;
      default:
        return null;
    }
  };

  return (
    <Box sx={{ width: '100%', padding: 3 }}>
      <MUIStepper activeStep={activeStep} alternativeLabel>
        {steps.map((step, index) => (
          <Step key={step}>
            <StepLabel>{step}</StepLabel>
          </Step>
        ))}
      </MUIStepper>
      
      <Box sx={{ mt: 4 }}>
        {renderStep()}
      </Box>
    </Box>
  );
};