// frontend/src/pages/RouteChecker.jsx
import React, { useState } from 'react'

const LOCATION_PRESETS = {
  'Wayanad Pass': { latitude: 11.6050, longitude: 76.0830 },
  'Kalpetta': { latitude: 11.6080, longitude: 76.0780 },
  'Munnar Gap Road': { latitude: 10.0889, longitude: 77.0595 }
}

function RouteChecker() {
  const [from, setFrom] = useState('Wayanad Pass')
  const [to, setTo] = useState('Kalpetta')
  
  // Latitude/Longitude state
  const [originCoords, setOriginCoords] = useState(LOCATION_PRESETS['Wayanad Pass'])
  const [destCoords, setDestCoords] = useState(LOCATION_PRESETS['Kalpetta'])
  
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFromChange = (value) => {
    setFrom(value)
    if (LOCATION_PRESETS[value]) {
      setOriginCoords(LOCATION_PRESETS[value])
    }
  }

  const handleToChange = (value) => {
    setTo(value)
    if (LOCATION_PRESETS[value]) {
      setDestCoords(LOCATION_PRESETS[value])
    }
  }

  const checkRoute = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    const payload = {
      origin: {
        latitude: parseFloat(originCoords.latitude),
        longitude: parseFloat(originCoords.longitude)
      },
      destination: {
        latitude: parseFloat(destCoords.latitude),
        longitude: parseFloat(destCoords.longitude)
      }
    }

    try {
      const response = await fetch('/api/v1/routes/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!response.ok) throw new Error('Failed to evaluate route safety')

      const data = await response.json()
      setResult(data)
    } catch (err) {
      console.warn('Backend unavailable or request failed:', err)
      setError(err.message || 'Error communicating with backend server.')
    } finally {
      setLoading(false)
    }
  }

  const getRiskBadgeColor = (level) => {
    switch (level?.toUpperCase()) {
      case 'CRITICAL': return '#EF4444'
      case 'HIGH': return '#F97316'
      case 'MODERATE': return '#EAB308'
      default: return '#10B981'
    }
  }

  return (
    <div style={{ padding: '40px', fontFamily: 'Segoe UI, sans-serif' }}>
      <h1 style={{ color: '#0F172A', marginTop: 0 }}>Route Risk Checker</h1>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxWidth: '450px' }}>
        <div>
          <label style={{ display: 'block', fontWeight: 600, marginBottom: '4px' }}>Origin Location / Lat & Lng</label>
          <input
            type="text"
            placeholder="Origin Name (e.g., Wayanad Pass)"
            value={from}
            onChange={(e) => handleFromChange(e.target.value)}
            style={{ padding: '10px', fontSize: '15px', borderRadius: '4px', border: '1px solid #CBD5E1', width: '100%', marginBottom: '6px' }}
          />
          <div style={{ display: 'flex', gap: '8px' }}>
            <input
              type="number" step="any" placeholder="Lat"
              value={originCoords.latitude}
              onChange={(e) => setOriginCoords({ ...originCoords, latitude: e.target.value })}
              style={{ padding: '8px', fontSize: '14px', borderRadius: '4px', border: '1px solid #CBD5E1', flex: 1 }}
            />
            <input
              type="number" step="any" placeholder="Lng"
              value={originCoords.longitude}
              onChange={(e) => setOriginCoords({ ...originCoords, longitude: e.target.value })}
              style={{ padding: '8px', fontSize: '14px', borderRadius: '4px', border: '1px solid #CBD5E1', flex: 1 }}
            />
          </div>
        </div>

        <div>
          <label style={{ display: 'block', fontWeight: 600, marginBottom: '4px' }}>Destination Location / Lat & Lng</label>
          <input
            type="text"
            placeholder="Destination Name (e.g., Kalpetta)"
            value={to}
            onChange={(e) => handleToChange(e.target.value)}
            style={{ padding: '10px', fontSize: '15px', borderRadius: '4px', border: '1px solid #CBD5E1', width: '100%', marginBottom: '6px' }}
          />
          <div style={{ display: 'flex', gap: '8px' }}>
            <input
              type="number" step="any" placeholder="Lat"
              value={destCoords.latitude}
              onChange={(e) => setDestCoords({ ...destCoords, latitude: e.target.value })}
              style={{ padding: '8px', fontSize: '14px', borderRadius: '4px', border: '1px solid #CBD5E1', flex: 1 }}
            />
            <input
              type="number" step="any" placeholder="Lng"
              value={destCoords.longitude}
              onChange={(e) => setDestCoords({ ...destCoords, longitude: e.target.value })}
              style={{ padding: '8px', fontSize: '14px', borderRadius: '4px', border: '1px solid #CBD5E1', flex: 1 }}
            />
          </div>
        </div>

        <button
          onClick={checkRoute}
          disabled={loading}
          style={{
            padding: '12px',
            fontSize: '16px',
            backgroundColor: '#1b3a2b',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontWeight: 500,
          }}
        >
          {loading ? 'Evaluating Spatial Risk...' : 'Check Route Safety'}
        </button>
      </div>

      {error && (
        <div style={{ marginTop: '20px', color: '#DC2626', maxWidth: '450px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: '24px', padding: '20px', backgroundColor: '#F8FAFC', border: '1px solid #E2E8F0', borderRadius: '8px', maxWidth: '450px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <span style={{ fontWeight: 600, color: '#0F172A' }}>Overall Assessment:</span>
            <span style={{
              backgroundColor: getRiskBadgeColor(result.risk_level),
              color: '#FFFFFF',
              padding: '4px 12px',
              borderRadius: '12px',
              fontWeight: 'bold',
              fontSize: '14px'
            }}>
              {result.risk_level}
            </span>
          </div>

          <p style={{ margin: '4px 0', color: '#334155' }}><strong>Risk Score:</strong> {result.risk_score}</p>
          <p style={{ margin: '4px 0', color: '#334155' }}><strong>Exposed Path:</strong> {result.exposed_percentage}%</p>
          <p style={{ marginTop: '12px', color: '#1E293B', fontStyle: 'italic' }}>{result.recommendation}</p>

          {result.dangerous_segments?.length > 0 && (
            <div style={{ marginTop: '16px', borderTop: '1px solid #E2E8F0', paddingTop: '12px' }}>
              <strong style={{ color: '#0F172A' }}>Active Hazard Zones Nearby:</strong>
              <ul style={{ paddingLeft: '20px', margin: '8px 0 0 0', color: '#475569' }}>
                {result.dangerous_segments.map((seg, idx) => (
                  <li key={idx}>
                    {seg.location || seg.segment_id} ({seg.distance_km} km away) — <strong>{seg.risk_level}</strong>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default RouteChecker