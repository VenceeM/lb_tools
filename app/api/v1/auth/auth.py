from app.services.auth.auth import AuthService
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from app.db.db import get_session
from app.schemas.auth.auth import AuthSchema
from sqlmodel.ext.asyncio.session import AsyncSession
from app.dependency.dependencies import RefreshTokenBearer,AccessTokenBearer
from app.core.utils import Utils
from app.db.redis import add_jwt_id_to_blocklist
from datetime import datetime

auth_routes = APIRouter()
auth_service = AuthService()
utils = Utils()
access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()

@auth_routes.post("/login")
async def user_login(login_data:AuthSchema,session:AsyncSession = Depends(get_session)):
    login = await auth_service.login(login_data=login_data,session=session)
    return login

@auth_routes.get("/refresh_token")
async def refresh_token(token_details = Depends(refresh_token_bearer)):
    expiry_timestamp = token_details["exp"]
    
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = utils.create_access_token(
            user_data=token_details["user"]
        )
        
        return JSONResponse(
            content={
                "access_token":new_access_token
            }
        )
        
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid token"
    )
    
@auth_routes.get("/logout")
async def revoke(token_details:dict = Depends(access_token_bearer)):
    jwt_id = token_details["jwt_id"]
    
    await add_jwt_id_to_blocklist(jwt_id=jwt_id)
    
    return JSONResponse(
        content={
            "message":"Logged out successfully"
        },
        status_code=status.HTTP_200_OK
    )