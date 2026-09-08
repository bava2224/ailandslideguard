from fastapi import FastAPI

from backend.routes.alerts import router as alerts_router
from backend.routes.prediction import router as prediction_router
from backend.routes.reports import router as reports_router
from backend.routes.routes import router as routes_router


app = FastAPI(
    title="LandslideGuard AI",
    description="AI-based landslide risk monitoring, early-warning and route-risk analysis system.",
    version="1.0.0"
)


# Include routers
app.include_router(prediction_router)
app.include_router(alerts_router)
app.include_router(reports_router)
app.include_router(routes_router)


@app.get("/")
def root():
    return {
        "message": "LandslideGuard AI Backend",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "LandslideGuard AI Backend"
    }