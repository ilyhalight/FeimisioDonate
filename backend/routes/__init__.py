from fastapi import APIRouter

from routes.endpoints import api_privileges, api_promocodes, api_methods, api_callbacks, api_payment_systems

api_router = APIRouter(prefix = "/api")
api_router.include_router(api_privileges.router, tags = ['Privileges'])
api_router.include_router(api_promocodes.router, tags = ['Promocodes'])
api_router.include_router(api_methods.router, tags = ['Methods'])
api_router.include_router(api_callbacks.router, tags = ['Callbacks'], prefix = "/callback")
api_router.include_router(api_payment_systems.router, tags = ['Payment Systems'])

