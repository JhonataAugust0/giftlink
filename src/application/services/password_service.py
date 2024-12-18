import secrets
import hashlib
import base64

class PasswordService:
    @classmethod
    def generate_salt(cls, length: int = 16) -> str:
        return secrets.token_hex(length // 2)

    @classmethod
    def hash_password(cls, password: str, salt: str) -> str:
        password_salt = f"{password}:{salt}".encode('utf-8')
        sha256_hash = hashlib.sha256(password_salt).digest()
        return base64.b64encode(sha256_hash).decode('utf-8')

    @classmethod
    def verify_password(cls, stored_password: str, provided_password: str) -> bool:
        salt, stored_hash = stored_password.split(':')  
        hashed_provided = PasswordService.hash_password(provided_password, salt)
        return secrets.compare_digest(stored_hash, hashed_provided)
    