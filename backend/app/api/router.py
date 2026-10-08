from fastapi import APIRouter

from app.features.auth.router import router as auth_router
from app.features.client_posts.router import router as client_posts_router
from app.features.client_profiles.router import router as client_profiles_router
from app.features.tutor_profiles.router import router as tutor_profiles_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(client_profiles_router)
api_router.include_router(tutor_profiles_router)
api_router.include_router(client_posts_router)
