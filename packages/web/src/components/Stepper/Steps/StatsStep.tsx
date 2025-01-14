import React from 'react';
import { Box, Button, Typography, Paper } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import { StatsStepProps } from '../../../types/components';

export const StatsStep: React.FC<StatsStepProps> = ({ onBack, results }) => {
  const handleDownloadReport = () => {
    // TODO: Implement report download
    console.log('Downloading report...');
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 600, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Spotify Statistics
      </Typography>
      
      {results.map((result) => (
        <Paper key={result.genre} sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            {result.genre.charAt(0).toUpperCase() + result.genre.slice(1)}
          </Typography>
          <Typography>
            Playlists found: {result.playlists.total}
          </Typography>
          <Typography>
            Artists found: {result.artists.total >= 100 ? '100+' : result.artists.total}
          </Typography>
        </Paper>
      ))}

      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={onBack} variant="outlined">
          Back
        </Button>
        <Button
          onClick={handleDownloadReport}
          variant="contained"
          startIcon={<DownloadIcon />}
        >
          Download Full Report
        </Button>
      </Box>
    </Box>
  );
}; 