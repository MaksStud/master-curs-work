from fastapi_mail import FastMail, ConnectionConfig
from core.config import settings

conf = ConnectionConfig(
    mail_from=settings.mail_from,
    mail_password=settings.mail_password,
    mail_server=settings.mail_server,
    mail_port=settings.mail_port,
    mail_tls=settings.mail_tls,
    mail_ssl=settings.mail_ssl,
    use_credentials=settings.use_credentials,
    validate_certs=settings.validate_certs
)

mail_app = FastMail(conf)
