from app.services.auth.auth import AuthService
from fastapi import APIRouter,Depends
from app.db.db import get_session
from app.schemas.auth.auth import AuthSchema
from sqlmodel.ext.asyncio.session import AsyncSession

auth_routes = APIRouter()
auth_service = AuthService()

@auth_routes.post("/login")
async def user_login(login_data:AuthSchema,session:AsyncSession = Depends(get_session)):
    login = await auth_service.login(login_data=login_data,session=session)
    return login