from pydantic import BaseModel,Field
import uuid
from datetime import datetime

class RoleSchema(BaseModel):
    title: str 