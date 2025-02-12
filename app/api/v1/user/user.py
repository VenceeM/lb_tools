from fastapi import APIRouter, Depends
from app.services.user.user import UserService
from app.models.user.model import UserModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user.schema import CreateUser,UpdateUser,DeactiveUser
from app.db.db import get_session
from typing import List
user_routes = APIRouter()

user_service = UserService()

@user_routes.get("/",response_model=List[UserModel])
async def get_users(session:AsyncSession = Depends(get_session)):
    users = await user_service.users(session=session)
    
    return users

@user_routes.post("/",response_model=UserModel)
async def create_user(user_data:CreateUser,session:AsyncSession = Depends(get_session)):
    new_user = await user_service.create(
        user_data=user_data,
        session=session
    )
    
    return new_user