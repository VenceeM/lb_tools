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
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["user","admin"]))

user_service = UserService()
security = HTTPBearer(auto_error=True)



@user_routes.get("/",response_model=List[UserModel],dependencies=[admin_role_checker])
async def get_users(
    session:AsyncSession = Depends(get_session)
    ):
    users = await user_service.users(session=session)
    return users

@user_routes.get("/me",response_model=UserModel,dependencies=[user_role_checker])
async def get_user(token_details = Depends(access_token_bearer), session:AsyncSession = Depends(get_session)):
    uid = token_details["user"]["user_id"]
    user = await user_service.user(uid=uid,session=session)
    return user



@user_routes.post("/sign_up",response_model=UserModel)
async def create_user(user_data:CreateUser,session:AsyncSession = Depends(get_session)):
    new_user = await user_service.create(
        user_data=user_data,
        session=session
    )
    
    return new_user


@user_routes.patch("/update/{uid}",response_model=UserModel,dependencies=[user_role_checker])
async def update_user(
    uid:str,
    update_user:UpdateUser,
    session:AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer)
    ):
    
    user = await user_service.update(
        uid=uid,
        user_data=update_user,
        session=session
    )
    
    return user
     
    
# Add deactivate user later.
    
        