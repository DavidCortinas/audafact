import { useState, useMemo, createContext } from 'react';
import type { AppProps } from 'next/app';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { createAppTheme } from '../src/theme';
import { Box, IconButton } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { AnalysisProvider } from '../src/context/AnalysisContext';

// Create a context for theme mode
export const ColorModeContext = createContext({ 
  toggleColorMode: () => {} 
});

function MyApp({ Component, pageProps }: AppProps) {
  const [mode, setMode] = useState<'light' | 'dark'>('dark');
  
  const colorMode = useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
      },
    }),
    []
  );

  const theme = useMemo(() => createAppTheme(mode), [mode]);

  return (
    <AnalysisProvider>
      <ColorModeContext.Provider value={colorMode}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Box
            sx={{
              position: 'fixed',
              top: 16,
              right: 16,
              zIndex: 1000,
            }}
          >
            <IconButton 
              onClick={colorMode.toggleColorMode} 
              color="inherit"
              sx={{
                bgcolor: 'background.paper',
                '&:hover': {
                  bgcolor: 'background.paper',
                  opacity: 0.9,
                },
              }}
            >
              {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
            </IconButton>
          </Box>
          <Component {...pageProps} />
        </ThemeProvider>
      </ColorModeContext.Provider>
    </AnalysisProvider>
  );
}

export default MyApp; 