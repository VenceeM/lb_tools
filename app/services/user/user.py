from app.repositories.users.user import UserRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user.schema import CreateUser,UpdateUser,DeactiveUser
from fastapi import HTTPException,status
from app.repositories.roles.roles import RoleRepository

user_repository = UserRepository()
role_repository = RoleRepository()

class UserService:
   
    USER_NOT_FOUND = "User not found"
    
    async def users(self,session:AsyncSession):
        users = await user_repository.get_users(session=session)
        
        return users
    
    async def user(self,uid:str ,session:AsyncSession):
        user = await user_repository.get_user(uid=uid,session=session)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.USER_NOT_FOUND
            )
        
        return user
    
    async def create(self,user_data:CreateUser,session:AsyncSession):
        email = user_data.email.lower()
        user = await user_repository.get_user_by_email(email=email,session=session)
        
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already exist."
            )
            
        role_id = await role_repository.role(title="user", session=session)
        
        new_user = await user_repository.create_user(user_data=user_data,role_uid=role_id.uid,session=session)
        
        return new_user
    
    async def update(self, uid:str ,user_data:UpdateUser, session:AsyncSession):
    
        user = await user_repository.get_user(uid=uid,session=session)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.USER_NOT_FOUND
            )
            
        update_user = await user_repository.update_user(
            user_data=user_data,
            updated_user=user,
            session=session
        )
        
        return update_user
    
    async def deactivate(self,uid:str ,user_data:DeactiveUser,session:AsyncSession):
        user = await user_repository.get_user(uid=uid,session=session)
       
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.USER_NOT_FOUND
            )

        deactivate_user = await user_repository.deactivate_user(
            user_data=user_data,
            updated_user=user,
            session=session
        )
        
        return deactivate_user
        
    
    
    