from passlib.context import CryptContext


passwd_context = CryptContext(
    schemes=["bcrypt"]
)

def generate_passwd_hash(password:str) -> str:
    pass

def verify_passwd(password:str, password_hash:str):
    pass