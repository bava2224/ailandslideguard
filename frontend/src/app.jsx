// frontend/src/App.jsx
import React from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home.jsx'
import RiskMap from './pages/RiskMap.jsx'
import RouteChecker from './pages/RouteChecker.jsx'

function App() {
  return (
    <BrowserRouter>
      <header>
        <nav
          style={{
            display: 'flex',
            gap: '24px',
            padding: '16px 24px',
            backgroundColor: '#1b3a2b',
            alignItems: 'center',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}
        >
          <span style={{ color: '#4ADE80', fontWeight: 'bold', fontSize: '1.2rem', marginRight: '12px' }}>
            ⛰️ LandslideGuard AI
          </span>
          <Link to="/" style={{ color: 'white', textDecoration: 'none', fontWeight: 500 }}>
            Home
          </Link>
          <Link to="/risk-map" style={{ color: 'white', textDecoration: 'none', fontWeight: 500 }}>
            Risk Map
          </Link>
          <Link to="/route-checker" style={{ color: 'white', textDecoration: 'none', fontWeight: 500 }}>
            Route Checker
          </Link>
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/risk-map" element={<RiskMap />} />
          <Route path="/route-checker" element={<RouteChecker />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App