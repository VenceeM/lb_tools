from fastapi import FastAPI
from app.api.v1.role.main import role_routes
from contextlib import asynccontextmanager;



@asynccontextmanager
async def life_span():
    pass


app = FastAPI()

app.include_router(role_routes,prefix="/roles", tags=["Roles"])