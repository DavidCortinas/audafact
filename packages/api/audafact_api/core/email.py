from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from ..config import settings
from pathlib import Path

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "email_templates",
)

fastmail = FastMail(conf)


async def send_verification_email(email: str, code: str):
    message = MessageSchema(
        subject="Verify your email for Audafact",
        recipients=[email],
        template_body={"code": code},
        subtype="html",
    )

    await fastmail.send_message(message, template_name="verification.html")
