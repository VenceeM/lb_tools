from celery import Celery
from app.core.config import Config
from app.core.helper import Helper
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.db import get_other_engine_session,get_other_engine
from asyncio import get_event_loop
from fastapi import HTTPException,BackgroundTasks
import asyncio
from app.db.seeders.roles import seed
from celery.result import AsyncResult
from typing import List

redis_host = f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0"
app = Celery(
    "worker",
    backend=redis_host,
    broker=redis_host
)
helper = Helper()


@app.task(name = "reports-extraction",track_started = True)
def extract(recipient_email:list[str],subject:str,body:str,uploaded_file:bytes):
    
    try:
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop=loop)
        
        result =loop.run_until_complete(
            helper.extract(recipient_emails=recipient_email,subject=subject,body=body,uploaded_file=uploaded_file)
        )
       
        return result
    except HTTPException as e :
        raise Exception(f"{e.detail}")
    except Exception as e:
        raise Exception(str(e))
    
        
    
async def get_extract(id:str):
    task = AsyncResult(id)
    active = app.control.inspect().active()

    return task.state

async def get_tasks():
    inspect = app.control.inspect()
    
    active_tasks = inspect.active() or {}
    reserved_tasks = inspect.reserved() or {}
    scheduled_tasks = inspect.scheduled() or {}
    
    return {
        "active": active_tasks,
        "reserved": reserved_tasks,
        "scheduled": scheduled_tasks
    }