import aiosmtplib
from email.mime.text import MIMEText
from src.infrastructure.envs.config import Settings

class EmailService:
    @staticmethod
    async def send_recovery_email(to_email: str, recovery_link: str):
        message = MIMEText(f"""
        Você solicitou a recuperação de senha. 
        Clique no link abaixo para redefinir:
        {recovery_link}
        
        Este link expirará em 24 horas.
        """)
        
        message['Subject'] = 'Recuperação de Senha'
        message['From'] = Settings.SMTP_USERNAME
        message['To'] = to_email

        async with aiosmtplib.SMTP(
            hostname=Settings.SMTP_SERVER, 
            port=Settings.SMTP_PORT
        ) as smtp:
            await smtp.starttls()
            await smtp.login(Settings.SMTP_USERNAME, Settings.SMTP_PASSWORD)
            await smtp.send_message(message)