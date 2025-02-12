from app.schemas.auth.auth import AuthSchema
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.utils import Utils
from app.repositories.users.user import UserRepository
from app.models.user.model import UserModel
from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
from datetime import timedelta


user_repository = UserRepository()
utils = Utils()
class AuthService:
    
    async def login(self,login_data:AuthSchema,session:AsyncSession):
        email = login_data.email.lower()
        password = login_data.password
        
        user = await user_repository.get_user_by_email(email=email,session=session)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )
            
        verify_password = utils.verify_passwd(
            password=password,
            password_hash=user.hash_password
        )
        
        if not verify_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )
            
        token = utils.create_access_token(
            user_data={
                "email":user.email,
                "user_id":str(user.uid),
            }
        )
        
        refresh_token = utils.create_access_token(
            user_data={
                "email":user.email,
                "user_id":str(user.uid),
            },
            expiry=timedelta(days=2)
        )
        
        response = JSONResponse(
            content={
                "message":"Login Success",
                "user":{
                    "email":email,
                    "user_id":str(user.uid),
                },
                "access_token":token,
                "refresh_token":refresh_token
            }
        )
        return response 
        
        
        
        
        