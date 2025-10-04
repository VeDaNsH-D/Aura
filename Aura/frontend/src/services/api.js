import axios from 'axios';

// Create an Axios instance with a base URL.
// The URL can be configured via an environment variable for flexibility.
// In a Create React App project, this would be REACT_APP_API_BASE_URL in a .env file.
// The fallback '/api' is useful when using a proxy during development.
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || '/api',
});

/**
 * Fetches a list of all entities from the backend.
 * @returns {Promise<Array>} A promise that resolves to an array of entities.
 * @throws {Error} Throws an error if the API request fails.
 */
export const getEntities = async () => {
  try {
    const response = await api.get('/entities');
    // The data is nested under the 'entities' key as defined by our marshal_list_with envelope
    return response.data.entities || [];
  } catch (error) {
    console.error('Error fetching entities:', error);
    // You could also handle different error types (e.g., network error vs. server error)
    throw error;
  }
};

/**
 * Fetches the event timeline for a specific entity.
 * @param {number} entityId - The ID of the entity whose timeline to fetch.
 * @returns {Promise<Array>} A promise that resolves to an array of events.
 * @throws {Error} Throws an error if the API request fails.
 */
export const getTimeline = async (entityId) => {
  if (!entityId) {
    // Return an empty array if no entityId is provided to prevent unnecessary API calls.
    return [];
  }
  try {
    const response = await api.get(`/timeline/${entityId}`);
    // The data is nested under the 'events' key
    return response.data.events || [];
  } catch (error) {
    console.error(`Error fetching timeline for entity ${entityId}:`, error);
    throw error;
  }
};
