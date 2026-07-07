import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Box,
  useTheme,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard,
  Map,
  Directions,
  Restaurant,
  Warning as WarningIcon,
  AccessibilityNew,
  DirectionsBus,
} from '@mui/icons-material';

const Navbar = () => {
  const theme = useTheme();
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <Dashboard />, ariaLabel: 'Go to Dashboard' },
    { path: '/navigation', label: 'Navigation', icon: <Map />, ariaLabel: 'Get Navigation help' },
    { path: '/crowd-map', label: 'Crowd Map', icon: <Directions />, ariaLabel: 'View Crowd Map' },
    { path: '/queues', label: 'Queues', icon: <Restaurant />, ariaLabel: 'Check Queue Status' },
    { path: '/emergency', label: 'Emergency', icon: <WarningIcon />, ariaLabel: 'Emergency Help' },
    { path: '/accessibility', label: 'Accessibility', icon: <AccessibilityNew />, ariaLabel: 'Accessibility Options' },
    { path: '/transport', label: 'Transport', icon: <DirectionsBus />, ariaLabel: 'Transport Options' },
  ];

  return (
    <AppBar 
      position="sticky" 
      elevation={1} 
      sx={{ bgcolor: 'white', color: 'text.primary' }}
      role="banner"
      aria-label="Main navigation"
    >
      <Toolbar>
        <Box display="flex" alignItems="center" flex={1}>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="Open menu"
            sx={{ display: { xs: 'flex', md: 'none' }, mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            component={Link}
            to="/"
            aria-label="StadiumGPT Home"
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

        <Box 
          component="nav"
          sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}
          role="navigation"
          aria-label="Main menu"
        >
          {navItems.map((item) => (
            <Button
              key={item.path}
              component={Link}
              to={item.path}
              aria-label={item.ariaLabel}
              startIcon={item.icon}
              sx={{
                color: location.pathname === item.path ? theme.palette.primary.main : 'text.secondary',
                fontWeight: location.pathname === item.path ? 600 : 400,
                '&:hover': { color: theme.palette.primary.main }
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;