from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import time
import logging
import structlog

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.v1.api import api_router

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


def create_application() -> FastAPI:
    """Create FastAPI application with all configurations"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        description="STRAUMANN Event Management API",
        contact={
            "name": "STRAUMANN Event Team",
            "email": "support@straumann-event.com",
        },
        license_info={
            "name": "MIT",
        },
    )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add trusted host middleware for security
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["*"]  # Configure this properly in production
    )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


# Create the app instance
app = create_application()


# Middleware for request timing and logging
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request
    logger.info(
        "Request started",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None
    )
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log completed request
    logger.info(
        "Request completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=process_time
    )
    
    return response


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.error(
        "Validation error",
        method=request.method,
        url=str(request.url),
        errors=exc.errors()
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "message": "Please check your input data"
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(
        "Unhandled exception",
        method=request.method,
        url=str(request.url),
        error=str(exc),
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        },
    )


# Application lifecycle events
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting STRAUMANN Event API", version=settings.VERSION)
    
    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("Shutting down STRAUMANN Event API")
    
    # Close database connections
    try:
        await close_db()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error("Error closing database connections", error=str(e))


# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "timestamp": time.time()
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# WebSocket connection manager for real-time features
class ConnectionManager:
    """WebSocket connection manager for live sessions"""
    
    def __init__(self):
        self.active_connections: dict = {}
        self.session_connections: dict = {}
    
    async def connect(self, websocket, user_id: str, session_id: str = None):
        """Connect user to WebSocket"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        
        if session_id:
            if session_id not in self.session_connections:
                self.session_connections[session_id] = []
            self.session_connections[session_id].append(user_id)
        
        logger.info("WebSocket connected", user_id=user_id, session_id=session_id)
    
    def disconnect(self, user_id: str, session_id: str = None):
        """Disconnect user from WebSocket"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        if session_id and session_id in self.session_connections:
            if user_id in self.session_connections[session_id]:
                self.session_connections[session_id].remove(user_id)
        
        logger.info("WebSocket disconnected", user_id=user_id, session_id=session_id)
    
    async def send_personal_message(self, message: str, user_id: str):
        """Send message to specific user"""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_text(message)
    
    async def broadcast_to_session(self, message: str, session_id: str):
        """Broadcast message to all users in a session"""
        if session_id in self.session_connections:
            for user_id in self.session_connections[session_id]:
                await self.send_personal_message(message, user_id)


# Global connection manager instance
manager = ConnectionManager()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    ) 