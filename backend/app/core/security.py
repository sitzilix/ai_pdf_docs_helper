import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    
    password_bytes = password.encode("utf-8")
    
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    return hashed.decode("utf-8")