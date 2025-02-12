from app.schemas.auth.auth import AuthSchema
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.utils import Utils
from app.repositories.users.user import UserRepository
from app.models.user.model import UserModel
user_repository = UserRepository()

class AuthRepository:
    
    async def check_user(email:str,session:AsyncSession):
        user = await user_repository.get_user_by_email(        
            email=email,
            session=session
        )
        
        return user
        
    
    async def login(login_data:AuthSchema,user_data:UserModel,session:AsyncSession):
        login_data_dict = login_data.model_dump()
        
        email = login_data.email
        password = login_data.password
        
        verify_password = Utils.verify_passwd(
            password=password,
            password_hash=user_data.hash_password
        )
        
        
        