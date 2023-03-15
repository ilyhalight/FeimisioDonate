from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FeimisioDonate",
        version="1.0.0",
        description="FeimisioDonate API Docs",
        terms_of_service="/terms/",
        license_info = {
            "name": "MIT",
        },
        routes = app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/api/static/assets/logo.svg",
        "altText": "Логотип Feimisio"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

tags_meta = [
    {
        'name': 'Privileges',
        'description': 'Operations with privileges'
    },
    {
        'name': 'Methods',
        'description': 'Operations with payment methods'
    },
    {
        'name': 'Payment Systems',
        'description': 'Operations with payment systems'
    },
    {
        'name': 'Promocodes',
        'description': 'Operations with promocodes'
    },
    {
        'name': 'Callbacks',
        'description': 'Getting callbacks from payment systems'
    },
]


app = FastAPI(openapi_url = '/api/openapi.json', docs_url = '/api/docs', redoc_url = '/api/redoc')
app.mount('/api/static', StaticFiles(directory = 'static'), name = 'static')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.openapi = custom_openapi