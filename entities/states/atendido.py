"""Entity (Value Object) — Estado Atendido de un turno."""
from .estado_turno import EstadoTurno


class Atendido(EstadoTurno):
    """Turno en el que el paciente fue atendido. Estado terminal."""

    def __init__(self) -> None:
        super().__init__("Atendido", "Paciente atendido")
