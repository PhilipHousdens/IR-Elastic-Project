# Utility function to hash passwords
def hash_password(password: str) -> str:
    return hash.bcrypt.hash(password)

# Utility function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash.bcrypt.verify(plain_password, hashed_password)
