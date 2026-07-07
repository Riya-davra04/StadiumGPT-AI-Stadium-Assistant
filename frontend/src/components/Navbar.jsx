import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  Box,
  Tooltip,
  Badge,
  useTheme,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard,
  Map,
  Directions,
  Restaurant,
  Warning as WarningIcon,  // ✅ Changed from Emergency
  AccessibilityNew,
  DirectionsBus,
  AccountCircle,
  Login,
  Logout,
  Notifications,
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const theme = useTheme();
  const location = useLocation();
  const { user, logout, isAuthenticated } = useAuth();
  const [anchorEl, setAnchorEl] = useState(null);
  const [mobileAnchorEl, setMobileAnchorEl] = useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleMobileMenu = (event) => {
    setMobileAnchorEl(event.currentTarget);
  };

  const handleMobileClose = () => {
    setMobileAnchorEl(null);
  };

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <Dashboard /> },
    { path: '/navigation', label: 'Navigation', icon: <Map /> },
    { path: '/crowd-map', label: 'Crowd Map', icon: <Directions /> },
    { path: '/queues', label: 'Queues', icon: <Restaurant /> },
    { path: '/emergency', label: 'Emergency', icon: <WarningIcon /> },  // ✅ Changed
    { path: '/accessibility', label: 'Accessibility', icon: <AccessibilityNew /> },
    { path: '/transport', label: 'Transport', icon: <DirectionsBus /> },
  ];

  return (
    <AppBar position="sticky" elevation={1} sx={{ bgcolor: 'white', color: 'text.primary' }}>
      <Toolbar>
        {/* Logo */}
        <Box display="flex" alignItems="center" flex={1}>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={handleMobileMenu}
            sx={{ display: { xs: 'flex', md: 'none' }, mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            component={Link}
            to="/"
            sx={{
              textDecoration: 'none',
              color: theme.palette.primary.main,
              fontWeight: 800,
              fontSize: '1.25rem',
              '&:hover': { opacity: 0.8 },
            }}
          >
            🏟️ StadiumGPT
          </Typography>
        </Box>

        {/* Desktop Navigation */}
        <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}>
          {navItems.map((item) => (
            <Button
              key={item.path}
              component={Link}
              to={item.path}
              startIcon={item.icon}
              sx={{
                color: location.pathname === item.path ? theme.palette.primary.main : 'text.secondary',
                fontWeight: location.pathname === item.path ? 600 : 400,
                '&:hover': {
                  color: theme.palette.primary.main,
                  bgcolor: 'transparent',
                },
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>

        {/* Right Side */}
        <Box display="flex" alignItems="center" gap={1}>
          <Tooltip title="Notifications">
            <IconButton color="inherit">
              <Badge badgeContent={3} color="error">
                <Notifications />
              </Badge>
            </IconButton>
          </Tooltip>

          {isAuthenticated ? (
            <>
              <Tooltip title={user?.name || 'User'}>
                <IconButton onClick={handleMenu} color="inherit">
                  <Avatar
                    sx={{
                      width: 32,
                      height: 32,
                      bgcolor: theme.palette.primary.main,
                      fontSize: '0.875rem',
                    }}
                  >
                    {user?.name?.[0]?.toUpperCase() || 'U'}
                  </Avatar>
                </IconButton>
              </Tooltip>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
                transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                PaperProps={{
                  sx: {
                    mt: 1.5,
                    minWidth: 200,
                    borderRadius: 2,
                    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                  },
                }}
              >
                <MenuItem sx={{ pointerEvents: 'none', opacity: 0.7 }}>
                  <Box>
                    <Typography variant="subtitle2">{user?.name}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {user?.email}
                    </Typography>
                  </Box>
                </MenuItem>
                <MenuItem onClick={handleClose}>
                  <AccountCircle sx={{ mr: 1 }} /> Profile
                </MenuItem>
                <MenuItem onClick={() => { handleClose(); logout(); }}>
                  <Logout sx={{ mr: 1 }} color="error" /> Logout
                </MenuItem>
              </Menu>
            </>
          ) : (
            <Button
              component={Link}
              to="/login"
              variant="contained"
              size="small"
              startIcon={<Login />}
            >
              Login
            </Button>
          )}
        </Box>
      </Toolbar>

      {/* Mobile Navigation */}
      <Menu
        anchorEl={mobileAnchorEl}
        open={Boolean(mobileAnchorEl)}
        onClose={handleMobileClose}
        PaperProps={{
          sx: {
            width: '100%',
            maxWidth: 300,
            mt: 1,
            borderRadius: 2,
            boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
          },
        }}
      >
        {navItems.map((item) => (
          <MenuItem
            key={item.path}
            component={Link}
            to={item.path}
            onClick={handleMobileClose}
            sx={{
              py: 1.5,
              color: location.pathname === item.path ? theme.palette.primary.main : 'inherit',
              bgcolor: location.pathname === item.path ? 'rgba(25, 118, 210, 0.08)' : 'transparent',
            }}
          >
            <Box display="flex" alignItems="center" gap={2}>
              {item.icon}
              <Typography>{item.label}</Typography>
            </Box>
          </MenuItem>
        ))}
        {!isAuthenticated && (
          <MenuItem component={Link} to="/login" onClick={handleMobileClose}>
            <Login sx={{ mr: 2 }} /> Login
          </MenuItem>
        )}
        {isAuthenticated && (
          <MenuItem onClick={() => { handleMobileClose(); logout(); }} sx={{ color: 'error.main' }}>
            <Logout sx={{ mr: 2 }} /> Logout
          </MenuItem>
        )}
      </Menu>
    </AppBar>
  );
};

export default Navbar;