from fastapi import APIRouter,Body,Request,Form
from typing import Annotated
from app.services.vault.vault import VaultService
from app.schemas.vault.vault import VaultSchema

vault_routes = APIRouter()
vault_service = VaultService()



@vault_routes.post("/")
async def generate(request:Request,secret_text:VaultSchema):
    
    result = await vault_service.generate_vault_link(data=secret_text.secret_text,request=request)
    
    return result

@vault_routes.get("/{key}",response_model=VaultSchema)
async def reveal_secret(key:str):
    return await vault_service.get_vault_secret(key=key)