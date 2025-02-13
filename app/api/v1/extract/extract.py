from fastapi import APIRouter,HTTPException,Depends,status
from app.db.db import get_other_engine_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.helper import Helper

extract_route = APIRouter()
helper = Helper()

@extract_route.get("/")
async def extract_weekly_data(session:AsyncSession = Depends(get_other_engine_session)):
    result = await helper.extract(session=session)
    return result
    
@extract_route.post("/")
async def send_extraction(to:str,subject:str,body:str):
    return helper.send_email(recipient_email=to,subject=subject,body=body)