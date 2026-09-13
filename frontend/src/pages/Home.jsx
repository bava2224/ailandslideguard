// frontend/src/pages/Home.jsx
import React, { useEffect, useState } from 'react'
import { fetchLandslides } from '../services/api'

function Home() {
  const [stats, setStats] = useState({
    totalZones: 0,
    highRiskCount: 0,
    systemStatus: 'Operational'
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLandslides()
      .then((data) => {
        if (Array.isArray(data)) {
          const highRisk = data.filter(
            (item) => item.risk_level?.toLowerCase() === 'high' || item.risk_level?.toLowerCase() === 'critical'
          ).length

          setStats({
            totalZones: data.length,
            highRiskCount: highRisk,
            systemStatus: 'Operational'
          })
        }
      })
      .catch((err) => {
        console.warn('Backend unavailable, rendering sample status:', err)
        setStats({ totalZones: 4, highRiskCount: 2, systemStatus: 'Demo Mode' })
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <div style={{ padding: '40px', textAlign: 'center', fontFamily: 'Segoe UI, sans-serif', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ color: '#0F172A', fontSize: '2.5rem', marginBottom: '16px' }}>LandslideGuard AI</h1>
      <p style={{ color: '#475569', fontSize: '1.2rem', lineHeight: '1.6', marginBottom: '12px' }}>
        An early-warning and travel-safety platform for landslide-prone regions
        in North East India.
      </p>
      <p style={{ color: '#64748B', fontSize: '1rem', marginBottom: '32px' }}>
        Use the navigation above to check the live risk map or test a route
        for landslide risk.
      </p>

      {/* Dynamic Status Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginTop: '20px' }}>
        <div style={{ padding: '20px', borderRadius: '8px', backgroundColor: '#F8FAFC', border: '1px solid #E2E8F0' }}>
          <span style={{ fontSize: '12px', color: '#64748B', fontWeight: 600 }}>SYSTEM STATUS</span>
          <h3 style={{ color: stats.systemStatus === 'Operational' ? '#10B981' : '#F59E0B', margin: '8px 0 0 0' }}>
            {loading ? 'Connecting...' : stats.systemStatus}
          </h3>
        </div>

        <div style={{ padding: '20px', borderRadius: '8px', backgroundColor: '#F8FAFC', border: '1px solid #E2E8F0' }}>
          <span style={{ fontSize: '12px', color: '#64748B', fontWeight: 600 }}>MONITORED SECTORS</span>
          <h3 style={{ color: '#0F172A', margin: '8px 0 0 0' }}>
            {loading ? '-' : stats.totalZones}
          </h3>
        </div>

        <div style={{ padding: '20px', borderRadius: '8px', backgroundColor: '#F8FAFC', border: '1px solid #E2E8F0' }}>
          <span style={{ fontSize: '12px', color: '#64748B', fontWeight: 600 }}>CRITICAL / HIGH RISKS</span>
          <h3 style={{ color: stats.highRiskCount > 0 ? '#EF4444' : '#10B981', margin: '8px 0 0 0' }}>
            {loading ? '-' : stats.highRiskCount}
          </h3>
        </div>
      </div>
    </div>
  )
}

export default Home