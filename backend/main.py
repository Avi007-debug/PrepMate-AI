"""
FastAPI application entrypoint for PrepMate-AI backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from config import settings

# Import routers
from routers.health import router as health_router
from routers.interview import router as interview_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health_router)
    app.include_router(interview_router)

    @app.on_event("startup")
    async def on_startup():
        logging.info(f"{settings.PROJECT_NAME} starting up")

    @app.on_event("shutdown")
    async def on_shutdown():
        logging.info(f"{settings.PROJECT_NAME} shutting down")

    return app


app = create_app()


if __name__ == "__main__":
    # When running directly, start uvicorn
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
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
