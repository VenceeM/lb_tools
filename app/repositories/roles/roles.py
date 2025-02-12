from sqlmodel import select,desc
from app.db.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.role.role import RoleSchema
from app.models.roles.model import RoleModel
import uuid

async def get_roles(session:AsyncSession):
    statement = select(RoleModel).order_by(desc(RoleModel.created_at))
    
    result = await session.exec(statement=statement)
    
    return result.all()


async def create_role(role_data:RoleSchema, session:AsyncSession):
    new_role_dict = role_data.model_dump()
    
    new_role = RoleModel(**new_role_dict)
    
    session.add(new_role)
    
    await session.commit()
    
    return new_role


async def get_role(title:str, session:AsyncSession):
    statement = select(RoleModel).where(RoleModel.title.lower() == title.lower())
    
    result = await session.exec(statement=statement)
    
    return result.first()

