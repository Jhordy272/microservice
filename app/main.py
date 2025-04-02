from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.Database_Connection_ORM import DatabaseConnectionORM
from app.api.v1 import Auth_Endpoint
from app.api.v1 import Authz_Endpoint
from app.api.v1 import User_Endpoint
from app.api.v1 import Role_Endpoint

db = DatabaseConnectionORM()
Base = db.get_base()
engine = db.get_engine()
Base.metadata.create_all(engine)
session = db.get_session()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.openapi_schema = app.openapi()
    
    if app.openapi_schema and 'components' not in app.openapi_schema:
        app.openapi_schema['components'] = {}

    app.openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    app.openapi_schema["security"] = [{"BearerAuth": []}]
    yield

app = FastAPI(lifespan=lifespan, root_path="/auth-authz-api", servers=[{"url": "/auth-authz-api", "description": "API authentication-authorization"}])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

#app.include_router(Auth_Endpoint.router, prefix="/auth", tags=["Authentication"])

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )