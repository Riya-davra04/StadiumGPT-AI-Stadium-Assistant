import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Autocomplete,
} from '@mui/material';
import {
  Map as MapIcon,
  Directions,
  AccessibilityNew,
  LocationOn,
  Schedule,
  TrendingUp,
} from '@mui/icons-material';
import { useWebSocket } from '../context/WebSocketContext';
import CrowdHeatmap from '../components/CrowdHeatmap';

const Navigation = () => {
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [preferences, setPreferences] = useState([]);
  const [accessibility, setAccessibility] = useState(false);
  const [route, setRoute] = useState(null);
  const [loading, setLoading] = useState(false);
  const { sendMessage } = useWebSocket();

  const locations = [
    'Gate A', 'Gate B', 'Gate C', 'Gate D', 'Gate E',
    'Section A1', 'Section A2', 'Section B1', 'Section B2',
    'Section C1', 'Section C2',
    'Food Court A', 'Food Court B', 'Food Court C',
    'Restroom 1', 'Restroom 2', 'Restroom 3',
    'First Aid', 'Guest Services', 'VIP Lounge',
  ];

  const handleNavigate = async () => {
    if (!start || !end) return;

    setLoading(true);
    try {
      await sendMessage('navigation', {
        start,
        end,
        preferences,
        accessibility,
      });
      // Mock route response for demo
      setRoute({
        path: [start, 'Concourse', 'Elevator', 'Section C', end],
        estimatedTime: 8,
        crowdLevel: 'medium',
        alternatives: [
          { path: [start, 'Gate B', 'Concourse', end], time: 12 },
          { path: [start, 'Food Court A', 'Elevator', end], time: 10 },
        ],
        accessibilityInfo: {
          wheelchairAccessible: true,
          elevatorAvailable: true,
          rampAvailable: true,
        },
      });
    } catch (error) {
      console.error('Navigation error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>
        Stadium Navigation
      </Typography>
      <Typography variant="body2" color="text.secondary" mb={3}>
        Find the best route to your destination
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={5}>
          <Paper sx={{ p: 3, borderRadius: 3 }}>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              Plan Your Route
            </Typography>

            <Autocomplete
              fullWidth
              options={locations}
              value={start}
              onChange={(_, newValue) => setStart(newValue)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Starting Location"
                  placeholder="Where are you?"
                  margin="normal"
                  fullWidth
                />
              )}
            />

            <Autocomplete
              fullWidth
              options={locations}
              value={end}
              onChange={(_, newValue) => setEnd(newValue)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Destination"
                  placeholder="Where are you going?"
                  margin="normal"
                  fullWidth
                />
              )}
            />

            <Box mt={2}>
              <Typography variant="subtitle2" gutterBottom>
                Preferences
              </Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {['Shortest', 'Fastest', 'Scenic', 'Less Crowded'].map((pref) => (
                  <Chip
                    key={pref}
                    label={pref}
                    clickable
                    color={preferences.includes(pref) ? 'primary' : 'default'}
                    onClick={() => {
                      if (preferences.includes(pref)) {
                        setPreferences(preferences.filter(p => p !== pref));
                      } else {
                        setPreferences([...preferences, pref]);
                      }
                    }}
                  />
                ))}
                <Chip
                  label="♿ Accessibility"
                  clickable
                  color={accessibility ? 'primary' : 'default'}
                  icon={<AccessibilityNew />}
                  onClick={() => setAccessibility(!accessibility)}
                />
              </Box>
            </Box>

            <Button
              fullWidth
              variant="contained"
              size="large"
              onClick={handleNavigate}
              disabled={!start || !end || loading}
              startIcon={<Directions />}
              sx={{ mt: 3, py: 1.5, borderRadius: 2 }}
            >
              {loading ? 'Finding Route...' : 'Navigate'}
            </Button>

            {route && (
              <Box mt={3}>
                <Divider sx={{ mb: 2 }} />
                <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                  Route Details
                </Typography>
                <List dense>
                  {route.path.map((step, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        {index === 0 ? <LocationOn color="primary" /> :
                         index === route.path.length - 1 ? <LocationOn color="success" /> :
                         <Directions />}
                      </ListItemIcon>
                      <ListItemText primary={step} />
                    </ListItem>
                  ))}
                </List>
                <Box display="flex" gap={2} mt={1}>
                  <Chip icon={<Schedule />} label={`${route.estimatedTime} min`} />
                  <Chip icon={<TrendingUp />} label={`Crowd: ${route.crowdLevel}`} />
                  {route.accessibilityInfo.wheelchairAccessible && (
                    <Chip icon={<AccessibilityNew />} label="Accessible" color="success" />
                  )}
                </Box>
                {route.alternatives.length > 0 && (
                  <Box mt={2}>
                    <Typography variant="caption" color="text.secondary">
                      Alternatives:
                    </Typography>
                    {route.alternatives.map((alt, idx) => (
                      <Chip
                        key={idx}
                        label={`${alt.time} min via ${alt.path[1]}`}
                        size="small"
                        variant="outlined"
                        sx={{ ml: 1, mt: 0.5 }}
                      />
                    ))}
                  </Box>
                )}
              </Box>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={7}>
          <Paper sx={{ p: 0, borderRadius: 3, overflow: 'hidden' }}>
            <Box height={500}>
              <CrowdHeatmap />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Navigation;