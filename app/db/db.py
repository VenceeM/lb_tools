from sqlmodel import create_engine,SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from app.core.config import Config
from sqlalchemy.orm import sessionmaker

engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_HOST,
        echo=True
    )
)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    Session = sessionmaker(
        bind=engine,
        class_= AsyncSession,
        expire_on_commit= False
    )
    
    async with Session() as session:
        yield session