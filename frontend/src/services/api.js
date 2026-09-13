// frontend/src/services/api.js
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Fetch all recorded landslide risk points from SQLite database
 */
export const fetchLandslides = async () => {
  const response = await fetch(`${BASE_URL}/api/v1/landslides/`);
  if (!response.ok) {
    throw new Error('Failed to fetch landslide hazard data.');
  }
  return response.json();
};

/**
 * Send spatial route coordinates to FastAPI backend for risk analysis.
 * Accepts either:
 *   - analyzeRouteRisk({ latitude: lat1, longitude: lng1 }, { latitude: lat2, longitude: lng2 })
 *   - analyzeRouteRisk(lat1, lng1, lat2, lng2)
 */
export const analyzeRouteRisk = async (origin, destination, destLat, destLng) => {
  let payload;

  if (typeof origin === 'object' && typeof destination === 'object') {
    payload = { origin, destination };
  } else {
    payload = {
      origin: { latitude: parseFloat(origin), longitude: parseFloat(destination) },
      destination: { latitude: parseFloat(destLat), longitude: parseFloat(destLng) },
    };
  }

  const response = await fetch(`${BASE_URL}/api/v1/routes/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error('Failed to compute route hazard safety analysis.');
  }

  return response.json();
};