"""
FastAPI entrypoint for PrepMate-AI backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import interview, health
from config import settings

app = FastAPI(
    title="PrepMate-AI API",
    description="AI-powered interview preparation platform",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(interview.router)


@app.get("/")
async def root():
    return {"message": "Welcome to PrepMate-AI API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
