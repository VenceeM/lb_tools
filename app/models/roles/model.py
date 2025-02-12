from sqlmodel import SQLModel, Field,Column
import uuid
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime

class RoleModel(SQLModel, table=True):
    __tablename__ = "roles"
    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str 
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
    return f"<Role {self.title}>"