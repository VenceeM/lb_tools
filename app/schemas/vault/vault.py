from pydantic import BaseModel


class VaultSchema(BaseModel):
    secret_text: str