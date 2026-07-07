import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976D2',
      light: '#42a5f5',
      dark: '#0d47a1',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#e91e63',
      light: '#f06292',
      dark: '#c2185b',
      contrastText: '#ffffff',
    },
    background: {
      default: '#f5f7fa',
      paper: '#ffffff',
    },
    success: { main: '#4caf50' },
    warning: { main: '#ff9800' },
    error: { main: '#f44336' },
    info: { main: '#2196f3' },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: { fontWeight: 700, fontSize: '2.5rem' },
    h2: { fontWeight: 700, fontSize: '2rem' },
    h3: { fontWeight: 600, fontSize: '1.75rem' },
    h4: { fontWeight: 600, fontSize: '1.5rem' },
    h5: { fontWeight: 600, fontSize: '1.25rem' },
    h6: { fontWeight: 600, fontSize: '1rem' },
    button: { textTransform: 'none', fontWeight: 600 },
  },
  shape: { borderRadius: 12 },
  
  // ============================================
  // ACCESSIBILITY: Minimum touch targets
  // ============================================
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          minHeight: 44,  // ✅ Minimum touch target size
          minWidth: 44,
          borderRadius: 8,
          fontWeight: 600,
          '&:focus-visible': {
            outline: '3px solid #1976D2',
            outlineOffset: '2px',
          },
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          minHeight: 44,  // ✅ Minimum touch target size
          minWidth: 44,
          '&:focus-visible': {
            outline: '3px solid #1976D2',
            outlineOffset: '2px',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiInputLabel-root': { fontWeight: 500 },
          '& .MuiOutlinedInput-root': {
            '& fieldset': { borderWidth: 2 },  // ✅ Better visibility
            '&:focus-within fieldset': { borderColor: '#1976D2' },
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          '&:focus-visible': {
            outline: '3px solid #1976D2',
            outlineOffset: '2px',
          },
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          borderRadius: 16,
        },
      },
    },
  },
});

export default theme;