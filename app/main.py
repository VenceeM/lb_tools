from fastapi import FastAPI,Depends
from app.api.v1.role.main import role_routes
from app.api.v1.user.user import user_routes
from app.api.v1.auth.auth import auth_routes
from app.api.v1.vault.vault import vault_routes
from app.api.v1.extract.extract import extract_route
from contextlib import asynccontextmanager;
from app.core.helper import Helper
from app.api.v1.search.search import search_routes
from app.core.config import Config
import os
import asyncio
helper = Helper()

@asynccontextmanager
async def life_span(app:FastAPI):
    
    # if os.path.exists(f"{os.getcwd()}/tmp/temp_index"):
    #     os.rmdir(f"{os.getcwd()}/tmp/temp_index")
    # else:
    #     os.makedirs(f"{os.getcwd()}/tmp/temp_index")

    yield
    

version = "v1"

app = FastAPI(
   
    title="Simple Tools",
    description="Playground",
    version=version,
    lifespan=life_span,
    docs_url="/mrdocs"
)


 
app.include_router(vault_routes,prefix=f"/api/{version}/vault",tags=["Credentials Vaule"])
app.include_router(auth_routes,prefix=f"/api/{version}/auth",tags=["Authentication"])
app.include_router(user_routes,prefix=f"/api/{version}/users", tags=["User"])
app.include_router(role_routes,prefix=f"/api/{version}/roles", tags=["Roles"])
app.include_router(extract_route,prefix=f"/api/{version}/extraction", tags=["Extractions"])
app.include_router(search_routes,prefix=f"/api/{version}/search", tags=["Search"])

    