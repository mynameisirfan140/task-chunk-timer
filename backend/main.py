import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.session import get_db
from backend.routers import task_router

app = FastAPI(title="Task Chunk Timer API")

# Enable CORS for frontend development (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router that defines all API endpoints
app.include_router(task_router.router, prefix="/api")

@app.get("/", response_model=dict)
def read_root():
    return {"message": "Task Chunk Timer API is running"}

# Dependency to provide a DB session per request
def get_current_db():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()