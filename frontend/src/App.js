import React, { useState } from 'react';
import EntitySelector from './components/EntitySelector';
import TimelineView from './components/TimelineView';
import { Container, Typography, CssBaseline } from '@mui/material';

function App() {
  const [selectedEntityId, setSelectedEntityId] = useState(null);

  const handleEntitySelect = (entityId) => {
    setSelectedEntityId(entityId);
  };

  return (
    <>
      <CssBaseline />
      <Container maxWidth="md">
        <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mt: 4 }}>
          Aura: Campus Activity Monitor
        </Typography>
        <EntitySelector onEntitySelect={handleEntitySelect} />
        <TimelineView entityId={selectedEntityId} />
      </Container>
    </>
  );
}

export default App;