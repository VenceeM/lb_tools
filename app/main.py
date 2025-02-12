from fastapi import FastAPI
from app.api.v1.role.main import role_routes
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


app.include_router(role_routes,prefix=f"/api/{version}/roles", tags=["Roles"])