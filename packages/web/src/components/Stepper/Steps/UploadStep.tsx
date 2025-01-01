import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Box, Typography, Button, TextField, Divider, CircularProgress, LinearProgress } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { ApiService } from '../../../services/api';
import { useAnalysis } from '../../../context/AnalysisContext';
import { transformAnalysisResponse } from '../../../services/transforms';
import { validateAnalysisResponse } from '../../../utils/validation';
import { CheckCircleOutline } from '@mui/icons-material';

const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB
const ACCEPTED_FORMATS = {
  'audio/mpeg': ['.mp3'],
  'audio/wav': ['.wav'],
  'audio/flac': ['.flac'],
  'audio/mp4': ['.mp4', '.m4a'],
  'audio/x-m4a': ['.m4a']
};

interface UploadStepProps {
  onNext: () => void;
}

interface PartialResults {
  genres?: any[];
  moodThemes?: any[];
  tags?: any[];
}

export const UploadStep: React.FC<UploadStepProps> = ({ onNext }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [url, setUrl] = useState('');
  const { dispatch } = useAnalysis();
  const [analysisStep, setAnalysisStep] = useState<'genres' | 'moods' | 'tags' | null>(null);
  const [partialResults, setPartialResults] = useState<PartialResults>({});

  const handleFileUpload = async (file: File) => {
    try {
      setIsLoading(true);
      setError(null);
      setIsAnalyzing(true);
      setPartialResults({});
      setUploadProgress(0); // Reset progress
      
      // Sequential analysis with partial results
      setAnalysisStep('genres');
      setUploadProgress(0); // Reset for genres
      const genres = await ApiService.analyzeGenres(file, (progress) => {
        if (progress.progress < 100) { // Only update if not complete
          setUploadProgress(progress.progress);
        }
      });
      setPartialResults(prev => ({ ...prev, genres }));

      setAnalysisStep('moods');
      setUploadProgress(0); // Reset for moods
      const moodThemes = await ApiService.analyzeMoodThemes(file, (progress) => {
        if (progress.progress < 100) {
          setUploadProgress(progress.progress);
        }
      });
      setPartialResults(prev => ({ ...prev, moodThemes }));

      setAnalysisStep('tags');
      setUploadProgress(0); // Reset for tags
      const tags = await ApiService.analyzeTags(file, (progress) => {
        if (progress.progress < 100) {
          setUploadProgress(progress.progress);
        }
      });
      setPartialResults(prev => ({ ...prev, tags }));

      const result = transformAnalysisResponse({
        success: true,
        genres,
        moodThemes,
        tags
      });

      dispatch({ type: 'ANALYSIS_SUCCESS', payload: validateAnalysisResponse(result) });
      
      setTimeout(() => {
        onNext();
      }, 1000);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err instanceof Error ? err.message : 'Failed to upload file');
    } finally {
      setIsLoading(false);
      setIsAnalyzing(false);
      setUploadProgress(0);
      setAnalysisStep(null);
    }
  };

  const handleUrlSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    try {
      setIsLoading(true);
      setError(null);
      setIsAnalyzing(true);
      setPartialResults({});

      setAnalysisStep('genres');
      const genres = await ApiService.analyzeGenresUrl(url);
      setPartialResults(prev => ({ ...prev, genres }));

      setAnalysisStep('moods');
      const moodThemes = await ApiService.analyzeMoodThemesUrl(url);
      setPartialResults(prev => ({ ...prev, moodThemes }));

      setAnalysisStep('tags');
      const tags = await ApiService.analyzeTagsUrl(url);
      setPartialResults(prev => ({ ...prev, tags }));

      const result = transformAnalysisResponse({
        success: true,
        genres,
        moodThemes,
        tags
      });

      dispatch({ type: 'ANALYSIS_SUCCESS', payload: validateAnalysisResponse(result) });
      onNext();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze URL');
    } finally {
      setIsLoading(false);
      setIsAnalyzing(false);
      setAnalysisStep(null);
    }
  };

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      await handleFileUpload(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    accept: ACCEPTED_FORMATS,
    maxSize: MAX_FILE_SIZE,
    multiple: false,
    noClick: true,
    onDropRejected: (rejectedFiles) => {
      const error = rejectedFiles[0]?.errors[0];
      if (error) {
        switch (error.code) {
          case 'file-invalid-type':
            setError('Invalid file type. Please upload an audio file (MP3, WAV, FLAC, MP4, M4A)');
            break;
          case 'file-too-large':
            setError(`File is too large. Maximum size is ${MAX_FILE_SIZE / 1024 / 1024}MB`);
            break;
          default:
            setError('Error uploading file. Please try again.');
        }
      }
    }
  });

  const getAnalysisMessage = () => {
    return (
      <Box sx={{ mt: 2 }}>
        <Typography sx={{ color: 'text.secondary', mb: 2 }}>
          {analysisStep === 'genres' && 'Analyzing genres...'}
          {analysisStep === 'moods' && 'Analyzing moods and themes...'}
          {analysisStep === 'tags' && 'Analyzing tags...'}
        </Typography>

        {partialResults.genres && (
          <Typography 
            sx={{ 
              color: 'success.main',
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              mb: 1 
            }}
          >
            <CheckCircleOutline fontSize="small" />
            Found {partialResults.genres.length} genres
          </Typography>
        )}

        {partialResults.moodThemes && (
          <Typography 
            sx={{ 
              color: 'success.main',
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              mb: 1 
            }}
          >
            <CheckCircleOutline fontSize="small" />
            Found {partialResults.moodThemes.length} moods/themes
          </Typography>
        )}

        {partialResults.tags && (
          <Typography 
            sx={{ 
              color: 'success.main',
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              mb: 1 
            }}
          >
            <CheckCircleOutline fontSize="small" />
            Found {partialResults.tags.length} tags
          </Typography>
        )}

        {(isAnalyzing && uploadProgress < 100) && (
          <Box sx={{ width: '100%', mt: 2 }}>
            <LinearProgress 
              variant="indeterminate"
            />
            <Typography variant="body2" sx={{ mt: 1, color: 'text.secondary' }}>
              {analysisStep === 'genres' && 'Analyzing audio for genres...'}
              {analysisStep === 'moods' && 'Analyzing audio for moods and themes...'}
              {analysisStep === 'tags' && 'Analyzing audio for tags...'}
            </Typography>
          </Box>
        )}
      </Box>
    );
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 3,
        maxWidth: '800px',
        margin: '0 auto',
        mt: 4,
      }}
    >
      <Typography variant="h4" component="h1" sx={{ fontWeight: 500 }}>
        Upload Your Track
      </Typography>

      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}

      {isAnalyzing && getAnalysisMessage()}

      {!isAnalyzing && (
        <>
          <Box
            {...getRootProps()}
            sx={{
              width: '100%',
              border: '1px dashed',
              borderColor: error ? 'error.main' : 'text.secondary',
              borderRadius: 1,
              p: 6,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 2,
              cursor: 'pointer',
              backgroundColor: isDragActive ? 'rgba(255, 255, 255, 0.04)' : 'transparent',
              '&:hover': {
                borderColor: theme => theme.palette.mode === 'dark' ? '#ffffff' : 'primary.main',
                backgroundColor: 'rgba(255, 255, 255, 0.04)',
              },
            }}
          >
            <input {...getInputProps()} />
            <CloudUploadIcon sx={{ fontSize: 48, color: 'text.secondary' }} />
            <Typography>
              {isDragActive ? 'Drop your audio file here' : 'Drag and drop your audio file here'}
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              Supports {Object.values(ACCEPTED_FORMATS).flat()
                .map(ext => ext.replace('.', '').toUpperCase()).join(', ')} 
              (max {MAX_FILE_SIZE / 1024 / 1024}MB)
            </Typography>
            <Button
              variant="contained"
              component="span"
              onClick={(e) => {
                e.stopPropagation();
                open();
              }}
              disabled={isLoading || isAnalyzing}
              sx={{ mt: 2 }}
            >
              {isLoading ? <CircularProgress size={24} /> : 'Choose File'}
            </Button>
          </Box>

          <Divider sx={{ my: 3 }}>OR</Divider>

          <Box component="form" onSubmit={handleUrlSubmit} sx={{ display: 'flex', gap: 2, width: '100%' }}>
            <TextField
              fullWidth
              placeholder="Paste streaming URL"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={isLoading || isAnalyzing}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={isLoading || isAnalyzing || !url.trim()}
            >
              {isLoading || isAnalyzing ? (
                <CircularProgress size={24} />
              ) : (
                'Analyze'
              )}
            </Button>
          </Box>
        </>
      )}
    </Box>
  );
};