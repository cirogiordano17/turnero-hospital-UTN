"""Entity (Value Object) — Estado Inasistencia de un turno."""
from .estado_turno import EstadoTurno


class Inasistencia(EstadoTurno):
    """El paciente no asistió al turno. Estado terminal."""

    def __init__(self) -> None:
        super().__init__("Inasistencia", "Paciente no asistió")
