"""Entity — Línea de prescripción dentro de una Receta."""
from __future__ import annotations
from entities.exceptions import ValidacionError


class DetalleReceta:
    """
    Representa un medicamento prescripto en una receta.

    IMPORTANTE: el constructor NO agrega este detalle a la receta padre.
    Esa lógica pertenece al GestorReceta (Control).

    Rol ECB: Entity.
    """

    def __init__(self, id_detalle: int, id_receta: int, id_medicamento: int,
                 cantidad: int, dosis: str, indicaciones: str = "") -> None:
        if cantidad <= 0:
            raise ValidacionError("La cantidad debe ser mayor a cero")
        self._id = id_detalle
        self._id_receta = id_receta
        self._id_medicamento = id_medicamento
        self._cantidad = cantidad
        self.dosis = dosis
        self.indicaciones = indicaciones

    @property
    def id_detalle(self) -> int:
        return self._id

    @property
    def id_receta(self) -> int:
        return self._id_receta

    @property
    def id_medicamento(self) -> int:
        return self._id_medicamento

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def dosis(self) -> str:
        return self._dosis

    @dosis.setter
    def dosis(self, value: str) -> None:
        if not value or not value.strip():
            raise ValidacionError("La dosis no puede estar vacía")
        self._dosis = value.strip()

    @property
    def indicaciones(self) -> str:
        return self._indicaciones

    @indicaciones.setter
    def indicaciones(self, value: str) -> None:
        self._indicaciones = (value or "").strip()

    def __repr__(self) -> str:
        return f"DetalleReceta(med={self._id_medicamento}, cant={self._cantidad}, dosis='{self._dosis}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DetalleReceta):
            return self._id == other._id
        return NotImplemented
