// frontend/src/app.jsx

import React, { useEffect, useState } from 'react'
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
} from 'react-router-dom'

import Home from './pages/Home.jsx'
import RiskMap from './pages/RiskMap.jsx'
import RouteChecker from './pages/RouteChecker.jsx'

const API_BASE_URL = 'http://127.0.0.1:8000'

// Reports page
function ReportsPage() {
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/v1/reports`)
      .then(async (response) => {
        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.detail || 'Failed to load reports')
        }

        return data
      })
      .then((data) => {
        setReports(Array.isArray(data) ? data : [])
      })
      .catch((err) => {
        setError(err.message)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  return (
    <div style={pageStyle}>
      <h1>Reports</h1>

      {loading && <p>Loading reports...</p>}

      {error && (
        <p style={errorStyle}>
          Error: {error}
        </p>
      )}

      {!loading && !error && reports.length === 0 && (
        <p>No reports available.</p>
      )}

      {!loading &&
        !error &&
        reports.map((report) => (
          <div key={report.id} style={cardStyle}>
            <h2>Report #{report.id}</h2>

            <p>
              <strong>Location:</strong>{' '}
              {report.location ?? 'N/A'}
            </p>

            <p>
              <strong>Description:</strong>{' '}
              {report.description ?? 'N/A'}
            </p>

            <p>
              <strong>Severity:</strong>{' '}
              {report.severity ?? 'N/A'}
            </p>

            <p>
              <strong>Status:</strong>{' '}
              {report.status ?? 'N/A'}
            </p>

            <p>
              <strong>Created At:</strong>{' '}
              {report.created_at ?? 'N/A'}
            </p>
          </div>
        ))}
    </div>
  )
}

// Alerts page
function AlertsPage() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/v1/alerts`)
      .then(async (response) => {
        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.detail || 'Failed to load alerts')
        }

        return data
      })
      .then((data) => {
        setAlerts(Array.isArray(data) ? data : [])
      })
      .catch((err) => {
        setError(err.message)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  return (
    <div style={pageStyle}>
      <h1>Landslide Alerts</h1>

      {loading && <p>Loading alerts...</p>}

      {error && (
        <p style={errorStyle}>
          Error: {error}
        </p>
      )}

      {!loading && !error && alerts.length === 0 && (
        <p>No alerts available.</p>
      )}

      {!loading &&
        !error &&
        alerts.map((alert) => (
          <div key={alert.id} style={cardStyle}>
            <h2>Alert #{alert.id}</h2>

            <p>
              <strong>Location:</strong>{' '}
              {alert.location ?? 'N/A'}
            </p>

            <p>
              <strong>Severity:</strong>{' '}
              {alert.severity ?? alert.risk_level ?? 'N/A'}
            </p>

            <p>
              <strong>Message:</strong>{' '}
              {alert.message ?? alert.description ?? 'N/A'}
            </p>

            <p>
              <strong>Status:</strong>{' '}
              {alert.status ?? 'N/A'}
            </p>

            <p>
              <strong>Created At:</strong>{' '}
              {alert.created_at ?? 'N/A'}
            </p>
          </div>
        ))}
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <header>
        <nav style={navStyle}>
          <span style={logoStyle}>
            🏔️ LandslideGuard AI
          </span>

          <Link to="/" style={linkStyle}>
            Home
          </Link>

          <Link to="/risk-map" style={linkStyle}>
            Risk Map
          </Link>

          <Link to="/route-checker" style={linkStyle}>
            Route Checker
          </Link>

          <Link to="/alerts" style={linkStyle}>
            Alerts
          </Link>

          <Link to="/reports" style={linkStyle}>
            Reports
          </Link>
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<Home />} />

          <Route
            path="/risk-map"
            element={<RiskMap />}
          />

          <Route
            path="/route-checker"
            element={<RouteChecker />}
          />

          <Route
            path="/alerts"
            element={<AlertsPage />}
          />

          <Route
            path="/reports"
            element={<ReportsPage />}
          />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

const navStyle = {
  display: 'flex',
  gap: '24px',
  padding: '16px 24px',
  backgroundColor: '#1b3a2b',
  alignItems: 'center',
  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  flexWrap: 'wrap',
}

const logoStyle = {
  color: '#4ADE80',
  fontWeight: 'bold',
  fontSize: '1.2rem',
  marginRight: '12px',
}

const linkStyle = {
  color: 'white',
  textDecoration: 'none',
  fontWeight: 500,
}

const pageStyle = {
  padding: '32px',
  minHeight: '100vh',
  backgroundColor: '#f8fafc',
  fontFamily: 'Arial, sans-serif',
}

const cardStyle = {
  backgroundColor: 'white',
  border: '1px solid #dbe3ea',
  borderRadius: '8px',
  padding: '20px',
  marginBottom: '16px',
  maxWidth: '650px',
}

const errorStyle = {
  color: '#b91c1c',
  backgroundColor: '#fee2e2',
  padding: '12px',
  borderRadius: '6px',
}

export default App