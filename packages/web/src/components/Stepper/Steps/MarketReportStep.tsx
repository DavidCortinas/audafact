import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  TextField, 
  Button, 
  Alert,
  CircularProgress 
} from '@mui/material';
import { useAnalysis } from '../../../context/AnalysisContext';

interface MarketReportStepProps {
  onBack: () => void;
}

export const MarketReportStep: React.FC<MarketReportStepProps> = ({ onBack }) => {
  const [verificationCode, setVerificationCode] = useState('');
  const [error, setError] = useState('');
  const [isVerifying, setIsVerifying] = useState(false);
  const [isResending, setIsResending] = useState(false);
  const [isVerified, setIsVerified] = useState(false);

  const handleVerifyCode = async () => {
    if (!verificationCode.trim()) {
      setError('Please enter the verification code');
      return;
    }

    setIsVerifying(true);
    setError('');

    try {
      // TODO: Add API call to verify code
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      setIsVerified(true);
    } catch (err) {
      setError('Invalid verification code. Please try again.');
    } finally {
      setIsVerifying(false);
    }
  };

  const handleResendCode = async () => {
    setIsResending(true);
    setError('');

    try {
      // TODO: Add API call to resend verification code
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      setError('A new verification code has been sent to your email');
    } catch (err) {
      setError('Failed to resend verification code. Please try again.');
    } finally {
      setIsResending(false);
    }
  };

  if (isVerified) {
    return (
      <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
        <Typography variant="h4" component="h1" sx={{ mb: 4, fontWeight: 500 }}>
          Market Report
        </Typography>
        {/* TODO: Add market report content here */}
        <Typography>
          Your interactive market report will appear here...
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
      <Typography variant="h4" component="h1" sx={{ mb: 4, fontWeight: 500 }}>
        Verify Your Email
      </Typography>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Enter Verification Code
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          We've sent a verification code to your email address. Enter it below to access your interactive market report.
        </Typography>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 400 }}>
          <TextField
            fullWidth
            label="Verification Code"
            value={verificationCode}
            onChange={(e) => {
              setVerificationCode(e.target.value);
              setError('');
            }}
            error={!!error}
            helperText={error}
            disabled={isVerifying}
          />

          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              onClick={handleVerifyCode}
              disabled={isVerifying || !verificationCode.trim()}
              sx={{ flex: 1 }}
            >
              {isVerifying ? <CircularProgress size={24} /> : 'Verify Code'}
            </Button>
            <Button
              variant="outlined"
              onClick={handleResendCode}
              disabled={isResending}
            >
              {isResending ? <CircularProgress size={24} /> : 'Resend Code'}
            </Button>
          </Box>
        </Box>
      </Paper>

      <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <Button onClick={onBack} variant="outlined">
          Back
        </Button>
      </Box>
    </Box>
  );
}; 