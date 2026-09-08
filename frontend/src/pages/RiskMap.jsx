function RiskMap() {
  const zones = [
    { name: 'Zone A - Shillong Hills', level: 'High', color: '#e07b39' },
    { name: 'Zone B - Kohima Slopes', level: 'Critical', color: '#c0392b' },
    { name: 'Zone C - Itanagar Ridge', level: 'Moderate', color: '#e5c100' },
    { name: 'Zone D - Aizawl Basin', level: 'Low', color: '#4a934a' },
  ]

  return (
    <div style={{ padding: '40px' }}>
      <h1>Risk Map</h1>
      <p>Current landslide risk zones (sample data for demo):</p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '20px' }}>
        {zones.map((zone) => (
          <div
            key={zone.name}
            style={{
              padding: '16px',
              borderRadius: '8px',
              backgroundColor: zone.color,
              color: 'white',
              fontWeight: 'bold',
            }}
          >
            {zone.name} — {zone.level} Risk
          </div>
        ))}
      </div>
    </div>
  )
}

export default RiskMap