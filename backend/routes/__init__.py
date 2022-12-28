from fastapi import APIRouter

from routes.endpoints import api_privilleges, api_methods, api_callbacks

api_router = APIRouter()
api_router.include_router(api_privilleges.router, tags = ['Privilleges'])
api_router.include_router(api_methods.router, tags = ['Methods'])
api_router.include_router(api_callbacks.router, tags = ['Callbacks'])

