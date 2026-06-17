"""Entity — Notificación de recordatorio de turno."""
from __future__ import annotations
from datetime import datetime
from entities.states.estado_notificacion import EstadoNotificacion
from entities.states.notificacion_pendiente import Pendiente
from entities.states.notificacion_enviada import Enviado
from entities.states.notificacion_error import Error


class Notificacion:
    """
    Representa una notificación programada para recordar a un paciente
    su turno (vía email, SMS, etc.).

    El ciclo de vida: Pendiente → Enviado / Error.

    IMPORTANTE: el constructor NO agrega esta notificación al Turno.
    Esa lógica pertenece al GestorNotificacion (Control).

    Rol ECB: Entity.
    """

    def __init__(self, id_notificacion: int, id_turno: int,
                 fecha_hora_envio: datetime, medio_envio: str,
                 estado: str = "Pendiente", intentos: int = 0) -> None:
        self._id = id_notificacion
        self._id_turno = id_turno
        self._fecha_hora_envio = fecha_hora_envio
        self._medio_envio = medio_envio
        self._estado: EstadoNotificacion = self._estado_desde_string(estado)
        self._intentos = intentos

    @property
    def id_notificacion(self) -> int:
        return self._id

    @property
    def id_turno(self) -> int:
        return self._id_turno

    @property
    def fecha_hora_envio(self) -> datetime:
        return self._fecha_hora_envio

    @property
    def medio_envio(self) -> str:
        return self._medio_envio

    @property
    def estado(self) -> EstadoNotificacion:
        return self._estado

    @property
    def intentos(self) -> int:
        return self._intentos

    def marcar_enviado(self) -> None:
        self._estado = Enviado()

    def marcar_error(self) -> None:
        self._estado = Error()
        self._intentos += 1

    def reintentar(self) -> None:
        self._estado = Pendiente()

    @staticmethod
    def _estado_desde_string(nombre: str) -> EstadoNotificacion:
        mapa = {"Pendiente": Pendiente, "Enviado": Enviado, "Error": Error}
        cls = mapa.get(nombre, Pendiente)
        return cls()

    def __repr__(self) -> str:
        return f"Notificacion(id={self._id}, turno={self._id_turno}, estado={self._estado.nombre})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Notificacion):
            return self._id == other._id
        return NotImplemented
