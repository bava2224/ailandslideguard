import { useState } from 'react'

function RouteChecker() {
  const [from, setFrom] = useState('')
  const [to, setTo] = useState('')
  const [result, setResult] = useState(null)

  function checkRoute() {
    if (!from || !to) return
    setResult({
      risk: 'Moderate',
      note: 'This route passes near one moderate-risk zone. Consider checking updates before travel.',
    })
  }

  return (
    <div style={{ padding: '40px' }}>
      <h1>Route Risk Checker</h1>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxWidth: '400px' }}>
        <input
          type="text"
          placeholder="From"
          value={from}
          onChange={(e) => setFrom(e.target.value)}
          style={{ padding: '10px', fontSize: '16px' }}
        />
        <input
          type="text"
          placeholder="To"
          value={to}
          onChange={(e) => setTo(e.target.value)}
          style={{ padding: '10px', fontSize: '16px' }}
        />
        <button
          onClick={checkRoute}
          style={{ padding: '10px', fontSize: '16px', backgroundColor: '#1b3a2b', color: 'white', border: 'none', cursor: 'pointer' }}
        >
          Check Route
        </button>
      </div>

      {result && (
        <div style={{ marginTop: '24px', padding: '16px', backgroundColor: '#e5c100', borderRadius: '8px', maxWidth: '400px' }}>
          <strong>Route Risk: {result.risk}</strong>
          <p>{result.note}</p>
        </div>
        
      )}
    </div>
  )
}

export default RouteChecker