import React, { useState, useEffect } from 'react';
import {
  Paper,
  Typography,
  Box,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  CircularProgress,
  Alert as MuiAlert,
} from '@mui/material';
import {
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  Notifications as NotificationsIcon,
} from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';

// Helper to select an icon based on severity
const getSeverityIcon = (severity) => {
  switch (severity.toLowerCase()) {
    case 'high':
    case 'critical':
      return <ErrorIcon color="error" />;
    case 'medium':
      return <WarningIcon color="warning" />;
    case 'low':
    default:
      return <InfoIcon color="info" />;
  }
};

// Helper to determine the color for the severity chip
const getSeverityChipColor = (severity) => {
  switch (severity.toLowerCase()) {
    case 'high':
    case 'critical':
      return 'error';
    case 'medium':
      return 'warning';
    case 'low':
    default:
      return 'info';
  }
};

function AlertsPanel() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        setLoading(true);
        // The endpoint is proxied by the development server (see package.json)
        const response = await fetch('/api/alert/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setAlerts(data.alerts);
      } catch (e) {
        setError(e.message);
        console.error("Failed to fetch alerts:", e);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, []); // Empty dependency array means this effect runs once on mount

  const renderContent = () => {
    if (loading) {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '150px' }}>
          <CircularProgress />
        </Box>
      );
    }

    if (error) {
      return (
        <MuiAlert severity="error" sx={{ mt: 2 }}>
          Failed to load alerts. Please try again later.
        </MuiAlert>
      );
    }

    if (alerts.length === 0) {
      return (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'text.secondary',
            minHeight: '150px',
          }}
        >
          <NotificationsIcon sx={{ fontSize: 40, mb: 1 }} />
          <Typography>No new alerts have been triggered.</Typography>
        </Box>
      );
    }

    return (
      <List dense>
        {alerts.map((alert) => (
          <ListItem key={alert.id} divider>
            <ListItemIcon sx={{ minWidth: 40 }}>
              {getSeverityIcon(alert.severity)}
            </ListItemIcon>
            <ListItemText
              primary={alert.message}
              secondary={`Triggered ${formatDistanceToNow(new Date(alert.timestamp))} ago for ${alert.entity_name}`}
            />
            <Chip
              label={alert.severity}
              color={getSeverityChipColor(alert.severity)}
              size="small"
              sx={{ ml: 1 }}
            />
          </ListItem>
        ))}
      </List>
    );
  };

  return (
    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', borderRadius: 2, maxHeight: '40vh', overflow: 'auto' }}>
      <Typography variant="h6" gutterBottom>
        Recent Alerts
      </Typography>
      {renderContent()}
    </Paper>
  );
}

export default AlertsPanel;