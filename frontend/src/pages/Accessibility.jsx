import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Button,
  Switch,
  FormControlLabel,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  AccessibilityNew,
  Hearing,
  Visibility,
  WheelchairPickup,
  Elevator,
  CheckCircle,
  VolumeUp,
  TextFields,
} from '@mui/icons-material';

const Accessibility = () => {
  const [features, setFeatures] = useState({
    wheelchairAccess: true,
    hearingAssistance: false,
    visualAssistance: true,
    textToSpeech: true,
    highContrast: false,
    reducedMotion: false,
  });

  const accessibleRoutes = [
    { from: 'Gate A', to: 'Section A1', features: ['Elevator', 'Ramp', 'Wide Doors'] },
    { from: 'Gate C', to: 'Section B2', features: ['Wheelchair Access', 'Accessible Restroom'] },
    { from: 'Gate D', to: 'Guest Services', features: ['Elevator', 'Visual Guidance'] },
  ];

  const handleToggle = (feature) => {
    setFeatures(prev => ({
      ...prev,
      [feature]: !prev[feature],
    }));
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>
        Accessibility
      </Typography>
      <Typography variant="body2" color="text.secondary" mb={3}>
        Accessibility features and services for all fans
      </Typography>

      <Grid container spacing={3}>
        {/* Settings */}
        <Grid item xs={12} md={4}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Accessibility Settings
              </Typography>
              <Box sx={{ mt: 2 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={features.wheelchairAccess}
                      onChange={() => handleToggle('wheelchairAccess')}
                      color="primary"
                    />
                  }
                  label={
                    <Box display="flex" alignItems="center" gap={1}>
                      <WheelchairPickup />
                      <Typography variant="body2">Wheelchair Access</Typography>
                    </Box>
                  }
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={features.hearingAssistance}
                      onChange={() => handleToggle('hearingAssistance')}
                      color="primary"
                    />
                  }
                  label={
                    <Box display="flex" alignItems="center" gap={1}>
                      <Hearing />
                      <Typography variant="body2">Hearing Assistance</Typography>
                    </Box>
                  }
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={features.visualAssistance}
                      onChange={() => handleToggle('visualAssistance')}
                      color="primary"
                    />
                  }
                  label={
                    <Box display="flex" alignItems="center" gap={1}>
                      <Visibility />
                      <Typography variant="body2">Visual Assistance</Typography>
                    </Box>
                  }
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={features.textToSpeech}
                      onChange={() => handleToggle('textToSpeech')}
                      color="primary"
                    />
                  }
                  label={
                    <Box display="flex" alignItems="center" gap={1}>
                      <VolumeUp />
                      <Typography variant="body2">Text-to-Speech</Typography>
                    </Box>
                  }
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={features.highContrast}
                      onChange={() => handleToggle('highContrast')}
                      color="primary"
                    />
                  }
                  label={
                    <Box display="flex" alignItems="center" gap={1}>
                      <TextFields />
                      <Typography variant="body2">High Contrast</Typography>
                    </Box>
                  }
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Accessible Routes */}
        <Grid item xs={12} md={8}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Accessible Routes
              </Typography>
              <List>
                {accessibleRoutes.map((route, index) => (
                  <React.Fragment key={index}>
                    <ListItem>
                      <ListItemIcon>
                        <AccessibilityNew color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box display="flex" alignItems="center" gap={1}>
                            <Typography variant="subtitle2" fontWeight={600}>
                              {route.from} → {route.to}
                            </Typography>
                          </Box>
                        }
                        secondary={
                          <Box display="flex" gap={1} mt={0.5}>
                            {route.features.map((feature, idx) => (
                              <Chip
                                key={idx}
                                label={feature}
                                size="small"
                                icon={<CheckCircle />}
                                color="success"
                                variant="outlined"
                              />
                            ))}
                          </Box>
                        }
                      />
                      <Button
                        variant="contained"
                        size="small"
                        startIcon={<Elevator />}
                      >
                        Navigate
                      </Button>
                    </ListItem>
                    {index < accessibleRoutes.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>

          {/* Services */}
          <Card sx={{ borderRadius: 3, mt: 3 }}>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Accessibility Services
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <WheelchairPickup color="primary" />
                    <Box>
                      <Typography variant="subtitle2">Wheelchair Rental</Typography>
                      <Typography variant="caption" color="text.secondary">
                        Available at Guest Services
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Hearing color="primary" />
                    <Box>
                      <Typography variant="subtitle2">Hearing Devices</Typography>
                      <Typography variant="caption" color="text.secondary">
                        Available at Guest Services
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Visibility color="primary" />
                    <Box>
                      <Typography variant="subtitle2">Visual Assistance</Typography>
                      <Typography variant="caption" color="text.secondary">
                        App-based guidance
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Elevator color="primary" />
                    <Box>
                      <Typography variant="subtitle2">Elevator Access</Typography>
                      <Typography variant="caption" color="text.secondary">
                        Gates A, C, and E
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Accessibility;