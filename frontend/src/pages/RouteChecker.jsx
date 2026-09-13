// frontend/src/pages/RouteChecker.jsx

import React, { useState } from 'react'

// Backend API URL
const API_BASE_URL = 'http://127.0.0.1:8000'

// Location presets
const LOCATION_PRESETS = {
  'Wayanad Pass': {
    latitude: 11.6050,
    longitude: 76.0830,
  },

  Kalpetta: {
    latitude: 11.6080,
    longitude: 76.0780,
  },

  'Munnar Gap Road': {
    latitude: 10.0889,
    longitude: 77.0595,
  },
}

function RouteChecker() {
  const [from, setFrom] = useState('Wayanad Pass')
  const [to, setTo] = useState('Kalpetta')

  const [originCoords, setOriginCoords] = useState(
    LOCATION_PRESETS['Wayanad Pass']
  )

  const [destCoords, setDestCoords] = useState(
    LOCATION_PRESETS.Kalpetta
  )

  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Handle origin location
  const handleFromChange = (value) => {
    setFrom(value)

    if (LOCATION_PRESETS[value]) {
      setOriginCoords(LOCATION_PRESETS[value])
    }
  }

  // Handle destination location
  const handleToChange = (value) => {
    setTo(value)

    if (LOCATION_PRESETS[value]) {
      setDestCoords(LOCATION_PRESETS[value])
    }
  }

  // Check route safety
  const checkRoute = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    const originLatitude = Number(originCoords.latitude)
    const originLongitude = Number(originCoords.longitude)

    const destinationLatitude = Number(destCoords.latitude)
    const destinationLongitude = Number(destCoords.longitude)

    // Validate coordinates
    if (
      !Number.isFinite(originLatitude) ||
      !Number.isFinite(originLongitude) ||
      !Number.isFinite(destinationLatitude) ||
      !Number.isFinite(destinationLongitude)
    ) {
      setError('Please enter valid latitude and longitude values.')
      setLoading(false)
      return
    }

    if (
      originLatitude < -90 ||
      originLatitude > 90 ||
      destinationLatitude < -90 ||
      destinationLatitude > 90 ||
      originLongitude < -180 ||
      originLongitude > 180 ||
      destinationLongitude < -180 ||
      destinationLongitude > 180
    ) {
      setError('Please enter valid geographic coordinates.')
      setLoading(false)
      return
    }

    const payload = {
      origin: {
        latitude: originLatitude,
        longitude: originLongitude,
      },
      destination: {
        latitude: destinationLatitude,
        longitude: destinationLongitude,
      },
    }

    try {
      console.log('Sending route request:', payload)

      const response = await fetch(
        `${API_BASE_URL}/api/v1/routes/analyze`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
          body: JSON.stringify(payload),
        }
      )

      const responseText = await response.text()

      let data = null

      try {
        data = responseText ? JSON.parse(responseText) : null
      } catch {
        data = null
      }

      // Handle backend errors
      if (!response.ok) {
        const backendMessage =
          data?.detail ||
          data?.message ||
          responseText ||
          'Unknown backend error'

        throw new Error(
          `Backend error ${response.status}: ${backendMessage}`
        )
      }

      if (!data) {
        throw new Error('Backend returned an empty response.')
      }

      console.log('Route safety response:', data)

      setResult(data)
    } catch (err) {
      console.error('Route safety request failed:', err)

      if (err instanceof TypeError) {
        setError(
          'Cannot connect to the backend. Please check whether the FastAPI server is running on port 8000.'
        )
      } else {
        setError(
          err.message || 'Error communicating with the backend server.'
        )
      }
    } finally {
      setLoading(false)
    }
  }

  // Get badge background color
  const getRiskBadgeColor = (level) => {
    switch (String(level || '').toUpperCase()) {
      case 'CRITICAL':
        return '#EF4444'

      case 'HIGH':
        return '#F97316'

      case 'MEDIUM':
      case 'MODERATE':
        return '#EAB308'

      case 'LOW':
      case 'SAFE':
        return '#10B981'

      default:
        return '#64748B'
    }
  }

  return (
    <div
      style={{
        padding: '40px',
        fontFamily: 'Segoe UI, sans-serif',
        backgroundColor: '#F8FAFC',
        minHeight: '100vh',
      }}
    >
      <h1
        style={{
          color: '#0F172A',
          marginTop: 0,
          marginBottom: '25px',
        }}
      >
        Route Risk Checker
      </h1>

      {/* FORM */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
          maxWidth: '450px',
        }}
      >
        {/* ORIGIN */}
        <div>
          <label
            style={{
              display: 'block',
              fontWeight: 600,
              marginBottom: '6px',
            }}
          >
            Origin Location / Lat & Lng
          </label>

          <input
            type="text"
            placeholder="Origin Name"
            value={from}
            onChange={(e) => handleFromChange(e.target.value)}
            style={inputStyle}
          />

          <div style={coordinateRowStyle}>
            <input
              type="number"
              step="any"
              placeholder="Latitude"
              value={originCoords.latitude}
              onChange={(e) =>
                setOriginCoords({
                  ...originCoords,
                  latitude: e.target.value,
                })
              }
              style={coordinateInputStyle}
            />

            <input
              type="number"
              step="any"
              placeholder="Longitude"
              value={originCoords.longitude}
              onChange={(e) =>
                setOriginCoords({
                  ...originCoords,
                  longitude: e.target.value,
                })
              }
              style={coordinateInputStyle}
            />
          </div>
        </div>

        {/* DESTINATION */}
        <div>
          <label
            style={{
              display: 'block',
              fontWeight: 600,
              marginBottom: '6px',
            }}
          >
            Destination Location / Lat & Lng
          </label>

          <input
            type="text"
            placeholder="Destination Name"
            value={to}
            onChange={(e) => handleToChange(e.target.value)}
            style={inputStyle}
          />

          <div style={coordinateRowStyle}>
            <input
              type="number"
              step="any"
              placeholder="Latitude"
              value={destCoords.latitude}
              onChange={(e) =>
                setDestCoords({
                  ...destCoords,
                  latitude: e.target.value,
                })
              }
              style={coordinateInputStyle}
            />

            <input
              type="number"
              step="any"
              placeholder="Longitude"
              value={destCoords.longitude}
              onChange={(e) =>
                setDestCoords({
                  ...destCoords,
                  longitude: e.target.value,
                })
              }
              style={coordinateInputStyle}
            />
          </div>
        </div>

        {/* BUTTON */}
        <button
          onClick={checkRoute}
          disabled={loading}
          style={{
            padding: '12px',
            fontSize: '16px',
            backgroundColor: loading ? '#64748B' : '#1B3A2B',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontWeight: 600,
          }}
        >
          {loading
            ? 'Evaluating Spatial Risk...'
            : 'Check Route Safety'}
        </button>
      </div>

      {/* ERROR */}
      {error && (
        <div
          style={{
            marginTop: '20px',
            padding: '14px',
            color: '#B91C1C',
            backgroundColor: '#FEF2F2',
            border: '1px solid #FECACA',
            borderRadius: '6px',
            maxWidth: '550px',
          }}
        >
          <strong>Error:</strong>
          <div style={{ marginTop: '6px' }}>{error}</div>
        </div>
      )}

      {/* RESULT */}
      {result && (
        <div
          style={{
            marginTop: '24px',
            padding: '24px',
            backgroundColor: '#FFFFFF',
            border: '1px solid #E2E8F0',
            borderRadius: '8px',
            maxWidth: '550px',
          }}
        >
          <h2
            style={{
              marginTop: 0,
              color: '#0F172A',
              fontSize: '22px',
            }}
          >
            Route Safety Result
          </h2>

          {/* OVERALL ASSESSMENT */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '16px',
            }}
          >
            <span
              style={{
                fontWeight: 600,
                color: '#0F172A',
              }}
            >
              Overall Assessment:
            </span>

            <span
              style={{
                backgroundColor: result.safe
                  ? '#10B981'
                  : getRiskBadgeColor(result.risk_level),
                color: '#FFFFFF',
                padding: '7px 14px',
                borderRadius: '14px',
                fontWeight: 'bold',
                fontSize: '14px',
              }}
            >
              {result.safe ? 'SAFE' : 'UNSAFE'}
            </span>
          </div>

          {/* RISK LEVEL */}
          <p style={resultTextStyle}>
            <strong>Risk Level:</strong>{' '}
            {result.risk_level || 'N/A'}
          </p>

          {/* ROUTE DISTANCE */}
          <p style={resultTextStyle}>
            <strong>Route Distance:</strong>{' '}
            {result.distance_km !== undefined &&
            result.distance_km !== null
              ? `${result.distance_km} km`
              : 'N/A'}
          </p>

          {/* WARNINGS */}
          <div
            style={{
              marginTop: '18px',
              borderTop: '1px solid #E2E8F0',
              paddingTop: '14px',
            }}
          >
            <h3 style={sectionHeadingStyle}>Warnings</h3>

            {Array.isArray(result.warnings) &&
            result.warnings.length > 0 ? (
              <ul style={listStyle}>
                {result.warnings.map((warning, index) => (
                  <li key={index} style={listItemStyle}>
                    {warning}
                  </li>
                ))}
              </ul>
            ) : (
              <p style={resultTextStyle}>
                No warnings detected for this route.
              </p>
            )}
          </div>

          {/* NEARBY HAZARDS */}
          <div
            style={{
              marginTop: '18px',
              borderTop: '1px solid #E2E8F0',
              paddingTop: '14px',
            }}
          >
            <h3 style={sectionHeadingStyle}>
              Nearby Landslide Hazards
            </h3>

            {Array.isArray(result.hazards) &&
            result.hazards.length > 0 ? (
              <ul style={listStyle}>
                {result.hazards.map((hazard, index) => (
                  <li
                    key={hazard.id || index}
                    style={listItemStyle}
                  >
                    <strong>
                      {hazard.location || 'Unknown location'}
                    </strong>

                    <br />

                    Risk Level:{' '}
                    {hazard.risk_level || 'Unknown'}

                    <br />

                    Distance from origin:{' '}
                    {hazard.distance_from_origin_km !== undefined
                      ? `${hazard.distance_from_origin_km} km`
                      : 'N/A'}
                  </li>
                ))}
              </ul>
            ) : (
              <p style={resultTextStyle}>
                No nearby landslide hazards found.
              </p>
            )}
          </div>

          {/* API RESPONSE */}
          <details style={{ marginTop: '18px' }}>
            <summary
              style={{
                cursor: 'pointer',
                color: '#475569',
                fontSize: '13px',
              }}
            >
              View API Response
            </summary>

            <pre
              style={{
                marginTop: '10px',
                padding: '12px',
                backgroundColor: '#F1F5F9',
                borderRadius: '4px',
                overflowX: 'auto',
                fontSize: '12px',
              }}
            >
              {JSON.stringify(result, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  )
}

// Styles
const inputStyle = {
  padding: '10px',
  fontSize: '15px',
  borderRadius: '4px',
  border: '1px solid #CBD5E1',
  width: '100%',
  boxSizing: 'border-box',
  marginBottom: '6px',
}

const coordinateRowStyle = {
  display: 'flex',
  gap: '8px',
}

const coordinateInputStyle = {
  padding: '8px',
  fontSize: '14px',
  borderRadius: '4px',
  border: '1px solid #CBD5E1',
  flex: 1,
  minWidth: 0,
}

const resultTextStyle = {
  margin: '8px 0',
  color: '#334155',
}

const sectionHeadingStyle = {
  margin: '0 0 8px',
  color: '#0F172A',
  fontSize: '17px',
}

const listStyle = {
  paddingLeft: '20px',
  marginTop: '8px',
  color: '#475569',
}

const listItemStyle = {
  marginBottom: '10px',
}

export default RouteChecker