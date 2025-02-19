from celery import Celery
from app.core.config import Config
from app.core.helper import Helper
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.db import get_other_engine_session,get_other_engine
from asyncio import get_event_loop
from fastapi import HTTPException
import asyncio
from celery.result import AsyncResult


redis_host = f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0"
app = Celery(
    "worker",
    backend=redis_host,
    broker=redis_host
)
helper = Helper()

@app.task(name="worker",track_started = True)
def extract(recipient_email:str,subject:str,body:str,uploaded_file:bytes,):
    
    try:
        
        result =  asyncio.run(
            helper.extract(recipient_email=recipient_email,subject=subject,body=body,uploaded_file=uploaded_file)
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