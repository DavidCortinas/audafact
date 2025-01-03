import React from 'react';
import { Box, Typography, Chip, Button, Paper } from '@mui/material';
import { useAnalysis } from '../../../context/AnalysisContext';

interface AnalysisStepProps {
  onNext: () => void;
  onBack: () => void;
}

export const AnalysisStep: React.FC<AnalysisStepProps> = ({ onNext, onBack }) => {
  const { state } = useAnalysis();
  console.log('Analysis state:', state);
  console.log('Analysis results:', state.results);
  
  // Extract and transform genres
  const genres = state.results?.genres || [];
  const flattenedGenres = genres.map(genre => ({
    name: genre.name,
    confidence: genre.confidence
  }));
  console.log(genres);
  console.log(flattenedGenres);

  // Extract and transform mood themes
  const moodThemes = state.results?.moodThemes || [];
  const allMoodThemes = moodThemes.map(theme => ({
    name: theme.name,
    confidence: theme.confidence
  }));
  console.log(moodThemes);
  console.log(allMoodThemes);

  // Extract and transform tags
  const tags = state.results?.tags || [];
  const allTags = tags.map(tag => ({
    name: tag.name,
    confidence: tag.confidence
  }));
  console.log(tags);
  console.log(allTags);

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
      <Typography variant="h4" component="h1" sx={{ mb: 4, fontWeight: 500 }}>
        Analysis Results
      </Typography>

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        {/* Genres Section */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Genres
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {flattenedGenres
              .sort((a, b) => b.confidence - a.confidence)
              .map((genre, index) => (
                <Chip
                  key={index}
                  label={`${genre.name} (${Math.round(genre.confidence * 100)}%)`}
                  color="success"
                  variant="outlined"
                />
              ))}
          </Box>
        </Paper>

        {/* Moods & Themes Section */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Moods & Themes
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {moodThemes
              .sort((a, b) => b.confidence - a.confidence)
              .map((mood, index) => (
                <Chip
                  key={index}
                  label={`${mood.name} (${Math.round(mood.confidence * 100)}%)`}
                  color="info"
                  variant="outlined"
                />
              ))}
          </Box>
        </Paper>

        {/* Tags Section */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Tags
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {tags
              .sort((a, b) => b.confidence - a.confidence)
              .map((tag, index) => (
                <Chip
                  key={index}
                  label={`${tag.name} (${Math.round(tag.confidence * 100)}%)`}
                  color="secondary"
                  variant="outlined"
                />
              ))}
          </Box>
        </Paper>
      </Box>

      <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <Button onClick={onBack} variant="outlined">
          Back
        </Button>
        <Button onClick={onNext} variant="contained">
          Continue
        </Button>
      </Box>
    </Box>
  );
};
