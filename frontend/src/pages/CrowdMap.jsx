import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Slider,
  Button,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import {
  Refresh,
  Warning,
  CheckCircle,
  People,
  LocationOn,
  TrendingUp,
  TrendingDown,
} from '@mui/icons-material';
import CrowdHeatmap from '../components/CrowdHeatmap';
import { useWebSocket } from '../context/WebSocketContext';

const CrowdMap = () => {
  const { sendMessage } = useWebSocket();
  const [crowdData, setCrowdData] = useState({
    overall: 0.45,
    sections: {},
    hotspots: [],
    predictions: [],
    recommendations: [],
  });
  const [timeRange, setTimeRange] = useState(15);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCrowdData();
    const interval = setInterval(fetchCrowdData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchCrowdData = async () => {
    setLoading(true);
    // Mock data
    const sections = {
      'Gate A': 0.7,
      'Gate B': 0.3,
      'Gate C': 0.8,
      'Gate D': 0.2,
      'Gate E': 0.5,
      'Section A': 0.6,
      'Section B': 0.4,
      'Section C': 0.9,
      'Food Court A': 0.85,
      'Food Court B': 0.5,
      'Restroom 1': 0.3,
      'Restroom 2': 0.1,
    };

    const hotspots = Object.entries(sections)
      .filter(([_, value]) => value > 0.7)
      .map(([name, density]) => ({ name, density }));

    setCrowdData({
      overall: Object.values(sections).reduce((a, b) => a + b, 0) / Object.values(sections).length,
      sections,
      hotspots,
      predictions: [
        { time: '15 min', level: 'high' },
        { time: '30 min', level: 'medium' },
        { time: '60 min', level: 'low' },
      ],
      recommendations: [
        'Open additional gates to reduce congestion',
        'Redirect fans to less crowded entrances',
        'Increase security presence at hotspots',
      ],
    });
    setLoading(false);
  };

  const getColor = (value) => {
    if (value < 0.3) return '#4CAF50';
    if (value < 0.6) return '#FF9800';
    if (value < 0.8) return '#F44336';
    return '#D32F2F';
  };

  const getLevel = (value) => {
    if (value < 0.3) return 'Low';
    if (value < 0.6) return 'Medium';
    if (value < 0.8) return 'High';
    return 'Critical';
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" fontWeight={700}>
            Crowd Map
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Real-time crowd density and heatmap
          </Typography>
        </Box>
        <Box display="flex" gap={2} alignItems="center">
          <Button
            startIcon={<Refresh />}
            variant="outlined"
            onClick={fetchCrowdData}
            disabled={loading}
          >
            Refresh
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 0, borderRadius: 3, overflow: 'hidden' }}>
            <Box height={550}>
              <CrowdHeatmap />
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Paper sx={{ p: 2, borderRadius: 3 }}>
                <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                  Overall Crowd Level
                </Typography>
                <Box display="flex" alignItems="center" gap={2}>
                  <Box
                    sx={{
                      width: 60,
                      height: 60,
                      borderRadius: '50%',
                      bgcolor: getColor(crowdData.overall),
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'white',
                      fontWeight: 700,
                      fontSize: '1.5rem',
                    }}
                  >
                    {Math.round(crowdData.overall * 100)}%
                  </Box>
                  <Box>
                    <Typography variant="h5" fontWeight={700}>
                      {getLevel(crowdData.overall)}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {crowdData.overall > 0.7 ? 'High congestion' : 
                       crowdData.overall > 0.4 ? 'Moderate flow' : 
                       'Smooth operations'}
                    </Typography>
                  </Box>
                </Box>
              </Paper>
            </Grid>

            <Grid item xs={12}>
              <Paper sx={{ p: 2, borderRadius: 3 }}>
                <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                  Hotspots
                </Typography>
                {crowdData.hotspots.length > 0 ? (
                  <List dense>
                    {crowdData.hotspots.map((spot, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <Warning color="error" />
                        </ListItemIcon>
                        <ListItemText
                          primary={spot.name}
                          secondary={`Density: ${Math.round(spot.density * 100)}%`}
                        />
                      </ListItem>
                    ))}
                  </List>
                ) : (
                  <Typography color="text.secondary" variant="body2">
                    No hotspots detected
                  </Typography>
                )}
              </Paper>
            </Grid>

            <Grid item xs={12}>
              <Paper sx={{ p: 2, borderRadius: 3 }}>
                <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                  Predictions
                </Typography>
                {crowdData.predictions.map((pred, index) => (
                  <Box key={index} display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                    <Typography variant="body2">{pred.time}</Typography>
                    <Chip
                      label={pred.level}
                      size="small"
                      color={pred.level === 'high' ? 'error' : pred.level === 'medium' ? 'warning' : 'success'}
                    />
                  </Box>
                ))}
              </Paper>
            </Grid>

            <Grid item xs={12}>
              <Paper sx={{ p: 2, borderRadius: 3 }}>
                <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                  Recommendations
                </Typography>
                {crowdData.recommendations.map((rec, index) => (
                  <Box key={index} display="flex" alignItems="center" gap={1} mb={1}>
                    <CheckCircle color="primary" fontSize="small" />
                    <Typography variant="body2">{rec}</Typography>
                  </Box>
                ))}
              </Paper>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CrowdMap;