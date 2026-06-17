"""Control — Casos de uso de notificaciones de turno."""
from __future__ import annotations
from datetime import datetime, timedelta
import logging

from boundary.persistence.notificacion_dao import NotificacionDAO
from boundary.persistence.paciente_dao import PacienteDAO
from boundary.services.email_service import EmailService

logger = logging.getLogger(__name__)


class GestorNotificacion:
    """
    Orquesta la creación, envío y seguimiento de notificaciones de turno.

    Separa claramente:
    - NotificacionDAO (persiste/lee estado de notificaciones)
    - EmailService (envía el email)
    - Esta clase (decide cuándo y cómo enviar)

    Rol ECB: Control.
    """

    def __init__(self, notificacion_dao: NotificacionDAO,
                 paciente_dao: PacienteDAO,
                 email_service: EmailService) -> None:
        self._notificacion_dao = notificacion_dao
        self._paciente_dao = paciente_dao
        self._email_service = email_service

    def crear_notificacion_turno(self, id_turno: int, fecha_turno,
                                  hora_turno, id_paciente: int,
                                  contacto_override: str = "") -> bool:
        """
        Programa una notificación 24 h antes del turno.

        Args:
            contacto_override: email manual; si se omite, se usa el contacto principal del paciente.
        """
        if contacto_override:
            medio = "Email"
            valor = contacto_override
        else:
            contacto = self._paciente_dao.obtener_contacto_principal(id_paciente)
            if not contacto:
                logger.warning("Paciente %s sin contacto registrado", id_paciente)
                return False
            medio = contacto["tipo_contacto"]
            valor = contacto["valor_contacto"]

        hora_dt = self._timedelta_to_time(hora_turno)
        fecha_hora_turno = datetime.combine(fecha_turno, hora_dt)
        fecha_hora_envio = fecha_hora_turno - timedelta(hours=24)

        id_notif = self._notificacion_dao.insertar(id_turno, fecha_hora_envio, medio)
        return id_notif is not None

    def procesar_pendientes(self) -> tuple[int, int]:
        """
        Obtiene y envía todas las notificaciones pendientes vencidas.

        Returns:
            (enviadas, fallidas)
        """
        pendientes = self._notificacion_dao.obtener_pendientes()
        enviadas = fallidas = 0

        for notif in pendientes:
            if self._procesar_una(notif):
                enviadas += 1
            else:
                fallidas += 1

        return enviadas, fallidas

    def _procesar_una(self, notif: dict) -> bool:
        id_notif = notif["id_notificacion"]
        medio = notif["medio_envio"]
        id_paciente = notif["id_paciente"]

        contacto = self._paciente_dao.obtener_contacto_principal(id_paciente)
        if not contacto or contacto["tipo_contacto"] != medio:
            self._notificacion_dao.marcar_error(id_notif, f"Sin contacto tipo {medio}")
            return False

        destinatario = contacto["valor_contacto"]
        fecha_str = notif["fecha"].strftime("%d/%m/%Y")
        hora_str = self._format_hora(notif["hora_inicio"])
        asunto = f"Recordatorio de Turno Médico - {fecha_str}"
        cuerpo = (
            f"Estimado/a {notif['nombre']} {notif['apellido']}:\n\n"
            f"Le recordamos su turno médico:\n"
            f"  Fecha: {fecha_str}\n"
            f"  Hora: {hora_str}\n"
            f"  Médico: Dr/a. {notif['medico_nombre']} {notif['medico_apellido']}\n\n"
            "Por favor, llegue 10 minutos antes.\n\n"
            "Sistema de Turnos — Hospital DAO"
        )

        if medio == "Email":
            ok, msg = self._email_service.enviar(destinatario, asunto, cuerpo)
        else:
            ok, msg = False, f"Medio '{medio}' no implementado"

        if ok:
            self._notificacion_dao.marcar_enviado(id_notif)
        else:
            self._notificacion_dao.incrementar_intento(id_notif, msg)

        return ok

    @staticmethod
    def _timedelta_to_time(valor):
        from datetime import time as time_t
        if isinstance(valor, timedelta):
            s = int(valor.total_seconds())
            return time_t(s // 3600, (s % 3600) // 60)
        return valor

    @staticmethod
    def _format_hora(valor) -> str:
        if isinstance(valor, timedelta):
            s = int(valor.total_seconds())
            return f"{s // 3600:02d}:{(s % 3600) // 60:02d}"
        return str(valor)[:5]
