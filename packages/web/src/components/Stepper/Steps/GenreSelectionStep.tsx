import React, { useState } from 'react';
import { Box, Typography, Button, Chip, Paper } from '@mui/material';
import { useAnalysis } from '../../../context/AnalysisContext';

interface GenreSelectionStepProps {
  onNext: () => void;
  onBack: () => void;
}

export const GenreSelectionStep: React.FC<GenreSelectionStepProps> = ({ onNext, onBack }) => {
  const { state } = useAnalysis();
  const [selectedGenres, setSelectedGenres] = useState<Set<string>>(new Set());
  
  const genres = state.results?.genres || [];
  const sortedGenres = [...genres].sort((a, b) => b.confidence - a.confidence);

  const handleGenreToggle = (genreId: string) => {
    setSelectedGenres(prev => {
      const newSet = new Set(prev);
      if (newSet.has(genreId)) {
        newSet.delete(genreId);
      } else {
        newSet.add(genreId);
      }
      return newSet;
    });
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
      <Typography variant="h4" component="h1" sx={{ mb: 4, fontWeight: 500 }}>
        Select Genres
      </Typography>

      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="body1" sx={{ mb: 2 }}>
          Select the genres that best describe your track. The confidence scores show how strongly each genre was detected.
        </Typography>

        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {sortedGenres.map((genre) => (
            <Chip
              key={genre.id}
              label={`${genre.name} (${Math.round(genre.confidence * 100)}%)`}
              onClick={() => handleGenreToggle(genre.id)}
              color={selectedGenres.has(genre.id) ? 'info' : 'default'}
              variant={selectedGenres.has(genre.id) ? 'filled' : 'outlined'}
              sx={{ 
                cursor: 'pointer',
                '&:hover': {
                  backgroundColor: theme => 
                    selectedGenres.has(genre.id) 
                      ? theme.palette.primary.main 
                      : theme.palette.action.hover,
                }
              }}
            />
          ))}
        </Box>
      </Paper>

      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <Button onClick={onBack} variant="outlined">
          Back
        </Button>
        <Button 
          onClick={onNext} 
          variant="contained"
          disabled={selectedGenres.size === 0}
        >
          Continue
        </Button>
      </Box>
    </Box>
  );
}; 