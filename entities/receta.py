"""Entity — Receta médica emitida en un turno."""
from __future__ import annotations
from datetime import date
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.detalle_receta import DetalleReceta


class Receta:
    """
    Representa una receta médica asociada a un historial clínico.

    Rol ECB: Entity.
    """

    def __init__(self, id_receta: int, id_historial: int,
                 fecha_emision: date, observaciones: str = "") -> None:
        self._id = id_receta
        self._id_historial = id_historial
        self._fecha_emision = fecha_emision
        self._observaciones = observaciones
        self._detalles: List["DetalleReceta"] = []

    @property
    def id_receta(self) -> int:
        return self._id

    @property
    def id_historial(self) -> int:
        return self._id_historial

    @property
    def fecha_emision(self) -> date:
        return self._fecha_emision

    @property
    def observaciones(self) -> str:
        return self._observaciones

    @observaciones.setter
    def observaciones(self, value: str) -> None:
        self._observaciones = (value or "").strip()

    @property
    def detalles(self) -> List["DetalleReceta"]:
        return list(self._detalles)

    def agregar_detalle(self, detalle: "DetalleReceta") -> None:
        """Agrega un medicamento a la receta."""
        if detalle not in self._detalles:
            self._detalles.append(detalle)

    def __repr__(self) -> str:
        return f"Receta(id={self._id}, fecha={self._fecha_emision}, items={len(self._detalles)})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Receta):
            return self._id == other._id
        return NotImplemented
