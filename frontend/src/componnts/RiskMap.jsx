// frontend/src/pages/RiskMap.jsx
import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

// Fix missing default Leaflet marker icons in Vite build pipeline
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
});

export default function RiskMap() {
  const [alerts, setAlerts] = useState([]);
  const position = [11.6050, 76.0830]; // Default center (Wayanad region)

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/alerts')
      .then((res) => res.json())
      .then((data) => setAlerts(data))
      .catch((err) => console.error("Failed to fetch risk map alerts:", err));
  }, []);

  return (
    <div style={{ height: "calc(100vh - 100px)", width: "100%", padding: "16px", boxSizing: "border-box" }}>
      <h2 style={{ marginTop: 0, color: "#0F172A" }}>🗺️ Spatial Hazard Map</h2>
      <p style={{ color: "#64748B", marginTop: "-8px", marginBottom: "16px" }}>
        Real-time monitoring of active risk zones and automated alerts.
      </p>

      <div style={{ height: "550px", width: "100%", borderRadius: "8px", overflow: "hidden", border: "1px solid #CBD5E1" }}>
        <MapContainer 
          center={position} 
          zoom={11} 
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          {/* Baseline Sector Marker */}
          <Marker position={position}>
            <Popup>
              <b>Wayanad Pass Sector 4</b><br />
              Baseline Risk Score: 85% (High Hazard)
            </Popup>
          </Marker>

          {/* Dynamic FastAPI Alert Markers */}
          {alerts.map((alert, idx) => (
            <Marker key={alert.id || idx} position={[alert.latitude || 11.605, alert.longitude || 76.083]}>
              <Popup>
                <b style={{ color: alert.level === 'CRITICAL' ? '#DC2626' : '#D97706' }}>
                  [{alert.level}] {alert.title}
                </b>
                <br />
                {alert.message}
                <br />
                <small>Risk Level: {((alert.risk_score || 0) * 100).toFixed(0)}%</small>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}