import bcrypt
# from passlib.hash import bcrypt
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        print(f"Password verification error: {e}")
        return False