import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home.jsx'
import RiskMap from './pages/RiskMap.jsx'
import RouteChecker from './pages/RouteChecker.jsx'

function App() {
  return (
    <BrowserRouter>
      <nav style={{ display: 'flex', gap: '20px', padding: '16px', backgroundColor: '#1b3a2b' }}>
        <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>Home</Link>
        <Link to="/risk-map" style={{ color: 'white', textDecoration: 'none' }}>Risk Map</Link>
        <Link to="/route-checker" style={{ color: 'white', textDecoration: 'none' }}>Route Checker</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/risk-map" element={<RiskMap />} />
        <Route path="/route-checker" element={<RouteChecker />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App