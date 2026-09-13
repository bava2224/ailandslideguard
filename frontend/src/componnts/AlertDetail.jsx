import React, { useState, useEffect } from "react";

export default function AlertDetail({ alertId }) {
  const [alert, setAlert] = useState(null);
  const [errorDetail, setErrorDetail] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlertDetail = async () => {
      setLoading(true);
      setErrorDetail(null);

      try {
        const res = await fetch(`http://localhost:8000/api/v1/alerts/${alertId}`);
        
        if (!res.ok) {
          // Parse the error payload returned by FastAPI
          const errorData = await res.json();
          throw new Error(errorData.detail || "Failed to fetch record");
        }

        const data = await res.json();
        setAlert(data);
      } catch (err) {
        setErrorDetail(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (alertId) fetchAlertDetail();
  }, [alertId]);

  if (loading) return <p>Loading details...</p>;

  // Pretty printed 404 / Error State
  if (errorDetail) {
    return (
      <div style={{
        padding: "16px",
        borderRadius: "8px",
        backgroundColor: "#FEF2F2",
        border: "1px solid #FCA5A5",
        color: "#991B1B",
        maxWidth: "400px",
        marginTop: "12px"
      }}>
        <h4 style={{ margin: "0 0 8px 0" }}>⚠️ Resource Error</h4>
        <p style={{ margin: 0 }}>{errorDetail}</p>
      </div>
    );
  }

  return (
    <div>
      <h3>{alert.title}</h3>
      <p>{alert.message}</p>
    </div>
  );
}