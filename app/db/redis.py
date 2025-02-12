import redis.asyncio as redis
from app.core.config import Config

JTI_EXPIRATION = 3600

redis = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)


async def add_jwt_id_to_blocklist(jwt_id:str) -> None:
    await redis.set(
        name=jwt_id,
        value="",
        ex=JTI_EXPIRATION
    )
    
async def token_in_blocklist(jwt_id:str) -> bool:
    jwt = await redis.get(jwt_id)
    
    return jwt is not None



