from sqlmodel import select,desc
from app.db.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.role.role import RoleSchema,UpdateRoleSchema
from app.models.roles.model import RoleModel
import uuid

class RoleRepository:
    
    async def roles(self,session:AsyncSession):
        statement = select(RoleModel).order_by(desc(RoleModel.created_at))
        
        result = await session.exec(statement=statement)
        
        return result.all()


    async def create(self,role_data:RoleSchema, session:AsyncSession):
        new_role_dict = role_data.model_dump()
        
        new_role = RoleModel(**new_role_dict)
        
        session.add(new_role)
        
        await session.commit()
        
        return new_role


    async def role(self,title:str, session:AsyncSession):
        statement = select(RoleModel).where(RoleModel.title == title)
        
        result = await session.exec(statement=statement)
        
        return result.first()


    async def role_by_id(self,uid:str,session:AsyncSession):
        statement = select(RoleModel).where(RoleModel.uid == uid)
        
        result = await session.exec(statement=statement)
        
        return result.first()
        

    async def update(self,role_data: RoleSchema,update_role:RoleModel,session:AsyncSession):
        role_data_dict = role_data.model_dump()
        
        for key, value in role_data_dict.items():
            setattr(update_role,key,value)
        
        await session.commit()
        
        return update_role
        
    