from sqlmodel import create_engine,SQLModel,select,text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine,create_async_engine
from app.core.config import Config
from sqlalchemy.orm import sessionmaker
from app.models.roles.model import RoleModel
from app.schemas.role.role import RoleSchema
from app.models.clients.client import Client
from fastapi import APIRouter,HTTPException,status,Query,Depends
from typing import List
import tantivy
from pydantic import BaseModel
from pymysqlreplication import BinLogStreamReader
from app.schemas.tantivy.schema import schema
from app.db.seeders.roles import seed

engine = create_async_engine(    
    url=Config.DATABASE_HOST,
    echo=True
    )

other_engine = create_async_engine(
    url=Config.OTHER_DB_URL,
    echo=True
    )

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        
async def seeder():
    Session = sessionmaker(
        bind=engine,
        class_= AsyncSession,
        expire_on_commit= False
    )
    
    async with Session() as session:
        await seed(session=session)
        

async def get_session():
    Session = sessionmaker(
        bind=engine,
        class_= AsyncSession,
        expire_on_commit= False
    )
    
    async with Session() as session:
        yield session
        
async def get_other_engine_session():
    Session = sessionmaker(
        bind=other_engine,
        class_=AsyncSession,
        expire_on_commit= False
    )
    
    async with Session() as session:
        yield session
        
async def get_other_engine() -> AsyncSession:
    
    Session = sessionmaker(
    bind=other_engine,
    class_=AsyncSession,
    expire_on_commit= False
    )
    
    async with Session() as session:
        sessions = session
        
    return sessions