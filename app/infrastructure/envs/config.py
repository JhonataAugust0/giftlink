import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # JWT Settings
    JWT_ALGORITHM:                str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES:  int = 30
    RECOVERY_TOKEN_EXPIRE_HOURS:  int = 24
    SECRET_KEY:                   str = os.environ.get('SECRET_KEY', 'fallback_secret_key')
    
    # Email SMTP Settings
    SMTP_PORT:                    int = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USERNAME:                str = os.environ.get('SMTP_USERNAME', '')
    SMTP_PASSWORD:                str = os.environ.get('SMTP_PASSWORD', '')
    SMTP_SERVER:                  str = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    
    # Database Settings
    POSTGRES_URL:                 str = os.environ.get('POSTGRES_URL')
