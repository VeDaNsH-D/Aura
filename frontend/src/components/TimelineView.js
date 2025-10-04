import React, { useState, useEffect } from 'react';
import { getTimeline } from '../services/api';
import {
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  CircularProgress,
  Paper,
  Divider,
} from '@mui/material';
import {
  CreditCard as SwipeIcon,
  Wifi as WifiIcon,
  MenuBook as LibraryIcon,
  HelpOutline as UnknownIcon,
} from '@mui/icons-material';

/**
 * Maps an event source type to its corresponding MUI icon.
 * @param {string} sourceType - The source type of the event (e.g., 'swipe', 'wifi').
 * @returns {JSX.Element} A React component for the icon.
 */
const getEventIcon = (sourceType) => {
  switch (sourceType) {
    case 'swipe':
      return <SwipeIcon color="primary" />;
    case 'wifi':
      return <WifiIcon color="secondary" />;
    case 'library':
      return <LibraryIcon sx={{ color: 'success.main' }} />;
    default:
      return <UnknownIcon color="action" />;
  }
};

/**
 * Displays a chronological timeline of events for a given entity.
 * @param {object} props - The component props.
 * @param {number|null} props.entityId - The ID of the entity to display the timeline for.
 */
const TimelineView = ({ entityId }) => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetches timeline data when the entityId prop changes.
    const fetchTimeline = async () => {
      if (!entityId) {
        setEvents([]); // Clear events if no entity is selected
        return;
      }
      try {
        setLoading(true);
        setError(null);
        const data = await getTimeline(entityId);
        setEvents(data);
      } catch (err) {
        setError('Failed to fetch timeline data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTimeline();
  }, [entityId]); // Re-run the effect whenever entityId changes

  if (!entityId) {
    return (
      <Paper elevation={2} sx={{ p: 3, textAlign: 'center', mt: 4 }}>
        <Typography variant="h6" color="text.secondary">
          Please select an entity to view their activity timeline.
        </Typography>
      </Paper>
    );
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" my={4}>
        <CircularProgress />
        <Typography ml={2}>Loading Timeline...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Typography color="error" align="center" my={4}>
        {error}
      </Typography>
    );
  }

  if (events.length === 0) {
    return (
      <Paper elevation={2} sx={{ p: 3, textAlign: 'center', mt: 4 }}>
        <Typography variant="h6" color="text.secondary">
          No activity recorded for the selected entity.
        </Typography>
      </Paper>
    );
  }

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom>
        Activity Timeline
      </Typography>
      <Paper elevation={2}>
        <List>
          {events.map((event, index) => (
            <React.Fragment key={event.id}>
              <ListItem>
                <ListItemIcon>{getEventIcon(event.source_type)}</ListItemIcon>
                <ListItemText
                  primary={event.description}
                  secondary={`${new Date(
                    event.timestamp
                  ).toLocaleString()} - Location: ${event.location}`}
                />
              </ListItem>
              {index < events.length - 1 && <Divider component="li" />}
            </React.Fragment>
          ))}
        </List>
      </Paper>
    </Box>
  );
};

export default TimelineView;