"""Entity (Value Object) — Registro de una transición de estado en un Turno."""
from datetime import datetime
from .estado_turno import EstadoTurno


class CambioEstado:
    """
    Registro inmutable de una transición de estado.

    Actúa como un log de auditoría: documenta cuándo ocurrió cada cambio
    y hacia qué estado. Al ser inmutable (sin setters), garantiza la
    integridad del historial.

    Rol ECB: Entity (Value Object).
    """

    def __init__(self, estado: EstadoTurno, fecha_hora: datetime | None = None) -> None:
        self._estado = estado
        self._fecha_hora = fecha_hora or datetime.now()

    @property
    def estado(self) -> EstadoTurno:
        """Estado al que se transitó."""
        return self._estado

    @property
    def fecha_hora(self) -> datetime:
        """Momento exacto del cambio."""
        return self._fecha_hora

    def __repr__(self) -> str:
        return f"CambioEstado({self._estado.nombre} @ {self._fecha_hora:%d/%m/%Y %H:%M})"
