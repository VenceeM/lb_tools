from pydantic import BaseModel, Field
from typing import Optional
import uuid


class CreateUser(BaseModel):
    first_name : str
    last_name : str
    email: str
    hash_password:str
    
class UpdateUser(BaseModel):
    first_name : Optional[str]
    last_name : Optional[str]
    email: Optional[str]
    
class DeactiveUser(BaseModel):
    status:str