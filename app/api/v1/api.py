from fastapi import APIRouter

from app.api.v1 import auth, events, sessions, speakers, favorites

api_router = APIRouter()

# Include all route modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(events.router, prefix="/events", tags=["Events"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(speakers.router, prefix="/speakers", tags=["Speakers"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])

# Additional routers will be added here as we create them
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(gallery.router, prefix="/gallery", tags=["Gallery"])
# api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
# api_router.include_router(networking.router, prefix="/networking", tags=["Networking"])
# api_router.include_router(surveys.router, prefix="/surveys", tags=["Surveys"])
# api_router.include_router(products.router, prefix="/products", tags=["Products"])
# api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
# api_router.include_router(websocket.router, prefix="/ws", tags=["WebSocket"]) 