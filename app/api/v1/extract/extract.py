from fastapi import APIRouter,HTTPException,Depends,status,UploadFile,BackgroundTasks,Request,Body
from app.db.db import get_other_engine_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.helper import Helper
from app.dependency.dependencies import AccessTokenBearer,RoleChecker
from typing import Annotated
import asyncio
from celery import Celery
from app.core.config import Config
from app.core.worker import extract, get_extract

extract_route = APIRouter()
helper = Helper()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin","user"]))




@extract_route.post("/", dependencies=[role_checker])
async def extract_weekly_data(file:UploadFile,to:Annotated[str, Body()],subject:Annotated[str, Body()],body:Annotated[str,Body()],session:AsyncSession = Depends(get_other_engine_session), token_details = Depends(access_token_bearer)):
    
    file_bytes = await file.read()
    
    result =  extract.delay(recipient_email=to,subject=subject,body=body,uploaded_file=file_bytes)
    # result = await helper.extract(recipient_email=to,subject=subject,body=body,session=session,file=file)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong"
        )
    
    return {
        "message":"Processing in background...",
        "task":result.id
    }

@extract_route.get("/")
async def get_extracted(id:str):
    result = await get_extract(id)
    return result


# @extract_route.post("/", dependencies=[role_checker])
# async def send_extraction(to:str,subject:str,body:str,token_details = Depends(access_token_bearer)):
#     return helper.send_email(recipient_email=to,subject=subject,body=body)