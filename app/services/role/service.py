from app.repositories.roles.roles import get_role,get_roles,create_role
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException,status
from app.schemas.role.role import RoleSchema

class RoleService:
    
    async def get_roles(self, session:AsyncSession):
        roles = await get_roles(session=session)
        return roles
    
    async def create_role(self, role_data:RoleSchema,session:AsyncSession):
        
        role = await get_role(role_data.title.lower(),session=session)
        
        if role:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role is already exist."
            )
        
        new_role = await create_role(
            role_data=role_data,
            session=session
        )
        
        return new_role
        