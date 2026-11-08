from fastapi import APIRouter
from app.api.routers import mood, recommend, feedback, catalog

api_router = APIRouter()
api_router.include_router(mood.router)
api_router.include_router(recommend.router)
api_router.include_router(feedback.router)
api_router.include_router(catalog.router)

