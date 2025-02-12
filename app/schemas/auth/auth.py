from pydantic import BaseModel,Field


class AuthSchema(BaseModel):
    email:str
    password:str