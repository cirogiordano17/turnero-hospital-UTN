"""Entity (Value Object) — Estado Programado de un turno."""
from .estado_turno import EstadoTurno


class Programado(EstadoTurno):
    """Turno reservado para un paciente específico."""

    def __init__(self) -> None:
        super().__init__("Programado", "Turno reservado")

    def cancelar(self) -> "Cancelado":  # type: ignore[name-defined]
        """Transiciona al estado Cancelado."""
        from .cancelado import Cancelado
        return Cancelado()

    def atender(self) -> "Atendido":  # type: ignore[name-defined]
        """Transiciona al estado Atendido."""
        from .atendido import Atendido
        return Atendido()

    def marcar_inasistencia(self) -> "Inasistencia":  # type: ignore[name-defined]
        """Transiciona al estado Inasistencia."""
        from .inasistencia import Inasistencia
        return Inasistencia()
