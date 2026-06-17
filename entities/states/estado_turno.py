"""Entity (Value Object) — Estado abstracto de un turno (Patrón State)."""
from abc import ABC, abstractmethod


class EstadoTurno(ABC):
    """
    Clase base abstracta del Patrón State para el ciclo de vida de un Turno.

    Cada estado concreto (Libre, Programado, Atendido, Cancelado, Inasistencia)
    hereda de esta clase e implementa únicamente las transiciones que le
    corresponden. Los métodos no disponibles lanzan EstadoInvalidoError en la
    subclase o simplemente no existen, lo que fuerza al código cliente a tratar
    cada estado de forma polimórfica.

    Rol ECB: Entity (Value Object — no tiene identidad propia, forma parte de Turno).
    """

    def __init__(self, nombre: str, descripcion: str) -> None:
        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        """Nombre del estado (ej. 'Libre', 'Programado')."""
        return self._nombre

    @property
    def descripcion(self) -> str:
        """Descripción legible del estado."""
        return self._descripcion

    def __repr__(self) -> str:
        return self._nombre

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EstadoTurno):
            return self._nombre == other._nombre
        return NotImplemented
