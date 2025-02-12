from passlib.context import CryptContext


passwd_context = CryptContext(
    schemes=["bcrypt"]
)

def generate_passwd_hash(password:str) -> str:
    pass