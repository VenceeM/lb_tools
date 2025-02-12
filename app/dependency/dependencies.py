from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.requests import Request
from app.core.utils import Utils
from fastapi import HTTPException, status,Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.redis import token_in_blocklist
from app.db.db import get_session
from typing import List
from app.repositories.users.user import UserRepository
from app.repositories.roles.roles import RoleRepository
from app.models.user.model import UserModel
import uuid

utils = Utils()
user_repository = UserRepository()
role_repository = RoleRepository()
class TokenBearer(HTTPBearer):
    
    def __init__(self,auto_error = True):
        super().__init__(auto_error=auto_error)
        
    
    async def __call__(self, request:Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        token = creds.credentials
        token_data = utils.decode_token(token)
        
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token"
            )
            
        
        if await token_in_blocklist(token_data["jwt_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token"
            )
            
        self.verify_token_data(token_data=token_data)
            
        return token_data
        
        
        
    async def token_valid(self,token:str) -> bool:
        token_data = utils.decode_token(token=token)
        
        if token_data is not None:
            return True
        
        return False
    
    def verify_token_data(self,token_data):
        raise NotImplementedError("Please override this method in child classes")
        
        
        
class AccessTokenBearer(TokenBearer):
    
    def verify_token_data(self,token_data) -> None:
        if token_data["refresh"] and token_data["refresh"] is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token"
            )
            
class RefreshTokenBearer(TokenBearer):
    
    def verify_token_data(self,token_data) -> None:
        if not token_data["refresh"] and token_data["refresh"] is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token"
            )
            
            
async def get_current_user(token_details: dict = Depends(AccessTokenBearer()), session:AsyncSession = Depends(get_session)):
    user_email = token_details["user"]["email"]

    user = await user_repository.get_user_by_email(email=user_email, session=session)
    
    return user


class RoleChecker:
    def __init__(self,allowed_roles:List[str]) -> None:
        self.allow_roles = allowed_roles
        
        
        
    async def __call__(self, current_user:UserModel = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
        
        roles = []
        for i in self.allow_roles:
            get_role = await role_repository.role(title=i,session=session)
            roles.append(get_role.uid)
        
        
        if current_user.role_uid in roles:
            return True
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission"
        )
        