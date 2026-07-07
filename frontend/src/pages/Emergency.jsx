import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Alert,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Warning as WarningIcon } from '@mui/icons-material';
import { announceToScreenReader, setPageTitle } from '../utils/accessibility';

const Emergency = () => {
  const [openDialog, setOpenDialog] = useState(false);
  const [emergencyType, setEmergencyType] = useState('medical');
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const formRef = useRef(null);

  useEffect(() => {
    setPageTitle('Emergency - Report an Emergency');
  }, []);

  const locations = [
    'Gate A', 'Gate B', 'Gate C', 'Gate D', 'Gate E',
    'Section A1', 'Section A2', 'Section B1', 'Section B2',
    'Section C1', 'Section C2',
    'Food Court A', 'Food Court B', 'Food Court C',
    'Restroom 1', 'Restroom 2', 'Restroom 3',
    'First Aid Station', 'Guest Services',
  ];

  const handleSubmit = () => {
    setSubmitted(true);
    announceToScreenReader('Emergency reported successfully. Help is on the way.', 'assertive');
    setTimeout(() => {
      setOpenDialog(false);
      setSubmitted(false);
      setDescription('');
      setLocation('');
      announceToScreenReader('Dialog closed', 'polite');
    }, 3000);
  };

  return (
    <Box 
      component="main"
      role="main"
      aria-label="Emergency reporting page"
    >
      <Typography 
        variant="h4" 
        component="h1" 
        sx={{ mb: 3 }}
        tabIndex={0}
      >
        🚨 Emergency
      </Typography>
      
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Report emergencies and view active alerts
      </Typography>

      <Paper 
        sx={{ p: 3, borderRadius: 3 }}
        role="region"
        aria-label="Emergency reporting form"
      >
        <Button
          variant="contained"
          color="error"
          size="large"
          startIcon={<WarningIcon />}
          onClick={() => {
            setOpenDialog(true);
            announceToScreenReader('Emergency reporting dialog opened', 'polite');
          }}
          sx={{ minHeight: 56 }}
          aria-label="Report an emergency"
        >
          Report Emergency
        </Button>

        <Box sx={{ mt: 3 }}>
          <Alert 
            severity="warning" 
            role="alert"
            aria-live="polite"
          >
            ⚠️ Only use this for real emergencies. False reports are prohibited.
          </Alert>
        </Box>
      </Paper>

      {/* Emergency Dialog */}
      <Dialog 
        open={openDialog} 
        onClose={() => {
          setOpenDialog(false);
          announceToScreenReader('Dialog closed', 'polite');
        }}
        maxWidth="sm" 
        fullWidth
        aria-labelledby="emergency-dialog-title"
      >
        <DialogTitle id="emergency-dialog-title">
          <Box display="flex" alignItems="center" gap={1}>
            <WarningIcon color="error" />
            <Typography variant="h6" component="span" fontWeight={700}>
              Report Emergency
            </Typography>
          </Box>
        </DialogTitle>
        <DialogContent>
          {submitted ? (
            <Alert 
              severity="success" 
              icon={<WarningIcon />}
              role="status"
              aria-live="polite"
            >
              Emergency reported successfully! Help is on the way.
            </Alert>
          ) : (
            <form 
              ref={formRef}
              noValidate
              aria-label="Emergency report form"
            >
              <TextField
                select
                fullWidth
                label="Emergency Type *"
                value={emergencyType}
                onChange={(e) => setEmergencyType(e.target.value)}
                margin="normal"
                required
                aria-required="true"
                aria-label="Select emergency type"
                helperText="Select the type of emergency"
                SelectProps={{
                  MenuProps: {
                    MenuListProps: {
                      'aria-label': 'Emergency type options'
                    }
                  }
                }}
              >
                {['medical', 'fire', 'security', 'crowd'].map((type) => (
                  <MenuItem key={type} value={type}>
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                  </MenuItem>
                ))}
              </TextField>

              <TextField
                select
                fullWidth
                label="Location *"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                margin="normal"
                required
                aria-required="true"
                aria-label="Select location"
                helperText="Select the location of the emergency"
              >
                {locations.map((loc) => (
                  <MenuItem key={loc} value={loc}>{loc}</MenuItem>
                ))}
              </TextField>

              <TextField
                fullWidth
                multiline
                rows={3}
                label="Description *"
                placeholder="Please describe the emergency..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                margin="normal"
                required
                aria-required="true"
                aria-label="Describe the emergency"
                helperText="Provide details about the emergency"
                inputProps={{
                  maxLength: 500,
                  'aria-describedby': 'description-helper'
                }}
              />

              <Alert 
                severity="warning" 
                sx={{ mt: 2 }}
                role="alert"
                aria-live="polite"
              >
                ⚠️ Only use this for real emergencies. False reports are prohibited.
              </Alert>
            </form>
          )}
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={() => {
              setOpenDialog(false);
              announceToScreenReader('Dialog closed', 'polite');
            }}
            aria-label="Cancel and close dialog"
          >
            Cancel
          </Button>
          <Button
            variant="contained"
            color="error"
            onClick={handleSubmit}
            disabled={!location || !description || submitted}
            aria-label="Submit emergency report"
          >
            Submit Emergency
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Emergency;