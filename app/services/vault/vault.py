from fastapi import HTTPException, Request,status,Response
from app.db.redis import store_secrets, delete_secret,get_secret
from app.core.utils import Utils
from app.schemas.vault.vault import VaultSchema

util = Utils()

class VaultService:
    
    async def generate_vault_link(self,data:str,request:Request) -> str:
        current_path = request.url
        
        encrypted_data = util.encrypt_data(data=data)
        key = encrypted_data["key"]
        value = encrypted_data["data"]
        url_key = encrypted_data["url_key"]
        values = {
            "key":key,
            "value": value
        }
        result = await store_secrets(
            key=url_key,
            value=values,
            expiration=3600
        )

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Something went wrong"
            )
            
        full_path = f"{current_path}{url_key}"
        
        return full_path
    
    
    async def get_vault_secret(self,key):
        result = await get_secret(key=key)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data not found"
            )
        
        key = result.get("key")
        value = result.get("value")
        
        decrypted_message = util.decrypt_data(key,value)
       
        return VaultSchema(secret_text=decrypted_message)
        
        