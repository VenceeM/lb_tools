from passlib.context import CryptContext
import secrets
import jwt
from datetime import datetime,timedelta
import uuid
from app.core.config import Config
import logging
from app.repositories.roles.roles import RoleRepository

passwd_context = CryptContext(schemes=["bcrypt"])


ACCESS_TOKEN_EXPIRY = 3600

class Utils:
    
    
    
    def generate_passwd_hash(self,password:str) -> str:
        hash = passwd_context.hash(password)
        return hash

    def verify_passwd(self, password:str, password_hash:str) -> bool:
        verify = passwd_context.verify(password,password_hash)
        return verify
    
    
        """
        This is a simple random generator tool 
        by default it has 16 bytes/character
        """
    def random_secret_generator(self, bytes:int = 16) -> str:
        random_string = secrets.token_urlsafe(bytes)
        return random_string
    
    def create_access_token(self,user_data:dict, expiry:timedelta = None, refresh:bool = False) -> str:
        payload = {}
        payload["user"] = user_data
        payload["exp"] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
        payload["jwt_id"] = str(uuid.uuid4())
        payload["refresh"] = refresh
        
        token = jwt.encode(
            payload=payload,
            key=Config.JWT_SECRET,
            algorithm=Config.JWT_ALORITHM
        )
        
        return token
    
    def decode_token(self, token:str) -> dict:
        try:
            token_data = jwt.decode(
                jwt=token,
                key=Config.JWT_SECRET,
                algorithms=[Config.JWT_ALORITHM]
            )
            
            return token_data
            
        except jwt.PyJWTError as e:
            logging.exception(e)
            return None