from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze, health

app = FastAPI(title="Resume Analyzer API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router, tags=["health"])
app.include_router(analyze.router, prefix="/api/v1", tags=["analysis"])
