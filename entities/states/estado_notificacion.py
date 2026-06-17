"""Entity (Value Object) — Estado abstracto de una Notificacion."""
from abc import ABC


class EstadoNotificacion(ABC):
    """Clase base para los estados del ciclo de vida de una Notificacion."""

    def __init__(self, nombre: str, descripcion: str) -> None:
        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion

    def __repr__(self) -> str:
        return self._nombre
