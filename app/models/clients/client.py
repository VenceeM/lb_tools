from sqlmodel import SQLModel,Field,Column

class Client(SQLModel,table=True):    
    id:int = Field(default=None, primary_key=True)
    first_name:str
    middle_name:str
    last_name:str
    email:str
    phone:str