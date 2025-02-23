from sqlmodel import SQLModel,Field,Column
import sqlalchemy.dialects.postgresql as pg
from typing import Optional,List
import uuid
from .status import StatusEnum
from datetime import datetime

class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    role_uid : Optional[uuid.UUID] = Field(foreign_key="roles.uid")
    first_name : str
    last_name : str
    email: str = Field(unique=True,nullable=False)
    hash_password:str = Field(nullable=False,exclude=True)
    is_verified: bool = Field(default=False)
    status:str = Field(default=StatusEnum.ACTIVE,nullable=False)
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            nullable=False,
            default=datetime.now()
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            nullable=False,
            default=datetime.now()
        )
    )
    
    
def __repr__(self):
    return f"<User {self.email}>"