import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Button,
} from '@mui/material';
import {
  People,
  Restaurant,
  Warning as WarningIcon,
  DirectionsBus,
  TrendingUp,
  Refresh,
  CheckCircle,
  Schedule,
} from '@mui/icons-material';
import { useWebSocket } from '../context/WebSocketContext';
import { useAuth } from '../context/AuthContext';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const { user } = useAuth();
  const { isConnected } = useWebSocket();
  const [stats, setStats] = useState({
    crowdLevel: 'medium',
    totalAttendance: 45231,
    capacity: 80000,
    queueCount: 12,
    avgWaitTime: 8,
    satisfaction: 92,
  });
  const [crowdHistory, setCrowdHistory] = useState([]);
  const [queueData, setQueueData] = useState([]);

  useEffect(() => {
    generateMockData();
    const interval = setInterval(generateMockData, 30000);
    return () => clearInterval(interval);
  }, []);

  const generateMockData = () => {
    const history = [];
    for (let i = 0; i < 12; i++) {
      history.push({
        time: `${i * 5}min`,
        crowd: Math.floor(20000 + Math.random() * 40000),
      });
    }
    setCrowdHistory(history);

    const queues = [
      { name: 'Food A', wait: Math.floor(Math.random() * 15) + 2 },
      { name: 'Food B', wait: Math.floor(Math.random() * 10) + 1 },
      { name: 'Food C', wait: Math.floor(Math.random() * 20) + 3 },
      { name: 'Restroom 1', wait: Math.floor(Math.random() * 5) + 1 },
      { name: 'Restroom 2', wait: Math.floor(Math.random() * 3) + 0 },
      { name: 'Merch', wait: Math.floor(Math.random() * 12) + 2 },
    ];
    setQueueData(queues);

    setStats(prev => ({
      ...prev,
      totalAttendance: Math.floor(30000 + Math.random() * 30000),
      queueCount: Math.floor(5 + Math.random() * 15),
      avgWaitTime: Math.floor(3 + Math.random() * 12),
      satisfaction: Math.floor(80 + Math.random() * 15),
    }));
  };

  const crowdLevelColors = {
    low: '#4CAF50',
    medium: '#FF9800',
    high: '#F44336',
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" fontWeight={700}>
            Dashboard
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Welcome back, {user?.name || 'Guest'}!
          </Typography>
        </Box>
        <Box display="flex" gap={1}>
          <Chip
            label={isConnected ? '🟢 Live' : '🔴 Offline'}
            color={isConnected ? 'success' : 'error'}
            size="small"
          />
          <Button startIcon={<Refresh />} variant="outlined" size="small" onClick={generateMockData}>
            Refresh
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography color="text.secondary" variant="caption">Attendance</Typography>
              <Typography variant="h4" fontWeight={700}>
                {stats.totalAttendance.toLocaleString()}
              </Typography>
              <LinearProgress
                variant="determinate"
                value={(stats.totalAttendance / stats.capacity) * 100}
                sx={{ mt: 2, height: 6, borderRadius: 3 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography color="text.secondary" variant="caption">Crowd Level</Typography>
              <Box display="flex" alignItems="center" gap={1}>
                <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: crowdLevelColors[stats.crowdLevel] }} />
                <Typography variant="h4" fontWeight={700} textTransform="capitalize">
                  {stats.crowdLevel}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography color="text.secondary" variant="caption">Avg Wait Time</Typography>
              <Typography variant="h4" fontWeight={700}>
                {stats.avgWaitTime} min
              </Typography>
              <Typography variant="caption" color="text.secondary">
                across {stats.queueCount} queues
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography color="text.secondary" variant="caption">Satisfaction</Typography>
              <Typography variant="h4" fontWeight={700}>
                {stats.satisfaction}%
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {stats.satisfaction > 85 ? '⭐ Excellent' : '⭐ Good'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, borderRadius: 3 }}>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              Crowd Attendance Trend
            </Typography>
            <Box height={300}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={crowdHistory}>
                  <XAxis dataKey="time" stroke="#888" />
                  <YAxis stroke="#888" />
                  <Tooltip />
                  <Line type="monotone" dataKey="crowd" stroke="#1976D2" strokeWidth={3} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, borderRadius: 3 }}>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              Queue Distribution
            </Typography>
            <Box height={300}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={queueData} layout="vertical">
                  <XAxis type="number" stroke="#888" />
                  <YAxis type="category" dataKey="name" stroke="#888" width={60} />
                  <Tooltip />
                  <Bar dataKey="wait" fill="#1976D2" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3, borderRadius: 3 }}>
            <Typography variant="h6" fontWeight={600} gutterBottom>
              Quick Actions
            </Typography>
            <Grid container spacing={2}>
              {[
                { label: 'Emergency', icon: <WarningIcon />, color: 'error', path: '/emergency' },
                { label: 'Navigation', icon: <DirectionsBus />, color: 'primary', path: '/navigation' },
                { label: 'Crowd Map', icon: <People />, color: 'warning', path: '/crowd-map' },
                { label: 'Queues', icon: <Restaurant />, color: 'success', path: '/queues' },
              ].map((action) => (
                <Grid item xs={6} sm={3} key={action.label}>
                  <Button
                    variant="contained"
                    color={action.color}
                    fullWidth
                    startIcon={action.icon}
                    href={action.path}
                    sx={{ py: 2, borderRadius: 2 }}
                  >
                    {action.label}
                  </Button>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;