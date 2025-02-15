from fastapi import FastAPI,Depends
from app.api.v1.role.main import role_routes
from app.api.v1.user.user import user_routes
from app.api.v1.auth.auth import auth_routes
from app.api.v1.extract.extract import extract_route
from contextlib import asynccontextmanager;
from app.core.helper import Helper
from app.api.v1.search.search import search_routes
import os

helper = Helper()

@asynccontextmanager
async def life_span(app:FastAPI):
    if not os.path.exists(f"{os.getcwd()}/tmp/temp_index"):
        
        os.makedirs(f"{os.getcwd()}/tmp/temp_index")
    
    yield
    

version = "v1"

app = FastAPI(
    title="Lb Tools",
    description="Simple tools",
    version=version,
    lifespan=life_span
)





app.include_router(auth_routes,prefix=f"/api/{version}/auth",tags=["Authentication"])
app.include_router(user_routes,prefix=f"/api/{version}/users", tags=["User"])
app.include_router(role_routes,prefix=f"/api/{version}/roles", tags=["Roles"])
app.include_router(extract_route,prefix=f"/api/{version}/extraction", tags=["Extraction"])
app.include_router(search_routes,prefix=f"/api/{version}/search", tags=["Search"])