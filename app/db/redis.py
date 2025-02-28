import redis.asyncio as redis
from app.core.config import Config
import json
JTI_EXPIRATION = 3600

redis = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

async def store_secrets(key:str,value:dict,expiration:int):
    json_data = json.dumps(value)
    return await redis.set(
        name=key,
        value=json_data,
        ex=expiration
    )
    
async def get_secret(key:str) -> dict | None:
    secret = await redis.get(key)
    
    return json.loads(secret) if secret else None    
    
async def delete_secret(key:str) -> None:
    
    await redis.delete(key)
    

async def add_jwt_id_to_blocklist(jwt_id:str) -> None:
    await redis.set(
        name=jwt_id,
        value="",
        ex=JTI_EXPIRATION
    )
    
async def token_in_blocklist(jwt_id:str) -> bool:
    jwt = await redis.get(jwt_id)
    
    return jwt is not None



