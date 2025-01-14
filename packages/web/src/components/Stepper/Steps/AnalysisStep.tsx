import React, { useState } from 'react';
import { Box, Typography, Chip, Button, Paper } from '@mui/material';
import { useAnalysis } from '../../../context/AnalysisContext';
import { ApiService } from '../../../services/api';
import { MetadataFields } from '../../Metadata/MetadataFields';

interface AnalysisStepProps {
  onNext: () => void;
  onBack: () => void;
  trackName: string;
  artistName: string;
  onTrackNameChange: (value: string) => void;
  onArtistNameChange: (value: string) => void;
  onSave: () => void;
  metadataSaved: boolean;
}

export const AnalysisStep: React.FC<AnalysisStepProps> = ({ 
  onNext, 
  onBack,
  ...metadataProps
}) => {
  const { state, dispatch } = useAnalysis();

  const handleToggle = (id: string, type: 'genres' | 'moods' | 'tags') => {
    const newSelections = new Set(state.selections[type]);
    if (newSelections.has(id)) {
      newSelections.delete(id);
    } else {
      newSelections.add(id);
    }
    
    dispatch({
      type: 'UPDATE_SELECTIONS',
      payload: {
        type,
        selections: newSelections
      }
    });
  };

  // Extract and transform genres
  const genres = state.results?.genres || [];
  const flattenedGenres = genres.map(genre => ({
    id: genre.id || genre.name,
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

  const handleContinue = async () => {
    try {
      const selectedItems = {
        genres: Array.from(state.selections.genres).map(id => 
          flattenedGenres.find(g => g.id === id)?.name || ''
        ),
        moods: Array.from(state.selections.moods).map(id => 
          moodThemes.find(m => m.id === id)?.name || ''
        ),
        tags: Array.from(state.selections.tags).map(id => 
          tags.find(t => t.id === id)?.name || ''
        )
      };
      
      const results = await ApiService.searchSpotify(selectedItems);
      onNext(results);
    } catch (error) {
      console.error('Error searching Spotify:', error);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
      <Typography variant="h4" component="h1" sx={{ mb: 4, fontWeight: 500 }}>
        Analysis Results
      </Typography>

      <MetadataFields
        trackName={metadataProps.trackName}
        artistName={metadataProps.artistName}
        onTrackNameChange={metadataProps.onTrackNameChange}
        onArtistNameChange={metadataProps.onArtistNameChange}
        onSave={metadataProps.onSave}
        metadataSaved={metadataProps.metadataSaved}
      />

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        {/* Genres Section */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Genres
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {flattenedGenres
              .sort((a, b) => b.confidence - a.confidence)
              .map((genre) => (
                <Chip
                  key={genre.id}
                  label={`${genre.name} (${Math.round(genre.confidence * 100)}%)`}
                  onClick={() => handleToggle(genre.id, 'genres')}
                  color="success"
                  variant={state.selections.genres.has(genre.id) ? 'filled' : 'outlined'}
                  sx={{ 
                    cursor: 'pointer',
                    '&:hover': {
                      backgroundColor: theme => 
                        state.selections.genres.has(genre.id) 
                          ? theme.palette.success.light 
                          : theme.palette.action.hover,
                    }
                  }}
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
                  onClick={() => handleToggle(mood.id, 'moods')}
                  color="info"
                  variant={state.selections.moods.has(mood.id) ? 'filled' : 'outlined'}
                  sx={{ cursor: 'pointer' }}
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
                  onClick={() => handleToggle(tag.id, 'tags')}
                  color="secondary"
                  variant={state.selections.tags.has(tag.id) ? 'filled' : 'outlined'}
                  sx={{ cursor: 'pointer' }}
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
          onClick={handleContinue} 
          variant="contained"
          disabled={state.selections.genres.size === 0 && state.selections.moods.size === 0 && state.selections.tags.size === 0}
        >
          Continue
        </Button>
      </Box>
    </Box>
  );
};
