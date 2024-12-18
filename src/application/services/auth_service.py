from typing import Dict
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
from src.adapters.output.data.orm.repositories.key_repository_orm import KeysRepositoryORM
from src.application.services.keys_service import KeyServiceManager 
from src.application.use_cases.key_use_case import KeyUseCase 
from cryptography.hazmat.primitives import serialization
from jose import ExpiredSignatureError, jwt


class JWTService:
    def __init__(self):
        self.key_manager = KeyServiceManager()

    async def get_key_repository(self) -> KeyUseCase:
            global use_case
            use_case = await KeysRepositoryORM().create_instance()
            return KeyUseCase(use_case)
    
    async def get_or_create_keys(self, user_id: int):
            await self.get_key_repository()
            # Verifica se as chaves existem
            row = await use_case.get_key_by_user_id(user_id)
            if row:
                # Descriptografa a chave privada
                private_key = await self.key_manager.decrypt_private_key(row.private_key)
                public_key = row.public_key
            else:
                # Gera novo par de chaves
                private_key_obj = rsa.generate_private_key(public_exponent=65537, key_size=2048)
                public_key_obj = private_key_obj.public_key()

                # Serializa chaves
                private_key = private_key_obj.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ).decode()

                public_key = public_key_obj.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ).decode()

                # Criptografa a chave privada antes de armazenar
                encrypted_private_key = await self.key_manager.encrypt_private_key(private_key)
                # Salva as chaves no banco
                await use_case.insert_key(public_key, encrypted_private_key, user_id)

            return private_key, public_key

    def create_access_token(self, data: Dict[str, str], private_key, expires_delta: timedelta = timedelta(minutes=120)) -> str:
        """
        Cria um token JWT assinado com a chave privada
        """
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})

        # Converte datetime para timestamp
        to_encode['exp'] = int(to_encode['exp'].timestamp())

        # Assina o token com a chave privada
        token = jwt.encode(
            to_encode, 
            private_key,
            algorithm='RS256'
        )
        return token

    def validate_token(self, token: str, public_key: str) -> Dict[str, str]:
        """
        Valida o token usando a chave pública
        """
        try:
            payload = jwt.decode(
                token, 
                public_key, 
                algorithms=['RS256']
            )
            return payload
        except ExpiredSignatureError:
            raise ValueError("Token expirado")