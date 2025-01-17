import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { 
  Box, 
  Typography, 
  Paper, 
  TextField, 
  Button, 
  Alert,
  CircularProgress 
} from '@mui/material';
import { ApiService } from '../../../services/api';

interface MarketReportStepProps {
  onBack: () => void;
  email: string;
}

export const MarketReportStep: React.FC<MarketReportStepProps> = ({ 
  onBack,
  email 
}) => {
  const router = useRouter();
  const [verificationCode, setVerificationCode] = useState('');
  const [error, setError] = useState('');
  const [isVerifying, setIsVerifying] = useState(false);
  const [isResending, setIsResending] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const handleVerifyCode = async () => {
    if (!verificationCode.trim()) {
      setError('Please enter the verification code');
      return;
    }

    setIsVerifying(true);
    setError('');
    setSuccessMessage('');

    try {
      const response = await ApiService.verifyCode(email, verificationCode);
      
      if (response.success) {
        setSuccessMessage('Email verified successfully!');
        // Redirect to dashboard after a brief delay
        setTimeout(() => {
          router.push('/dashboard');
        }, 1500);
      } else {
        setError(response.error || 'Invalid verification code. Please try again.');
      }
    } catch (err) {
      setError(err.message || 'Failed to verify code. Please try again.');
    } finally {
      setIsVerifying(false);
    }
  };

  const handleResendCode = async () => {
    setIsResending(true);
    setError('');
    setSuccessMessage('');

    try {
      const response = await ApiService.resendVerificationCode(email);
      
      if (response.success) {
        setSuccessMessage('A new verification code has been sent to your email');
        setVerificationCode('');
      } else {
        setError(response.error || 'Failed to resend code. Please try again.');
      }
    } catch (err) {
      setError(err.message || 'Failed to resend code. Please try again.');
    } finally {
      setIsResending(false);
    }
  };

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
          We've sent a verification code to <strong>{email}</strong>. Enter it below to access your interactive market report.
        </Typography>

        {successMessage && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {successMessage}
          </Alert>
        )}

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 400 }}>
          <TextField
            fullWidth
            label="Verification Code"
            value={verificationCode}
            onChange={(e) => {
              setVerificationCode(e.target.value);
              setError('');
              setSuccessMessage('');
            }}
            error={!!error}
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