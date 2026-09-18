from fastapi_mail import FastMail, ConnectionConfig
from core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_FROM=settings.mail_from,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_SERVER=settings.mail_server,
    MAIL_PORT=settings.mail_port,
    MAIL_STARTTLS=settings.mail_tls,
    MAIL_SSL_TLS=settings.mail_ssl,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs
)

mail_app = FastMail(conf)
