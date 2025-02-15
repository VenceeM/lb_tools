import smtplib
from email.message import EmailMessage
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from .config import Config
from .constant import QUERY
import pandas as pd
from sqlmodel import create_engine
import urllib.parse
from datetime import datetime, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import text
from fastapi import status,Depends,HTTPException
from app.db.db import get_other_engine_session

class Helper:
    
    def delete_old_files(self,directory_path):
        try:
            files = os.listdir(directory_path)
            for file in files:
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return True
        except OSError as e:
            print(str(e))

    async def extract(self,recipient_email:str,subject:str,body:str,session:AsyncSession) -> dict | None:
        
        try:

            os.path
        
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d 00:00:00')
            end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d 23:59:59')

            cwd = os.getcwd()
            
            file_name = f"{(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")}-{(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")}"
            file_path = f"{cwd}/app/files/{file_name}.xlsx"
            
            statement = text(QUERY)
            
            result = await session.exec(statement=statement,params=[{"start_date":start_date,"end_date":end_date}])
            rows = result.fetchall()
            
            if not rows:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No Data"
                )
            
            data_frame = pd.DataFrame(rows,columns=result.keys())
            data_frame.to_excel(file_path,engine="openpyxl")
            
            
            self.send_email(
                recipient_email=recipient_email,
                subject=subject,
                body=body
            )
            
            return {
                "success": "Success"
            }
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"{str(e)}")

           
        
        
    def send_email(self,recipient_email:str,subject:str,body:str):
        cwd = os.getcwd()
        file_name = f"{(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")}-{(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")}"
        file_path = f"{cwd}/app/files/{file_name}.xlsx"
        directory = f"{cwd}/app/files"
        
        msg = MIMEMultipart()
        msg["From"] = Config.SENDER_EMAIL
        msg["To"] = recipient_email
        msg["Subject"] =subject
        
        msg.attach(MIMEText(body,"plain"))
        
        if os.path.exists(file_path):
            with open(file_path,"rb") as attachment:
                mime_base = MIMEBase("application","octet-stream")
                mime_base.set_payload(attachment.read())
                encoders.encode_base64(mime_base)
                mime_base.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
                msg.attach(mime_base)
                
        else:
            print("File not found")
            exit()
            
        try:
            server = smtplib.SMTP(Config.SMTP_SERVER,Config.SMTP_PORT)
            server.starttls()
            server.login(Config.SENDER_EMAIL,Config.SENDER_PASSWORD)
            server.sendmail(Config.SENDER_EMAIL,recipient_email,msg.as_string())
            server.quit()
        except Exception as e:
            print(e)
            
        finally:
            self.delete_old_files(directory_path=directory)