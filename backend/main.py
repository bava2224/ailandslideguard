# main.py (at root C:\ailandslideguard\main.py)
import sys
from pathlib import Path

# Force Python to look in the backend directory and root directory for modules
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Handle imports safely whether folders are in root or backend
try:
    from database.database import engine, Base
    from routes.alerts import router as alerts_router
    from routes.prediction import router as prediction_router
    from routes.reports import router as reports_router
    from routes.routes import router as routes_router
    from routes.landslides import router as landslides_router
except ImportError:
    from backend.database.database import engine, Base
    from backend.routes.alerts import router as alerts_router
    from backend.routes.prediction import router as prediction_router
    from backend.routes.reports import router as reports_router
    from backend.routes.routes import router as routes_router
    from backend.routes.landslides import router as landslides_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LandslideGuard AI",
    description="AI-based landslide risk monitoring, early-warning and route-risk analysis system.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.status_code,
            "message": exc.detail,
            "path": request.url.path,
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
    )

app.include_router(prediction_router)
app.include_router(alerts_router)
app.include_router(reports_router)
app.include_router(routes_router)
app.include_router(landslides_router, prefix="/api/v1/landslides", tags=["Landslides"])

@app.get("/")
def root():
    return {"message": "LandslideGuard AI Backend", "status": "running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "LandslideGuard AI Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)