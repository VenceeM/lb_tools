from app.schemas.user.schema import CreateUser, UpdateUser,DeactiveUser
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from app.models.user.model import UserModel
from app.core.utils import Utils

utils = Utils()

class UserRepository:
    
    
    async def get_users(self, session:AsyncSession):
        statement = select(UserModel).order_by(desc(UserModel.created_at))
        
        result = await session.exec(statement=statement)
        
        return result
    
    
    async def get_user(self,uid:str,session:AsyncSession):
        statement = select(UserModel).where(UserModel.uid == uid)
        result = await session.exec(statement=statement)
        
        return result.first()
    
    async def get_user_by_email(self,email:str,session:AsyncSession):
        statement = select(UserModel).where(UserModel.email == email)
        
        result = await session.exec(statement=statement)
        
        return result.first()
    
    async def create_user(self,user_data : CreateUser, session:AsyncSession):
        
        user_data_dict = user_data.model_dump()
        
        new_user = UserModel(**user_data_dict)
        new_user.hash_password = utils.generate_passwd_hash(user_data_dict["hash_password"])
        
        session.add(new_user)
        
        await session.commit()
        return new_user
    
    
    async def update_user(self, user_data: UpdateUser,updated_user:UserModel ,session:AsyncSession):
        user_data_dict = user_data.model_dump()
        
        for key, value in user_data_dict.items():
            setattr(updated_user,key,value)
        
        await session.commit()
        
        return updated_user
    
    async def deactivate_user(self,user_data:DeactiveUser,updated_user:UserModel,session:AsyncSession):
        user_data_dict = user_data.model_dump()
        
        updated_user.status = user_data_dict.get("status")
        
        await session.commit()
        
        return updated_user
    
    