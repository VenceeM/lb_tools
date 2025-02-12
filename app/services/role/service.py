from app.repositories.roles.roles import RoleRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException,status
from app.schemas.role.role import RoleSchema,UpdateRoleSchema
from fastapi.responses import JSONResponse

role_repository = RoleRepository()    

class RoleService:
    
    async def get_roles(self, session:AsyncSession):
        roles = await role_repository.roles(session=session)
        return roles
    
    async def create_role(self, role_data:RoleSchema,session:AsyncSession):

        role = await role_repository.role(role_data.title.lower(),session=session)
        
        if role:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role is already exist."
        )
        
        new_role = await role_repository.create(
            role_data=role_data,
            session=session
        )
        
        return new_role
        
    async def update_role(self,uid:str,update_role:UpdateRoleSchema, session: AsyncSession):
        
        role = await role_repository.role_by_id(uid=uid,session=session)
        
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found."
            )
            
        update = await role_repository.update(
            role_data=update_role,
            update_role=role,
            session=session
        )
        
        return update