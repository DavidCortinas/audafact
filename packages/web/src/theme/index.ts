import { createTheme, ThemeOptions } from '@mui/material/styles';

const getDesignTokens = (mode: 'light' | 'dark'): ThemeOptions => ({
  palette: {
    mode,
    ...(mode === 'light'
      ? {
          // Light mode - "Disturbed" theme
          primary: {
            main: '#5c6b8a',      // Waikawa Gray
            light: '#a2b8d2',     // Rock Blue
            dark: '#4a5670',      
          },
          secondary: {
            main: '#f07838',      // Jaffa
            light: '#f5c9a8',     // Maize
            dark: '#ba4c40',      // Crail
          },
          background: {
            default: '#f5f7fa',   
            paper: '#ffffff',     
          },
          text: {
            primary: '#5c6b8a',   // Waikawa Gray
            secondary: '#ba4c40',  // Crail
          },
        }
      : {
          // Dark mode - original dark theme
          primary: {
            main: '#3c3f68',      // Fiord
            light: '#4d4d80',     // East Bay
            dark: '#282c4d',      // Martinique
          },
          background: {
            default: '#1c1f3b',   // Mirage
            paper: '#282c4d',     // Martinique
          },
          text: {
            primary: '#fff',
            secondary: '#ba4c40',  // Crail
          },
        }),
  },
  components: {
    MuiStepper: {
      styleOverrides: {
        root: {
          backgroundColor: 'transparent',
          padding: 0,
          '& .MuiStepConnector-line': {
            borderColor: mode === 'light' ? '#a2b8d2' : '#606271',
          },
        },
      },
    },
    MuiStepLabel: {
      styleOverrides: {
        label: {
          color: mode === 'light' ? '#a2b8d2' : '#606271',
          '&.Mui-active': {
            color: mode === 'light' ? '#f07838' : '#ffffff',
          },
          '&.Mui-completed': {
            color: mode === 'light' ? '#5c6b8a' : '#3c3f68',
          },
        },
      },
    },
    MuiStepIcon: {
      styleOverrides: {
        root: {
          color: mode === 'light' ? '#a2b8d2' : '#606271',
          '&.Mui-active': {
            color: mode === 'light' ? '#f07838' : '#ffffff',
          },
          '&.Mui-completed': {
            color: mode === 'light' ? '#5c6b8a' : '#3c3f68',
          },
        },
        text: {
          fill: mode === 'dark' ? '#1c1f3b' : '#ffffff',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
        contained: {
          backgroundColor: mode === 'light' ? '#5c6b8a' : '#3c3f68',
          '&:hover': {
            backgroundColor: mode === 'light' ? '#4a5670' : '#282c4d',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          ...(mode === 'light' && {
            boxShadow: '0 2px 4px rgba(92, 107, 138, 0.1)',
          }),
        },
      },
    },
  },
});

// Create theme instance
export const theme = createTheme(getDesignTokens('dark')); // Default to dark mode

// Export the theme creator function for dynamic theme switching
export const createAppTheme = (mode: 'light' | 'dark') => createTheme(getDesignTokens(mode));
