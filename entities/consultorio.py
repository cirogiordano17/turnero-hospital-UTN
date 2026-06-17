"""Entity — Consultorio físico del hospital."""
from __future__ import annotations
from entities.exceptions import ValidacionError


class Consultorio:
    """
    Representa un consultorio físico donde se realizan los turnos.

    Rol ECB: Entity.
    """

    def __init__(self, id_consultorio: int, numero: int, piso: int,
                 equipamiento: str = "") -> None:
        self._id = id_consultorio
        self._numero = numero
        self._piso = piso
        self.equipamiento = equipamiento

    @property
    def id_consultorio(self) -> int:
        return self._id

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def piso(self) -> int:
        return self._piso

    @property
    def equipamiento(self) -> str:
        return self._equipamiento

    @equipamiento.setter
    def equipamiento(self, value: str) -> None:
        self._equipamiento = (value or "").strip()

    def __repr__(self) -> str:
        return f"Consultorio(nro={self._numero}, piso={self._piso})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Consultorio):
            return self._id == other._id
        return NotImplemented
