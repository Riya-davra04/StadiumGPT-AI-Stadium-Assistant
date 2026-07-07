import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Button,
  LinearProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  DirectionsBus,
  Train,
  LocalTaxi,
  LocalParking,  // ✅ Changed from Parking
  Directions,
  Schedule,
  AttachMoney,
  CheckCircle,
  Warning,
} from '@mui/icons-material';

const Transport = () => {
  const [transportOptions, setTransportOptions] = useState([]);
  const [parking, setParking] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);

  useEffect(() => {
    fetchTransportData();
    const interval = setInterval(fetchTransportData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchTransportData = () => {
    // Mock transport data
    setTransportOptions([
      {
        id: 'metro',
        name: 'Metro',
        icon: <Train />,
        distance: '200m',
        time: '5 min',
        crowd: 'medium',
        availability: 'available',
        waitTime: '3 min',
        cost: '$2.50',
        status: 'running',
      },
      {
        id: 'bus',
        name: 'Bus',
        icon: <DirectionsBus />,
        distance: '150m',
        time: '10 min',
        crowd: 'low',
        availability: 'available',
        waitTime: '15 min',
        cost: '$1.50',
        status: 'on-time',
      },
      {
        id: 'taxi',
        name: 'Ride Share',
        icon: <LocalTaxi />,
        distance: '100m',
        time: '8 min',
        crowd: 'low',
        availability: 'limited',
        waitTime: '20 min',
        cost: '$15.50',
        status: 'available',
      },
      {
        id: 'parking',
        name: 'Parking',
        icon: <LocalParking />,  // ✅ Changed
        distance: '300m',
        time: '12 min',
        crowd: 'high',
        availability: 'limited',
        waitTime: 'N/A',
        cost: '$10.00',
        status: 'almost-full',
      },
    ]);

    setParking([
      { id: 'P1', name: 'Parking P1', available: 45, total: 200, status: 'available' },
      { id: 'P2', name: 'Parking P2', available: 12, total: 150, status: 'limited' },
      { id: 'P3', name: 'Parking P3', available: 0, total: 100, status: 'full' },
    ]);
  };

  const getCrowdColor = (level) => {
    switch (level) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      default: return 'default';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'available':
      case 'running':
      case 'on-time': return 'success';
      case 'limited':
      case 'almost-full': return 'warning';
      case 'full': return 'error';
      default: return 'default';
    }
  };

  const getRecommendation = () => {
    const best = transportOptions
      .filter(t => t.availability === 'available')
      .sort((a, b) => parseInt(a.time) - parseInt(b.time))[0];
    
    if (best) {
      return {
        option: best,
        message: `🚀 Best option: ${best.name} - Only ${best.time} away!`,
      };
    }
    return null;
  };

  const recommendation = getRecommendation();

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>
        Transport
      </Typography>
      <Typography variant="body2" color="text.secondary" mb={3}>
        Real-time transport options and parking availability
      </Typography>

      {/* Recommendation */}
      {recommendation && (
        <Card sx={{ borderRadius: 3, mb: 3, bgcolor: 'success.light', color: 'white' }}>
          <CardContent>
            <Box display="flex" alignItems="center" gap={2}>
              <CheckCircle />
              <Box>
                <Typography variant="subtitle1" fontWeight={600}>
                  Recommended Transport
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  {recommendation.message}
                </Typography>
              </Box>
              <Button
                variant="contained"
                color="primary"
                sx={{ ml: 'auto', bgcolor: 'white', color: 'text.primary' }}
              >
                Get Directions
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}

      <Grid container spacing={3}>
        {/* Transport Options */}
        <Grid item xs={12} md={8}>
          <Grid container spacing={2}>
            {transportOptions.map((option) => (
              <Grid item xs={12} sm={6} key={option.id}>
                <Card
                  sx={{
                    borderRadius: 3,
                    cursor: 'pointer',
                    '&:hover': { boxShadow: 6 },
                    border: selectedOption?.id === option.id ? '2px solid #1976D2' : 'none',
                  }}
                  onClick={() => setSelectedOption(option)}
                >
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="center">
                      <Box display="flex" alignItems="center" gap={1}>
                        {option.icon}
                        <Typography variant="h6" fontWeight={600}>
                          {option.name}
                        </Typography>
                      </Box>
                      <Chip
                        label={option.status}
                        color={getStatusColor(option.status)}
                        size="small"
                      />
                    </Box>

                    <Box display="flex" gap={2} mt={2}>
                      <Box>
                        <Typography variant="caption" color="text.secondary">
                          Distance
                        </Typography>
                        <Typography variant="body2" fontWeight={500}>
                          {option.distance}
                        </Typography>
                      </Box>
                      <Box>
                        <Typography variant="caption" color="text.secondary">
                          Time
                        </Typography>
                        <Typography variant="body2" fontWeight={500}>
                          {option.time}
                        </Typography>
                      </Box>
                      <Box>
                        <Typography variant="caption" color="text.secondary">
                          Cost
                        </Typography>
                        <Typography variant="body2" fontWeight={500}>
                          {option.cost}
                        </Typography>
                      </Box>
                    </Box>

                    <Box display="flex" gap={1} mt={1}>
                      <Chip
                        label={`Crowd: ${option.crowd}`}
                        size="small"
                        color={getCrowdColor(option.crowd)}
                        variant="outlined"
                      />
                      {option.waitTime !== 'N/A' && (
                        <Chip
                          icon={<Schedule />}
                          label={`Wait: ${option.waitTime}`}
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>

        {/* Parking */}
        <Grid item xs={12} md={4}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Parking Status
              </Typography>
              <List>
                {parking.map((p) => (
                  <React.Fragment key={p.id}>
                    <ListItem>
                      <ListItemIcon>
                        <LocalParking  // ✅ Changed
                          color={p.status === 'full' ? 'error' : p.status === 'limited' ? 'warning' : 'success'}
                        />
                      </ListItemIcon>
                      <ListItemText
                        primary={p.name}
                        secondary={
                          <Box>
                            <Typography variant="body2">
                              {p.available} / {p.total} available
                            </Typography>
                            <LinearProgress
                              variant="determinate"
                              value={(p.available / p.total) * 100}
                              sx={{ height: 4, borderRadius: 2, mt: 0.5 }}
                              color={p.status === 'full' ? 'error' : p.status === 'limited' ? 'warning' : 'success'}
                            />
                          </Box>
                        }
                      />
                      <Chip
                        label={p.status}
                        size="small"
                        color={getStatusColor(p.status)}
                      />
                    </ListItem>
                    <Divider />
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>

          {/* Tips */}
          <Card sx={{ borderRadius: 3, mt: 3 }}>
            <CardContent>
              <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                💡 Transport Tips
              </Typography>
              <Box display="flex" flexDirection="column" gap={1}>
                <Typography variant="body2">
                  • Metro is fastest during peak hours
                </Typography>
                <Typography variant="body2">
                  • Book ride-share 15 min before leaving
                </Typography>
                <Typography variant="body2">
                  • Parking P2 has best availability
                </Typography>
                <Typography variant="body2">
                  • Leave after 12 min to avoid traffic
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Transport;