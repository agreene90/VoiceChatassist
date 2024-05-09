
import aiosqlite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

database_url = 'sqlite+aiosqlite:///chat_memory.db'

# Using SQLAlchemy for connection pooling
engine = create_async_engine(database_url, echo=True, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def store_interaction(text, response, user_id=None, session_id=None):
    async with AsyncSessionLocal() as session:
        new_interaction = Interactions(text=text, response=response, user_id=user_id, session_id=session_id)
        session.add(new_interaction)
        await session.commit()

class Interactions(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    response = Column(String)
    timestamp = Column(DateTime, default=func.now())
    user_id = Column(String, index=True)
    session_id = Column(String, index=True)
