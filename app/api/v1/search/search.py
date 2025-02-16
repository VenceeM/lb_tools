from fastapi import Query,APIRouter,HTTPException,status
from typing import List
from app.core.config import Config
from app.services.search.search import SearchService

search_routes = APIRouter()

search_service = SearchService()

@search_routes.get("/")
async def search(query:str = Query(... , title="Searching"), field_names: str = Query(..., title="Field names")):
    fields = field_names.split(" ")
    
    return await search_service.search(query,fields)

@search_routes.post("/initialize")
async def initialize_engine(data: List[dict]):
    return await search_service.init_data(data)

@search_routes.patch("/")
async def update_record(data:dict):
    return await search_service.add_or_update(data)

# Deprecated
@search_routes.delete("/",deprecated=True)
async def delete_all_record():
    return await search_service.delete_all_records()