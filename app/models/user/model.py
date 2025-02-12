from sqlmodel import SQLModel,Field,Column
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
import uuid
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
    role_uid : Optional[uuid.UUID] = Field(default=None,foreign_key="roles.uid")
    first_name : str
    last_name : str
    email: str = Field(unique=True,nullable=False)
    hash_password:str
    is_verified: bool = Field(default=False)
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