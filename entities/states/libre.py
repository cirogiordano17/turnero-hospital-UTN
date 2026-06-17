"""Entity (Value Object) — Estado Libre de un turno."""
from .estado_turno import EstadoTurno


class Libre(EstadoTurno):
    """Turno disponible para ser asignado a un paciente."""

    def __init__(self) -> None:
        super().__init__("Libre", "Turno disponible para programar")

    def programar(self) -> "Programado":  # type: ignore[name-defined]
        """Transiciona al estado Programado."""
        from .programado import Programado
        return Programado()
