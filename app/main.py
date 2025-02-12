from fastapi import FastAPI
from app.api.v1.role.main import role_routes
from app.api.v1.user.user import user_routes
from app.api.v1.auth.auth import auth_routes
from contextlib import asynccontextmanager;


@asynccontextmanager
async def life_span():
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