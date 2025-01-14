import React from 'react';
import { Box, Typography, Paper, Chip, Button } from '@mui/material';
import { useAnalysis } from '../../../context/AnalysisContext';
import { MetadataFields } from '../../Metadata/MetadataFields';

interface ResultSelectionsStepProps {
  onNext: () => void;
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

      <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <Button onClick={onBack} variant="outlined">
          Back
        </Button>
        <Button 
          onClick={onNext} 
          variant="contained"
          disabled={selectedGenres.length === 0 && selectedMoods.length === 0 && selectedTags.length === 0}
        >
          Continue
        </Button>
      </Box>
    </Box>
  );
}; 