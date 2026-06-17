"""Entity (Value Object) — Estado Cancelado de un turno."""
from .estado_turno import EstadoTurno


class Cancelado(EstadoTurno):
    """Turno cancelado. Puede liberarse para reutilizarlo."""

    def __init__(self) -> None:
        super().__init__("Cancelado", "Turno cancelado")

    def liberar(self) -> "Libre":  # type: ignore[name-defined]
        """Transiciona al estado Libre para reutilizar el slot."""
        from .libre import Libre
        return Libre()
