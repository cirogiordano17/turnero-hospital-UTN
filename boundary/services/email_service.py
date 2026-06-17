"""Boundary (Servicio externo) — Envío de emails via SMTP."""
from __future__ import annotations
import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


class EmailService:
    """
    Encapsula el envío de emails via Gmail SMTP.

    Al separar esta responsabilidad del GestorNotificacion, podemos:
    - Reemplazar el proveedor de SMTP sin tocar la lógica de negocio.
    - Hacer mocking en tests sin conectarse a servidores externos.

    Rol ECB: Boundary (Servicio externo).
    """

    def __init__(self) -> None:
        self._sender = os.getenv("EMAIL_SENDER", "")
        self._password = os.getenv("EMAIL_PASSWORD", "")

    @property
    def configurado(self) -> bool:
        """True si las credenciales están disponibles."""
        return bool(self._sender and self._password)

    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> tuple[bool, str]:
        """
        Envía un email de texto plano.

        Returns:
            (True, mensaje_ok) o (False, descripcion_error)
        """
        if not self.configurado:
            return False, "Credenciales de email no configuradas en .env"

        try:
            msg = MIMEMultipart()
            msg["From"] = self._sender
            msg["To"] = destinatario
            msg["Subject"] = asunto
            msg.attach(MIMEText(cuerpo, "plain", "utf-8"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(self._sender, self._password)
                server.send_message(msg)

            return True, f"Email enviado a {destinatario}"

        except smtplib.SMTPAuthenticationError:
            return False, "Credenciales de Gmail incorrectas o App Password requerida"
        except Exception as exc:
            logger.error("Error al enviar email a %s: %s", destinatario, exc)
            return False, f"Error al enviar email: {exc}"
