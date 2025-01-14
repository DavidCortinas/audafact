import React from 'react';
import { Grid, TextField, Button } from '@mui/material';
import { CheckCircleOutline, SaveOutlined } from '@mui/icons-material';

interface MetadataFieldsProps {
  trackName: string;
  artistName: string;
  onTrackNameChange: (value: string) => void;
  onArtistNameChange: (value: string) => void;
  onSave: () => void;
  metadataSaved: boolean;
}

export const MetadataFields: React.FC<MetadataFieldsProps> = ({
  trackName,
  artistName,
  onTrackNameChange,
  onArtistNameChange,
  onSave,
  metadataSaved,
}) => {
  return (
    <Grid 
      container 
      spacing={3} 
      sx={{ mb: 3 }} 
      alignItems="center"
      justifyContent="center"
    >
      <Grid item xs={12} sm={4}>
        <TextField
          fullWidth
          label="Track Name"
          value={trackName}
          onChange={(e) => onTrackNameChange(e.target.value)}
          variant="outlined"
        />
      </Grid>
      <Grid item xs={12} sm={4}>
        <TextField
          fullWidth
          label="Artist Name"
          value={artistName}
          onChange={(e) => onArtistNameChange(e.target.value)}
          variant="outlined"
        />
      </Grid>
      <Grid item xs={12} sm={3}>
        <Button
          variant="contained"
          startIcon={metadataSaved ? <CheckCircleOutline sx={{ fontSize: 20 }} /> : <SaveOutlined sx={{ fontSize: 20 }} />}
          onClick={onSave}
          disabled={!trackName.trim() && !artistName.trim()}
          sx={{ 
            height: '100%',
            minHeight: '56px',
            width: '100%',
            borderRadius: 1,
            textTransform: 'none',
            fontSize: '0.9rem',
            padding: '8px 16px',
            backgroundColor: theme => theme.palette.text.secondary,
            '&:hover': {
              backgroundColor: theme => theme.palette.text.primary,
            },
            '&.Mui-disabled': {
              backgroundColor: theme => `${theme.palette.text.secondary}4D`,
            },
            ...(metadataSaved && {
              backgroundColor: '#4caf50',
              '&:hover': {
                backgroundColor: '#43a047',
              },
            }),
            '& .MuiButton-startIcon': {
              marginRight: 1,
              marginLeft: -0.5,
            },
          }}
        >
          {metadataSaved ? 'Saved!' : 'Save'}
        </Button>
      </Grid>
    </Grid>
  );
}; 