# ailandslideguard
AI-Based Early Warning and Landslide Risk Monitoring System
# 🏔️ LandslideGuard AI

LandslideGuard AI is a full-stack hazard monitoring, early-warning, and route-safety platform engineered specifically for landslide-prone regions in North East India. The system provides real-time spatial visualization of risk zones, meteorological telemetry (rainfall, soil moisture), and automated route safety evaluations.

---

## 🛠️ Tech Stack

* **Backend**: FastAPI, Python, SQLite, SQLAlchemy, Uvicorn
* **Frontend**: React, Vite, Leaflet.js, React-Leaflet, CSS3
* **Spatial Logic**: Haversine distance-based coordinate filtering and risk radius calculations

---

## 📁 Project Structure

```text
ailandslideguard/
│
├── backend/
│   ├── routes/
│   │   ├── alerts.py
│   │   ├── landslides.py
│   │   ├── prediction.py
│   │   ├── reports.py
│   │   └── routes.py
│   ├── services/
│   └── main.py
│
├── database/
│   └── database.py
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Home.jsx
    │   │   ├── RiskMap.jsx
    │   │   └── RouteChecker.jsx
    │   ├── services/
    │   │   └── api.js
    │   ├── App.jsx
    │   └── main.jsx
    └── package.json

    Prerequisites
Python (v3.10+) installed on your system

Node.js & npm installed on your system

1. Backend Setup (FastAPI)
Open a terminal in the root project directory:

PowerShell
cd C:\ailandslideguard
Install backend dependencies (if not already installed):

PowerShell
pip install fastapi uvicorn sqlalchemy pydantic
Start the FastAPI development server:

PowerShell
python -m uvicorn backend.main:app --reload
The backend will be live at http://localhost:8000.

2. Frontend Setup (React & Vite)
Open a new terminal window and navigate to the frontend folder:

PowerShell
cd C:\ailandslideguard\frontend
Install frontend dependencies:

PowerShell
npm install
Install Leaflet mapping packages:

PowerShell
npm install leaflet react-leaflet
Start the Vite development server:

PowerShell
npm run dev
The frontend dashboard will be available at your local Vite URL (e.g., http://localhost:5176).

 Key Features
Live Status Dashboard: Monitors active operational metrics, system health, and critical sector counts directly from the SQLite database.

Interactive Leaflet Risk Map: Plots monitored sectors across North East India with color-coded risk levels (Critical, High, Moderate, Low), interactive popups, and 25km/50km hazard radius overlays.

Route Safety Analyzer: Computes spatial safety ratings and hazards along custom travel paths using distance metrics.

Fallback Simulation: Gracefully switches to local simulation fallback states if backend telemetry is temporarily unreachable.

 License
This project is open-source and developed for academic and hazard-mitigation research purposes.