// frontend/src/components/NotificationCenter.jsx
import React, { useState, useEffect } from "react";

const API_BASE_URL = "http://localhost:8000/api/v1/alerts";

export default function NotificationCenter() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch alerts from FastAPI backend
  const fetchAlerts = async () => {
    try {
      const response = await fetch(API_BASE_URL);
      const data = await response.json();
      setAlerts(data);
    } catch (error) {
      console.error("Error loading alerts:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 10000); // Polling every 10 seconds
    return () => clearInterval(interval);
  }, []);

  // Acknowledge alert status update
  const handleAcknowledge = async (id) => {
    try {
      const res = await fetch(`${API_BASE_URL}/${id}/acknowledge`, { method: "PATCH" });
      if (res.ok) fetchAlerts();
    } catch (err) {
      console.error("Acknowledge error:", err);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h2>🚨 Emergency Notifications Dashboard</h2>
      {loading ? (
        <p>Loading active alerts...</p>
      ) : alerts.length === 0 ? (
        <p>No active alerts reported.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {alerts.map((alert) => (
            <li
              key={alert.id}
              style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "15px",
                marginBottom: "10px",
                backgroundColor: alert.level === "CRITICAL" ? "#FFE6E6" : "#FFF9E6"
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <strong style={{ color: alert.level === "CRITICAL" ? "#D32F2F" : "#D97706" }}>
                  [{alert.level}] {alert.title}
                </strong>
                <span>Status: <b>{alert.status}</b></span>
              </div>
              <p>{alert.message}</p>
              <small>
                Location: {alert.latitude}, {alert.longitude} | Risk: {alert.risk_score * 100}%
              </small>
              <br />
              {alert.status === "ACTIVE" && (
                <button
                  onClick={() => handleAcknowledge(alert.id)}
                  style={{
                    marginTop: "10px",
                    padding: "6px 12px",
                    backgroundColor: "#1D4ED8",
                    color: "white",
                    border: "none",
                    borderRadius: "4px",
                    cursor: "pointer"
                  }}
                >
                  Acknowledge Alert
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}