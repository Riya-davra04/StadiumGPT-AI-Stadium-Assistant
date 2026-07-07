import React, { useState, useEffect, useRef } from 'react';
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
  WifiOff,
  Wifi,
} from '@mui/icons-material';
import { useWebSocket } from '../context/WebSocketContext';
import { useAuth } from '../context/AuthContext';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { announceToScreenReader, setPageTitle } from '../utils/accessibility';

const Dashboard = () => {
  const { user } = useAuth();
  const { isConnected, messages } = useWebSocket();
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
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const timerRef = useRef(null);

  useEffect(() => {
    setPageTitle('Dashboard');
    generateMockData();
    const interval = setInterval(generateMockData, 30000);
    return () => {
      clearInterval(interval);
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  // ✅ WebSocket real-time updates
  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      if (lastMessage.type === 'crowd_broadcast') {
        const data = lastMessage.data;
        setStats(prev => ({
          ...prev,
          crowdLevel: data.crowd_level || prev.crowdLevel,
          totalAttendance: data.current_density ? Math.floor(data.current_density * 80000) : prev.totalAttendance,
        }));
        setLastUpdate(new Date());
        
        // ✅ Announce updates to screen readers
        if (data.crowd_level === 'high') {
          announceToScreenReader('Alert: High crowd density detected', 'assertive');
        }
      }
    }
  }, [messages]);

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
  };

  const crowdLevelColors = {
    low: '#4CAF50',
    medium: '#FF9800',
    high: '#F44336',
  };

  return (
    <Box role="main" id="main-content" aria-label="Dashboard">
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h1" sx={{ fontSize: '2rem', fontWeight: 700 }}>
            Dashboard
          </Typography>
          <Typography variant="body2" color="text.secondary" aria-live="polite">
            Welcome back, {user?.name || 'Guest'}! Here's your stadium overview.
          </Typography>
        </Box>
        <Box display="flex" gap={2} alignItems="center">
          <Chip
            label={isConnected ? '🟢 Live' : '🔴 Offline'}
            color={isConnected ? 'success' : 'error'}
            size="small"
            role="status"
            aria-live="polite"
          />
          <Typography variant="caption" color="text.secondary">
            Updated: {lastUpdate.toLocaleTimeString()}
          </Typography>
          <Button
            startIcon={<Refresh />}
            variant="outlined"
            size="small"
            onClick={generateMockData}
            aria-label="Refresh dashboard data"
          >
            Refresh
          </Button>
        </Box>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card 
            sx={{ borderRadius: 3, '&:hover': { boxShadow: 6 } }}
            role="article"
            aria-label={`Attendance: ${stats.totalAttendance.toLocaleString()}`}
          >
            <CardContent>
              <Typography color="text.secondary" variant="caption" fontWeight={500}>
                Attendance
              </Typography>
              <Typography variant="h4" fontWeight={700} aria-live="polite">
                {stats.totalAttendance.toLocaleString()}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                of {stats.capacity.toLocaleString()} capacity
              </Typography>
              <LinearProgress
                variant="determinate"
                value={(stats.totalAttendance / stats.capacity) * 100}
                sx={{ mt: 2, height: 6, borderRadius: 3 }}
                aria-label={`${Math.round((stats.totalAttendance / stats.capacity) * 100)}% full`}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card 
            sx={{ borderRadius: 3, '&:hover': { boxShadow: 6 } }}
            role="article"
            aria-label={`Crowd level: ${stats.crowdLevel}`}
          >
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography color="text.secondary" variant="caption" fontWeight={500}>
                    Crowd Level
                  </Typography>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        borderRadius: '50%',
                        bgcolor: crowdLevelColors[stats.crowdLevel],
                      }}
                    />
                    <Typography variant="h4" fontWeight={700} textTransform="capitalize">
                      {stats.crowdLevel}
                    </Typography>
                  </Box>
                </Box>
                <Box sx={{ bgcolor: 'warning.light', borderRadius: 2, p: 1, color: 'warning.main' }}>
                  <TrendingUp />
                </Box>
              </Box>
              <Typography variant="caption" color="text.secondary" display="block" mt={1}>
                {stats.crowdLevel === 'high' ? '🚨 Consider alternative routes' : 
                 stats.crowdLevel === 'medium' ? '⚡ Manageable but busy' : 
                 '✅ Smooth operations'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card 
            sx={{ borderRadius: 3, '&:hover': { boxShadow: 6 } }}
            role="article"
            aria-label={`Average wait time: ${stats.avgWaitTime} minutes`}
          >
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography color="text.secondary" variant="caption" fontWeight={500}>
                    Avg Wait Time
                  </Typography>
                  <Typography variant="h4" fontWeight={700}>
                    {stats.avgWaitTime} min
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    across {stats.queueCount} queues
                  </Typography>
                </Box>
                <Box sx={{ bgcolor: 'info.light', borderRadius: 2, p: 1, color: 'info.main' }}>
                  <Schedule />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card 
            sx={{ borderRadius: 3, '&:hover': { boxShadow: 6 } }}
            role="article"
            aria-label={`Satisfaction rate: ${stats.satisfaction}%`}
          >
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography color="text.secondary" variant="caption" fontWeight={500}>
                    Satisfaction
                  </Typography>
                  <Typography variant="h4" fontWeight={700}>
                    {stats.satisfaction}%
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {stats.satisfaction > 85 ? '⭐ Excellent' : '⭐ Good'}
                  </Typography>
                </Box>
                <Box sx={{ bgcolor: 'success.light', borderRadius: 2, p: 1, color: 'success.main' }}>
                  <CheckCircle />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, borderRadius: 3 }} role="figure" aria-label="Crowd attendance trend chart">
            <Typography variant="h6" fontWeight={600} gutterBottom>
              Crowd Attendance Trend
            </Typography>
            <Box height={300}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={crowdHistory}>
                  <XAxis dataKey="time" stroke="#888" />
                  <YAxis stroke="#888" />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="crowd"
                    stroke="#1976D2"
                    strokeWidth={3}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, borderRadius: 3 }} role="figure" aria-label="Queue distribution chart">
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
          <Paper sx={{ p: 3, borderRadius: 3 }} role="navigation" aria-label="Quick actions">
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
                    aria-label={`Go to ${action.label}`}
                  >
                    {action.label}
                  </Button>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>
      </Grid>

      {/* WebSocket Status */}
      <Box mt={2} display="flex" alignItems="center" gap={1}>
        {isConnected ? <Wifi fontSize="small" color="success" /> : <WifiOff fontSize="small" color="error" />}
        <Typography variant="caption" color="text.secondary">
          {isConnected ? 'Real-time updates active' : 'Reconnecting...'}
        </Typography>
      </Box>
    </Box>
  );
};

export default Dashboard;