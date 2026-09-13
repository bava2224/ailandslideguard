// frontend/src/pages/RiskMap.jsx
import React, { useEffect, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { fetchLandslides } from '../services/api'

// Resolve Leaflet marker icon asset paths within Vite build
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

const FALLBACK_ZONES = [
  { id: 1, location: 'Zone A - Shillong Hills', risk_level: 'High', latitude: 25.5788, longitude: 91.8933, rainfall: 110.5, soil_moisture: 0.78 },
  { id: 2, location: 'Zone B - Kohima Slopes', risk_level: 'Critical', latitude: 25.6751, longitude: 94.1086, rainfall: 145.0, soil_moisture: 0.89 },
  { id: 3, location: 'Zone C - Itanagar Ridge', risk_level: 'Moderate', latitude: 27.0844, longitude: 93.6053, rainfall: 62.0, soil_moisture: 0.55 },
  { id: 4, location: 'Zone D - Aizawl Basin', risk_level: 'Low', latitude: 23.7271, longitude: 92.7176, rainfall: 18.2, soil_moisture: 0.32 },
]

export default function RiskMap() {
  const [landslides, setLandslides] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLandslides()
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setLandslides(data)
        } else {
          setLandslides(FALLBACK_ZONES)
        }
      })
      .catch((err) => {
        console.warn('Backend unavailable, rendering demo risk map markers:', err)
        setLandslides(FALLBACK_ZONES)
      })
      .finally(() => setLoading(false))
  }, [])

  const getRiskColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'critical': return '#c0392b'
      case 'high': return '#e07b39'
      case 'moderate': return '#e5c100'
      case 'low': return '#4a934a'
      default: return '#6b7280'
    }
  }

  // Map center defaults to North East India center coordinates
  const mapCenter = [25.5788, 91.8933]

  return (
    <div style={{ padding: '30px', fontFamily: 'Segoe UI, sans-serif' }}>
      <h1 style={{ color: '#0F172A', marginTop: 0 }}>Spatial Risk Map</h1>
      <p style={{ color: '#475569', marginBottom: '20px' }}>
        Current landslide risk zones tracked across monitored sectors:
      </p>

      {loading ? (
        <p>Loading interactive map elements...</p>
      ) : (
        <div style={{ height: '550px', width: '100%', borderRadius: '12px', overflow: 'hidden', boxShadow: '0 4px 12px rgba(0,0,0,0.15)' }}>
          <MapContainer center={mapCenter} zoom={7} style={{ height: '100%', width: '100%' }}>
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {landslides.map((item, idx) => {
              const lat = parseFloat(item.latitude)
              const lng = parseFloat(item.longitude)

              if (isNaN(lat) || isNaN(lng)) return null

              const riskColor = getRiskColor(item.risk_level)
              const name = item.location || item.name || `Sector ${idx + 1}`

              return (
                <React.Fragment key={item.id || idx}>
                  <Marker position={[lat, lng]}>
                    <Popup>
                      <div style={{ padding: '4px', minWidth: '160px' }}>
                        <h4 style={{ margin: '0 0 6px 0', color: '#0F172A' }}>{name}</h4>
                        <p style={{ margin: '3px 0', fontSize: '13px' }}>
                          <strong>Risk Level:</strong> <span style={{ color: riskColor, fontWeight: 'bold' }}>{item.risk_level}</span>
                        </p>
                        {item.rainfall !== undefined && (
                          <p style={{ margin: '3px 0', fontSize: '13px' }}><strong>Rainfall:</strong> {item.rainfall} mm</p>
                        )}
                        {item.soil_moisture !== undefined && (
                          <p style={{ margin: '3px 0', fontSize: '13px' }}><strong>Soil Moisture:</strong> {item.soil_moisture}</p>
                        )}
                      </div>
                    </Popup>
                  </Marker>
                  <Circle
                    center={[lat, lng]}
                    radius={50000}
                    pathOptions={{
                      color: riskColor,
                      fillColor: riskColor,
                      fillOpacity: 0.25
                    }}
                  />
                </React.Fragment>
              )
            })}
          </MapContainer>
        </div>
      )}
    </div>
  )
}