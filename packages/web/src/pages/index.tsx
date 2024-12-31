import { Box } from '@mui/material';
import { Stepper } from '../components/Stepper';

export default function Home() {
  return (
    <Box 
      sx={{ 
        minHeight: '100vh',
        backgroundColor: 'background.default',
        padding: '20px',
      }}
    >
      <Box 
        sx={{ 
          maxWidth: '1200px', 
          margin: '0 auto',
        }}
      >
        <Stepper />
      </Box>
    </Box>
  );
}