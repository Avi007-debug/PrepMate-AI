"""FastAPI application entrypoint for PrepMate-AI backend"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers.health import router as health_router
from routers.interview import router as interview_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="AI-powered interview preparation platform",
        version="1.0.0",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Include routers
    app.include_router(health_router)
    app.include_router(interview_router)

    # Root endpoint
    @app.get("/")
    async def root():
        return {"message": "Welcome to PrepMate-AI API"}

    # Startup and shutdown events
    @app.on_event("startup")
    async def on_startup():
        logging.info(f"{settings.PROJECT_NAME} starting up")

    @app.on_event("shutdown")
    async def on_shutdown():
        logging.info(f"{settings.PROJECT_NAME} shutting down")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
