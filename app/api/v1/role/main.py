from fastapi import APIRouter,HTTPException,status,Depends
from app.services.role.service import RoleService
from app.models.roles.model import RoleModel
from app.schemas.role.role import RoleSchema
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from app.db.db import get_session

role_routes = APIRouter()
role_service = RoleService()

@role_routes.get("/",response_model=List[RoleModel])
async def get_all_roles(session:AsyncSession = Depends(get_session)):
    roles = await role_service.get_roles(session)
    
    return roles