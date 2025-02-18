from app.services.role.service import RoleService
from sqlmodel import text
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.role.role import RoleSchema
from app.repositories.roles.roles import RoleRepository

role_service = RoleService()
role_repository = RoleRepository()

async def seed(session: AsyncSession ):
    
    role = await role_service.get_roles(session=session)
    
    if "user" not in role:
        await user_seed(session)
        
    if "admin" not in role:
        await admin_seed(session)
    
        
async def user_seed(session: AsyncSession) -> None:
    role_data = RoleSchema(
        title="user"
    )
    
    role = await role_repository.role(role_data.title.lower(),session=session)
    if not role:
        await role_service.create_role(role_data=role_data,session=session)
   
async def admin_seed(session: AsyncSession) -> None:
    role_data = RoleSchema(
        title="admin"
    )
    role = await role_repository.role(role_data.title.lower(),session=session)
    if not role:
        await role_service.create_role(role_data=role_data,session=session)
    
   