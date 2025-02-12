from fastapi import APIRouter,HTTPException,status,Depends
from app.services.role.service import RoleService
from app.models.roles.model import RoleModel
from app.schemas.role.role import RoleSchema
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import JSONResponse
from typing import List
from app.db.db import get_session
from app.dependency.dependencies import AccessTokenBearer,RoleChecker

role_routes = APIRouter()
role_service = RoleService()

admin_role = Depends(RoleChecker(["admin"]))


@role_routes.get("/",response_model=List[RoleModel],dependencies=[admin_role])
async def get_all_roles(session:AsyncSession = Depends(get_session)):
    roles = await role_service.get_roles(session)
    
    return roles

@role_routes.post("/",response_model=RoleModel,dependencies=[admin_role])
async def create(role_data:RoleSchema, session:AsyncSession = Depends(get_session)):
    new_role = await role_service.create_role(
        role_data=role_data,
        session=session
    )
    
    return new_role

@role_routes.patch("/{uid}",response_model=RoleModel, dependencies=[admin_role])
async def update(uid:str,role_data:RoleSchema, session:AsyncSession = Depends(get_session)):
    updated_role = await role_service.update_role(
        uid=uid,
        update_role=role_data,
        session=session
    )
    
    return updated_role