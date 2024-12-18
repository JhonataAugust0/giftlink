from cryptography.fernet import Fernet
from src.infrastructure.envs.config import Settings
import base64


encryption_key = Settings.SECRET_ENCRYPTION_KEY
if not encryption_key:
    raise ValueError("A variável de ambiente SECRET_ENCRYPTION_KEY não está definida.")

try:
    SECRET_ENCRYPTION_KEY = base64.urlsafe_b64decode(encryption_key.encode())
except Exception as e:
    raise ValueError(f"A chave de criptografia fornecida não está no formato válido. Erro: {e}")

class KeyServiceManager:
    def __init__(self):
        self.fernet = Fernet(encryption_key)

    async def encrypt_private_key(self, private_key: str) -> str:
        return self.fernet.encrypt(private_key.encode()).decode()

    async def decrypt_private_key(self, encrypted_key: str) -> str:
        return self.fernet.decrypt(encrypted_key.encode()).decode()
    
    async def encrypt_public_key(self, public_key: str) -> str:
        return self.fernet.encrypt(public_key.encode()).decode()
    
    async def decrypt_public_key(self, encrypted_key: str) -> str:
        return self.fernet.decrypt(encrypted_key.encode()).decode()