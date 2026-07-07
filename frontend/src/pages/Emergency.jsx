import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  TextField,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Warning as WarningIcon,  // ✅ Changed from EmergencyIcon
  MedicalServices,
  FireExtinguisher,
  Security,
  CheckCircle,
  LocationOn,
  Phone,
  People,
} from '@mui/icons-material';
import { useWebSocket } from '../context/WebSocketContext';

const Emergency = () => {
  const { sendMessage } = useWebSocket();
  const [openDialog, setOpenDialog] = useState(false);
  const [emergencyType, setEmergencyType] = useState('medical');
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [activeAlerts, setActiveAlerts] = useState([
    {
      id: 1,
      type: 'medical',
      location: 'Section A',
      severity: 'medium',
      status: 'active',
      time: '2 min ago',
    },
    {
      id: 2,
      type: 'security',
      location: 'Gate B',
      severity: 'low',
      status: 'responded',
      time: '15 min ago',
    },
  ]);

  const emergencyTypes = [
    { value: 'medical', label: 'Medical', icon: <MedicalServices /> },
    { value: 'fire', label: 'Fire', icon: <FireExtinguisher /> },
    { value: 'security', label: 'Security', icon: <Security /> },
    { value: 'crowd', label: 'Crowd Issue', icon: <People /> },
  ];

  const locations = [
    'Gate A', 'Gate B', 'Gate C', 'Gate D', 'Gate E',
    'Section A1', 'Section A2', 'Section B1', 'Section B2',
    'Section C1', 'Section C2',
    'Food Court A', 'Food Court B', 'Food Court C',
    'Restroom 1', 'Restroom 2', 'Restroom 3',
    'First Aid Station', 'Guest Services',
  ];

  const handleSubmit = async () => {
    try {
      await sendMessage('emergency', {
        type: emergencyType,
        location,
        description,
        severity: 'medium',
      });
      setSubmitted(true);
      setTimeout(() => {
        setOpenDialog(false);
        setSubmitted(false);
        setDescription('');
        setLocation('');
      }, 3000);
    } catch (error) {
      console.error('Emergency report error:', error);
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'medical': return 'error';
      case 'fire': return 'error';
      case 'security': return 'warning';
      case 'crowd': return 'warning';
      default: return 'info';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'error';
      case 'responded': return 'warning';
      case 'resolved': return 'success';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" fontWeight={700}>
            Emergency
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Report emergencies and view active alerts
          </Typography>
        </Box>
        <Button
          variant="contained"
          color="error"
          startIcon={<WarningIcon />}  // ✅ Changed from EmergencyIcon
          onClick={() => setOpenDialog(true)}
          sx={{ borderRadius: 2 }}
        >
          Report Emergency
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Emergency Contacts */}
        <Grid item xs={12} md={4}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Emergency Contacts
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <MedicalServices color="error" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Medical Team"
                    secondary="Call: 111"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <Security color="warning" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Security"
                    secondary="Call: 112"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <FireExtinguisher color="error" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Fire Department"
                    secondary="Call: 113"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <Phone color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="General Emergency"
                    secondary="Call: 911"
                  />
                </ListItem>
              </List>
              <Divider sx={{ my: 2 }} />
              <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                First Aid Stations
              </Typography>
              <Typography variant="body2" color="text.secondary">
                📍 Section A - Main Level
              </Typography>
              <Typography variant="body2" color="text.secondary">
                📍 Section C - Upper Level
              </Typography>
              <Typography variant="body2" color="text.secondary">
                📍 Section E - Lower Level
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Active Alerts */}
        <Grid item xs={12} md={8}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Active Alerts
              </Typography>
              {activeAlerts.length > 0 ? (
                <List>
                  {activeAlerts.map((alert) => (
                    <React.Fragment key={alert.id}>
                      <ListItem>
                        <ListItemIcon>
                          <WarningIcon color={getTypeColor(alert.type)} />  {/* ✅ Changed */}
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Box display="flex" alignItems="center" gap={1}>
                              <Typography variant="subtitle2" fontWeight={600}>
                                {alert.type.toUpperCase()}
                              </Typography>
                              <Chip
                                label={alert.status}
                                size="small"
                                color={getStatusColor(alert.status)}
                              />
                              <Chip
                                label={alert.severity}
                                size="small"
                                color={alert.severity === 'critical' ? 'error' : 'warning'}
                              />
                            </Box>
                          }
                          secondary={
                            <Box>
                              <Typography variant="body2">
                                📍 {alert.location}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                {alert.time}
                              </Typography>
                            </Box>
                          }
                        />
                        {alert.status === 'active' && (
                          <Button
                            size="small"
                            variant="contained"
                            color="primary"
                          >
                            Respond
                          </Button>
                        )}
                      </ListItem>
                      <Divider />
                    </React.Fragment>
                  ))}
                </List>
              ) : (
                <Alert severity="success" icon={<CheckCircle />}>
                  No active emergencies
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Emergency Tips */}
        <Grid item xs={12}>
          <Card sx={{ borderRadius: 3, bgcolor: 'warning.light' }}>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                🚨 Emergency Tips
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <CheckCircle color="success" />
                    <Typography variant="body2">
                      Stay calm and follow instructions
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <CheckCircle color="success" />
                    <Typography variant="body2">
                      Locate nearest emergency exit
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <CheckCircle color="success" />
                    <Typography variant="body2">
                      Assist others who need help
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <CheckCircle color="success" />
                    <Typography variant="body2">
                      Follow emergency personnel directions
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Report Emergency Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={1}>
            <WarningIcon color="error" />  {/* ✅ Changed */}
            <Typography variant="h6" fontWeight={700}>
              Report Emergency
            </Typography>
          </Box>
        </DialogTitle>
        <DialogContent>
          {submitted ? (
            <Alert severity="success" icon={<CheckCircle />} sx={{ mt: 2 }}>
              Emergency reported successfully! Help is on the way.
            </Alert>
          ) : (
            <Box sx={{ mt: 1 }}>
              <TextField
                select
                fullWidth
                label="Emergency Type"
                value={emergencyType}
                onChange={(e) => setEmergencyType(e.target.value)}
                margin="normal"
              >
                {emergencyTypes.map((type) => (
                  <MenuItem key={type.value} value={type.value}>
                    <Box display="flex" alignItems="center" gap={1}>
                      {type.icon}
                      {type.label}
                    </Box>
                  </MenuItem>
                ))}
              </TextField>

              <TextField
                select
                fullWidth
                label="Location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                margin="normal"
              >
                {locations.map((loc) => (
                  <MenuItem key={loc} value={loc}>{loc}</MenuItem>
                ))}
              </TextField>

              <TextField
                fullWidth
                multiline
                rows={3}
                label="Description"
                placeholder="Please describe the emergency..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                margin="normal"
              />

              <Alert severity="warning" sx={{ mt: 2 }}>
                Only use this for real emergencies. False reports are prohibited.
              </Alert>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>
            Cancel
          </Button>
          <Button
            variant="contained"
            color="error"
            onClick={handleSubmit}
            disabled={!location || !description || submitted}
          >
            Submit Emergency
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Emergency;