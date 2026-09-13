// frontend/src/components/RouteAnalysis.jsx
import React, { useState } from 'react';
import { analyzeRouteRisk } from '../services/api';

export const RouteAnalysis = () => {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Form inputs for testing
  const [originLat, setOriginLat] = useState(11.6000);
  const [originLng, setOriginLng] = useState(76.0800);
  const [destLat, setDestLat] = useState(11.6100);
  const [destLng, setDestLng] = useState(76.0900);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await analyzeRouteRisk(
        parseFloat(originLat),
        parseFloat(originLng),
        parseFloat(destLat),
        parseFloat(destLng)
      );
      setAnalysis(data);
    } catch (err) {
      setError(err.message || 'Error connecting to backend API');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto', color: '#fff' }}>
      <h2>LandslideGuard Route Risk Analysis</h2>
      
      <form onSubmit={handleAnalyze} style={{ display: 'grid', gap: '10px', marginBottom: '20px' }}>
        <div>
          <h4>Origin Coordinates</h4>
          <input 
            type="number" step="any" value={originLat} 
            onChange={(e) => setOriginLat(e.target.value)} 
            placeholder="Origin Latitude" required 
          />
          <input 
            type="number" step="any" value={originLng} 
            onChange={(e) => setOriginLng(e.target.value)} 
            placeholder="Origin Longitude" required 
          />
        </div>

        <div>
          <h4>Destination Coordinates</h4>
          <input 
            type="number" step="any" value={destLat} 
            onChange={(e) => setDestLat(e.target.value)} 
            placeholder="Destination Latitude" required 
          />
          <input 
            type="number" step="any" value={destLng} 
            onChange={(e) => setDestLng(e.target.value)} 
            placeholder="Destination Longitude" required 
          />
        </div>

        <button type="submit" disabled={loading} style={{ padding: '10px', marginTop: '10px' }}>
          {loading ? 'Evaluating Spatial Risk...' : 'Analyze Route'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {analysis && (
        <div style={{ background: '#2a2a2a', padding: '15px', borderRadius: '8px' }}>
          <h3>Risk Level: <span style={{ color: analysis.risk_level === 'CRITICAL' ? 'red' : 'orange' }}>{analysis.risk_level}</span></h3>
          <p><strong>Risk Score:</strong> {analysis.risk_score}</p>
          <p><strong>Exposed Distance:</strong> {analysis.exposed_percentage}%</p>
          <p><strong>Recommendation:</strong> {analysis.recommendation}</p>

          {analysis.dangerous_segments.length > 0 && (
            <div>
              <h4>Nearby Hazard Segments:</h4>
              <ul>
                {analysis.dangerous_segments.map((seg, idx) => (
                  <li key={idx}>
                    <strong>{seg.location || seg.segment_id}</strong> - {seg.distance_km} km away ({seg.risk_level})
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
