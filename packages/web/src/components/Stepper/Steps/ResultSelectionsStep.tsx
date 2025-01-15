import React, { useState } from 'react';
import { Box, Typography, Paper, Chip, Button, TextField, Alert } from '@mui/material';
import { useAnalysis } from '../../../context/AnalysisContext';
import { MetadataFields } from '../../Metadata/MetadataFields';
import { ApiService } from '../../../services/api';

interface ResultSelectionsStepProps {
  onNext: (email: string) => void;
  onBack: () => void;
  trackName: string;
  artistName: string;
  onTrackNameChange: (value: string) => void;
  onArtistNameChange: (value: string) => void;
  onSave: () => void;
  metadataSaved: boolean;
}

export const ResultSelectionsStep: React.FC<ResultSelectionsStepProps> = ({
  onNext,
  onBack,
  ...metadataProps
}) => {
  const { state } = useAnalysis();
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState('');

  // Get selected items
  const selectedGenres = Array.from(state.selections.genres)
    .map(id => state.results?.genres.find(g => g.id === id))
    .filter(g => g !== undefined);

  const selectedMoods = Array.from(state.selections.moods)
    .map(id => state.results?.moodThemes.find(m => m.id === id))
    .filter(m => m !== undefined);

  const selectedTags = Array.from(state.selections.tags)
    .map(id => state.results?.tags.find(t => t.id === id))
    .filter(t => t !== undefined);

  const validateEmail = (email: string) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const handleContinue = async () => {
    if (!validateEmail(email)) {
      setEmailError('Please enter a valid email address');
      return;
    }

    try {
      // Send verification email with user data
      const response = await ApiService.sendVerificationEmail({
        email,
        trackName: state.metadata.trackName,
        artistName: state.metadata.artistName,
        selections: {
          genres: Array.from(state.selections.genres),
          moods: Array.from(state.selections.moods),
          tags: Array.from(state.selections.tags)
        }
      });

      if (response.success) {
        setEmailError('');
        onNext(email);
      } else {
        setEmailError(response.error || 'Failed to send verification email');
      }
    } catch (err) {
      setEmailError(err.message || 'Failed to send verification email');
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
      <Typography variant="h4" component="h1" sx={{ mb: 4, fontWeight: 500 }}>
        Selected Results
      </Typography>

      <MetadataFields {...metadataProps} />

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        {/* Selected Genres */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Selected Genres
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {selectedGenres.map((genre) => (
              <Chip
                key={genre.id}
                label={`${genre.name} (${Math.round(genre.confidence * 100)}%)`}
                color="success"
                variant="filled"
              />
            ))}
          </Box>
        </Paper>

        {/* Selected Moods & Themes */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Selected Moods & Themes
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {selectedMoods.map((mood) => (
              <Chip
                key={mood.id}
                label={`${mood.name} (${Math.round(mood.confidence * 100)}%)`}
                color="info"
                variant="filled"
              />
            ))}
          </Box>
        </Paper>

        {/* Selected Tags */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Selected Tags
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {selectedTags.map((tag) => (
              <Chip
                key={tag.id}
                label={`${tag.name} (${Math.round(tag.confidence * 100)}%)`}
                color="secondary"
                variant="filled"
              />
            ))}
          </Box>
        </Paper>
      </Box>

      {/* Add Email Registration Section */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Generate Your Market Report
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Enter your email to save your selections and continue to your interactive market report.
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-start' }}>
          <TextField
            fullWidth
            label="Email Address"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setEmailError('');
            }}
            error={!!emailError}
            helperText={emailError}
            sx={{ maxWidth: 400 }}
          />
        </Box>
      </Paper>

      <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <Button onClick={onBack} variant="outlined">
          Back
        </Button>
        <Button 
          onClick={handleContinue} 
          variant="contained"
          disabled={
            (selectedGenres.length === 0 && 
            selectedMoods.length === 0 && 
            selectedTags.length === 0) ||
            !email.trim()
          }
        >
          Continue to Market Report
        </Button>
      </Box>

      {/* Add selection requirement message if needed */}
      {selectedGenres.length === 0 && 
       selectedMoods.length === 0 && 
       selectedTags.length === 0 && (
        <Alert severity="info" sx={{ mt: 2 }}>
          Please select at least one genre, mood, or tag to continue.
        </Alert>
      )}
    </Box>
  );
}; 