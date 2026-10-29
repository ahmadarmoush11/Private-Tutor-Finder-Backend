from fastapi import APIRouter

from app.features.areas.router import router as areas_router
from app.features.auth.router import router as auth_router
from app.features.client_posts.router import router as client_posts_router
from app.features.client_profiles.router import router as client_profiles_router
from app.features.degree_verifications.admin_router import router as degree_verifications_admin_router
from app.features.degree_verifications.router import router as degree_verifications_router
from app.features.lesson_requests.router import router as lesson_requests_router
from app.features.lesson_requests.tutor_router import router as tutor_inbox_router
from app.features.post_availabilities.router import router as post_availabilities_router
from app.features.post_availabilities.tutor_router import router as tutor_availabilities_router
from app.features.subjects.router import router as subjects_router
from app.features.tutor_posts.router import router as tutor_posts_router
from app.features.tutor_profiles.router import router as tutor_profiles_router
from app.features.tutor_reviews.client_router import router as client_reviews_router
from app.features.tutor_reviews.router import router as tutor_reviews_router
from app.features.tutor_reviews.tutor_router import router as tutor_received_reviews_router
from app.features.notifications.router import router as notifications_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(areas_router)
api_router.include_router(subjects_router)
api_router.include_router(client_profiles_router)
api_router.include_router(tutor_profiles_router)
api_router.include_router(client_posts_router)
api_router.include_router(tutor_posts_router)
api_router.include_router(lesson_requests_router)
api_router.include_router(tutor_inbox_router)
api_router.include_router(post_availabilities_router)
api_router.include_router(tutor_availabilities_router)
api_router.include_router(tutor_reviews_router)
api_router.include_router(client_reviews_router)
api_router.include_router(tutor_received_reviews_router)
api_router.include_router(notifications_router)
api_router.include_router(degree_verifications_router)
api_router.include_router(degree_verifications_admin_router)
