from fastapi import APIRouter, Depends
from app.services.user.user import UserService
from app.models.user.model import UserModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user.schema import CreateUser,UpdateUser,DeactiveUser
from app.db.db import get_session
from typing import List
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from typing import Annotated
from app.dependency.dependencies import RoleChecker, AccessTokenBearer

user_routes = APIRouter()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin","user"]))

user_service = UserService()
security = HTTPBearer(auto_error=True)

@user_routes.get("/",response_model=List[UserModel],dependencies=[role_checker])
async def get_users(
    token_details = Depends(access_token_bearer),
    session:AsyncSession = Depends(get_session)
    ):
    
    users = await user_service.users(session=session)
    
    print(token_details)
    
    return users

@user_routes.post("/",response_model=UserModel)
async def create_user(user_data:CreateUser,session:AsyncSession = Depends(get_session)):
    new_user = await user_service.create(
        user_data=user_data,
        session=session
    )
    
    return new_user

@user_routes.patch("/",response_model=UserModel)
async def update_user(uid:str,update_user:UpdateUser,session:AsyncSession = Depends(get_session)):
    
    user = await user_service.update(
        uid=uid,
        user_data=update_user,
        session=session
    )
    
    return user
     
    
# Add deactivate user later.
    
        