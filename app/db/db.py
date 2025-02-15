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
        

# index = tantivy.Index(schema=schema)
# writer = index.writer()


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
        
# async def init_customers():
    
#     async for session in get_other_engine_session():
#         query = text(
#             """
#             SELECT id,first_name,middle_name,last_name,email,phone FROM customers WHERE deleted_at is NULL AND is_deleted_by_customer is NULL
            
#             """
#         )
#         result = await session.exec(statement=query)
#         customers = result.all()
        
#         for customer in customers:
#             writer.add_document(
#                 tantivy.Document(
#                     id=str(customer.id),
#                     first_name=customer.first_name if customer.first_name else "",
#                     middle_name=customer.middle_name if customer.middle_name else "",
#                     last_name=customer.last_name if customer.last_name else "",
#                     email=customer.email if customer.email else "",
#                     phone=customer.phone if customer.phone else ""
                    
#                 )
#             )
#         writer.commit()