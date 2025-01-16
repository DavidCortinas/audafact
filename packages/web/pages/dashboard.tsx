import { Dashboard } from '../src/components/Dashboard';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { CircularProgress, Box } from '@mui/material';

export default function DashboardPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if we're in the browser
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('authToken');
      if (!token) {
        router.push('/');
      } else {
        setIsLoading(false);
      }
    }
  }, [router]);

  if (isLoading) {
    return (
      <Box 
        sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          minHeight: '100vh' 
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return <Dashboard />;
} 