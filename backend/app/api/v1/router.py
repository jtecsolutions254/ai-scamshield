from fastapi import APIRouter
from app.api.v1 import email, sms, url, stats

api_router = APIRouter()
api_router.include_router(email.router, tags=["Analyze Email"])
api_router.include_router(sms.router, tags=["Analyze SMS"])
api_router.include_router(url.router, tags=["Analyze URL"])
api_router.include_router(stats.router, tags=["Stats"])
