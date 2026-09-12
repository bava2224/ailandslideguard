from fastapi import FastAPI

app = FastAPI(title="LandslideGuard AI")

@app.get("/")
def root():
    return {
        "message": "LandslideGuard AI Backend is running"
    }