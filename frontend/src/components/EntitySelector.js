import React, { useState, useEffect } from 'react';
import { getEntities } from '../services/api';
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Box,
  Typography,
} from '@mui/material';

/**
 * A dropdown component to select a campus entity.
 * It fetches the list of entities from the API on mount.
 * @param {object} props - The component props.
 * @param {function(number|null)} props.onEntitySelect - Callback function invoked with the selected entity's ID.
 */
const EntitySelector = ({ onEntitySelect }) => {
  const [entities, setEntities] = useState([]);
  const [selectedEntity, setSelectedEntity] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch entities when the component mounts
    const fetchEntities = async () => {
      try {
        setLoading(true);
        const data = await getEntities();
        setEntities(data);
        setError(null);
      } catch (err) {
        setError('Failed to load entities. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchEntities();
  }, []); // Empty dependency array ensures this runs only once on mount

  const handleChange = (event) => {
    const entityId = event.target.value;
    setSelectedEntity(entityId);
    // Call the parent component's handler function
    if (onEntitySelect) {
      onEntitySelect(entityId);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" my={4}>
        <CircularProgress />
        <Typography ml={2}>Loading Entities...</Typography>
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

  return (
    <FormControl fullWidth variant="outlined" sx={{ my: 2 }}>
      <InputLabel id="entity-select-label">Select an Entity</InputLabel>
      <Select
        labelId="entity-select-label"
        id="entity-select"
        value={selectedEntity}
        label="Select an Entity"
        onChange={handleChange}
      >
        <MenuItem value="">
          <em>None</em>
        </MenuItem>
        {entities.map((entity) => (
          <MenuItem key={entity.id} value={entity.id}>
            {entity.name} ({entity.entity_type})
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default EntitySelector;