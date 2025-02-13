from fastapi import FastAPI,Depends
from app.api.v1.role.main import role_routes
from app.api.v1.user.user import user_routes
from app.api.v1.auth.auth import auth_routes
from app.api.v1.extract.extract import extract_route
from contextlib import asynccontextmanager;
from app.core.helper import Helper
from app.db.db import get_session,get_other_engine_session

helper = Helper()

@asynccontextmanager
async def life_span(app:FastAPI):
    pass

version = "v1"

app = FastAPI(
    title="Lb Tools",
    description="Simple tools",
    version=version
)


app.include_router(auth_routes,prefix=f"/api/{version}/auth",tags=["Authentication"])
app.include_router(user_routes,prefix=f"/api/{version}/users", tags=["User"])
app.include_router(role_routes,prefix=f"/api/{version}/roles", tags=["Roles"])
app.include_router(extract_route,prefix=f"/api/{version}/extraction", tags=["Extraction"])