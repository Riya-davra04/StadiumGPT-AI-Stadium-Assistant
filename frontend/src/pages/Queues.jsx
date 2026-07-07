import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  IconButton,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
} from '@mui/material';
import {
  Restaurant,
  RestaurantMenu,
  LocalDrink,
  ShoppingBag,
  Refresh,
  Directions,
  Schedule,
  CheckCircle,
  Warning,
} from '@mui/icons-material';
import { useWebSocket } from '../context/WebSocketContext';

const Queues = () => {
  const { sendMessage } = useWebSocket();
  const [queues, setQueues] = useState([]);
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    fetchQueues();
    const interval = setInterval(fetchQueues, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchQueues = async () => {
    setLoading(true);
    // Mock data
    const mockQueues = [
      { id: 'food_a', name: 'Food Court A', type: 'food', waitTime: 25, length: 45, capacity: 50, status: 'busy' },
      { id: 'food_b', name: 'Food Court B', type: 'food', waitTime: 6, length: 12, capacity: 40, status: 'available' },
      { id: 'food_c', name: 'Food Court C', type: 'food', waitTime: 18, length: 35, capacity: 60, status: 'moderate' },
      { id: 'restroom_1', name: 'Restroom 1', type: 'restroom', waitTime: 3, length: 8, capacity: 10, status: 'available' },
      { id: 'restroom_2', name: 'Restroom 2', type: 'restroom', waitTime: 0, length: 2, capacity: 12, status: 'available' },
      { id: 'restroom_3', name: 'Restroom 3', type: 'restroom', waitTime: 8, length: 20, capacity: 8, status: 'busy' },
      { id: 'merch_1', name: 'Merchandise Store', type: 'merch', waitTime: 12, length: 25, capacity: 20, status: 'moderate' },
    ];

    setQueues(mockQueues);

    // Generate recommendations
    const bestFood = mockQueues.filter(q => q.type === 'food').sort((a, b) => a.waitTime - b.waitTime)[0];
    const bestRestroom = mockQueues.filter(q => q.type === 'restroom').sort((a, b) => a.waitTime - b.waitTime)[0];
    
    setRecommendations([
      {
        type: 'food',
        title: 'Best Food Option',
        description: `${bestFood.name} - Only ${bestFood.waitTime} min wait`,
        action: `Walk 2 minutes to save ${25 - bestFood.waitTime} minutes`,
      },
      {
        type: 'restroom',
        title: 'Best Restroom',
        description: `${bestRestroom.name} - ${bestRestroom.length} people waiting`,
        action: 'Available now',
      },
    ]);
    setLoading(false);
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'food': return <RestaurantMenu />;
      case 'restroom': return <LocalDrink />;
      case 'merch': return <ShoppingBag />;
      default: return <Restaurant />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'available': return 'success';
      case 'moderate': return 'warning';
      case 'busy': return 'error';
      default: return 'default';
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'available': return '🟢 Available';
      case 'moderate': return '🟡 Moderate';
      case 'busy': return '🔴 Busy';
      default: return status;
    }
  };

  const getLoadPercentage = (length, capacity) => {
    return Math.min((length / capacity) * 100, 100);
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" fontWeight={700}>
            Queue Status
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Real-time queue wait times and predictions
          </Typography>
        </Box>
        <Button
          startIcon={<Refresh />}
          variant="outlined"
          onClick={fetchQueues}
          disabled={loading}
        >
          Refresh
        </Button>
      </Box>

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <Grid container spacing={2} mb={3}>
          {recommendations.map((rec, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card sx={{ borderRadius: 3, bgcolor: 'primary.light', color: 'white' }}>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={1}>
                    <CheckCircle />
                    <Typography variant="subtitle2" fontWeight={600}>
                      {rec.title}
                    </Typography>
                  </Box>
                  <Typography variant="body2" sx={{ opacity: 0.9, mt: 1 }}>
                    {rec.description}
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.8, display: 'block', mt: 1 }}>
                    💡 {rec.action}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Queue Cards */}
      <Grid container spacing={3}>
        {queues.map((queue) => (
          <Grid item xs={12} sm={6} md={4} key={queue.id}>
            <Card sx={{ borderRadius: 3, '&:hover': { boxShadow: 6 } }}>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Box display="flex" alignItems="center" gap={1}>
                    {getTypeIcon(queue.type)}
                    <Typography variant="h6" fontWeight={600} fontSize="1rem">
                      {queue.name}
                    </Typography>
                  </Box>
                  <Chip
                    label={getStatusLabel(queue.status)}
                    color={getStatusColor(queue.status)}
                    size="small"
                  />
                </Box>

                <Box display="flex" justifyContent="space-between" alignItems="center" mt={2}>
                  <Box>
                    <Typography variant="caption" color="text.secondary">
                      Wait Time
                    </Typography>
                    <Typography variant="h5" fontWeight={700}>
                      {queue.waitTime} min
                    </Typography>
                  </Box>
                  <Box textAlign="right">
                    <Typography variant="caption" color="text.secondary">
                      Queue Length
                    </Typography>
                    <Typography variant="h5" fontWeight={700}>
                      {queue.length}
                    </Typography>
                  </Box>
                </Box>

                <Box mt={2}>
                  <Box display="flex" justifyContent="space-between" mb={0.5}>
                    <Typography variant="caption" color="text.secondary">
                      Capacity
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {queue.length}/{queue.capacity}
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={getLoadPercentage(queue.length, queue.capacity)}
                    sx={{ height: 6, borderRadius: 3 }}
                    color={getStatusColor(queue.status)}
                  />
                </Box>

                {queue.waitTime > 15 && (
                  <Button
                    fullWidth
                    variant="outlined"
                    size="small"
                    startIcon={<Directions />}
                    sx={{ mt: 2 }}
                  >
                    Find Alternative
                  </Button>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Queues;