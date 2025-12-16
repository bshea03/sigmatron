from fastapi import APIRouter
from apps.api.app.routers.oauth import router as oauth_router

api_router = APIRouter()
api_router.include_router(oauth_router, prefix="/oauth", tags=["OAuth"])