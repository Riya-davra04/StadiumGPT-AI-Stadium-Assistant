import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, Chip, Grid, Card, CardContent } from '@mui/material';

const CrowdHeatmap = () => {
  const [crowdData, setCrowdData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate crowd data
    const generateData = () => {
      const locations = [
        { name: 'Gate A', density: 0.7, status: 'high' },
        { name: 'Gate B', density: 0.3, status: 'low' },
        { name: 'Gate C', density: 0.8, status: 'critical' },
        { name: 'Gate D', density: 0.2, status: 'low' },
        { name: 'Gate E', density: 0.5, status: 'medium' },
        { name: 'Food Court A', density: 0.85, status: 'critical' },
        { name: 'Food Court B', density: 0.4, status: 'medium' },
        { name: 'Restroom 1', density: 0.3, status: 'low' },
        { name: 'Restroom 2', density: 0.1, status: 'low' },
        { name: 'Section A', density: 0.6, status: 'medium' },
        { name: 'Section B', density: 0.4, status: 'low' },
        { name: 'Section C', density: 0.9, status: 'critical' },
      ];
      setCrowdData(locations);
      setLoading(false);
    };

    generateData();
    const interval = setInterval(generateData, 5000);
    return () => clearInterval(interval);
  }, []);

  const getColor = (status) => {
    switch (status) {
      case 'low': return '#4CAF50';
      case 'medium': return '#FF9800';
      case 'high': return '#F44336';
      case 'critical': return '#D32F2F';
      default: return '#9E9E9E';
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'low': return '🟢 Low';
      case 'medium': return '🟡 Medium';
      case 'high': return '🔴 High';
      case 'critical': return '🚨 Critical';
      default: return status;
    }
  };

  return (
    <Box sx={{ height: '100%', minHeight: 500 }}>
      {loading ? (
        <Box display="flex" alignItems="center" justifyContent="center" height="100%" minHeight={500}>
          <Typography>Loading crowd data...</Typography>
        </Box>
      ) : (
        <>
          <Grid container spacing={2}>
            {crowdData.map((item, index) => (
              <Grid item xs={6} sm={4} md={3} key={index}>
                <Card sx={{ borderRadius: 2 }}>
                  <CardContent>
                    <Typography variant="subtitle2" fontWeight={600}>
                      {item.name}
                    </Typography>
                    <Box display="flex" alignItems="center" gap={1} mt={1}>
                      <Box
                        sx={{
                          width: 12,
                          height: 12,
                          borderRadius: '50%',
                          bgcolor: getColor(item.status),
                        }}
                      />
                      <Chip
                        label={getStatusLabel(item.status)}
                        size="small"
                        sx={{
                          bgcolor: getColor(item.status),
                          color: 'white',
                          fontWeight: 500,
                        }}
                      />
                    </Box>
                    <Typography variant="caption" color="text.secondary" display="block" mt={0.5}>
                      Density: {Math.round(item.density * 100)}%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* Legend */}
          <Paper
            sx={{
              position: 'absolute',
              bottom: 20,
              right: 20,
              p: 2,
              bgcolor: 'rgba(255, 255, 255, 0.95)',
              borderRadius: 2,
              minWidth: 150,
              boxShadow: '0 2px 12px rgba(0,0,0,0.1)',
            }}
          >
            <Typography variant="subtitle2" fontWeight={600} gutterBottom>
              Crowd Density
            </Typography>
            <Box display="flex" flexDirection="column" gap={0.5}>
              <Box display="flex" alignItems="center" gap={1.5}>
                <Box width={20} height={4} bgcolor="#4CAF50" borderRadius={1} />
                <Typography variant="caption" color="text.secondary">Low</Typography>
              </Box>
              <Box display="flex" alignItems="center" gap={1.5}>
                <Box width={20} height={4} bgcolor="#FF9800" borderRadius={1} />
                <Typography variant="caption" color="text.secondary">Medium</Typography>
              </Box>
              <Box display="flex" alignItems="center" gap={1.5}>
                <Box width={20} height={4} bgcolor="#F44336" borderRadius={1} />
                <Typography variant="caption" color="text.secondary">High</Typography>
              </Box>
              <Box display="flex" alignItems="center" gap={1.5}>
                <Box width={20} height={4} bgcolor="#D32F2F" borderRadius={1} />
                <Typography variant="caption" color="text.secondary">Critical</Typography>
              </Box>
            </Box>
          </Paper>

          <Chip
            label="Live"
            color="error"
            size="small"
            sx={{
              position: 'absolute',
              top: 20,
              right: 20,
              fontWeight: 600,
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            }}
          />
        </>
      )}
    </Box>
  );
};

export default CrowdHeatmap;