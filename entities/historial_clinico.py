"""Entity — Historial clínico generado al atender un turno."""
from __future__ import annotations
from datetime import date
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.receta import Receta


class HistorialClinico:
    """
    Registra el resultado de un turno atendido: diagnóstico, tratamiento
    y receta asociada.

    IMPORTANTE: el constructor NO agrega este historial al paciente.
    Esa responsabilidad pertenece al Control (GestorPaciente / GestorTurno).

    Rol ECB: Entity.
    """

    def __init__(self, id_historial: int, id_turno: int, id_paciente: int,
                 diagnostico: str = "", tratamiento: str = "",
                 notas: str = "", observaciones: str = "",
                 fecha_registro: Optional[date] = None) -> None:
        self._id = id_historial
        self._id_turno = id_turno
        self._id_paciente = id_paciente
        self._diagnostico = diagnostico
        self._tratamiento = tratamiento
        self._notas = notas
        self._observaciones = observaciones
        self._fecha_registro = fecha_registro or date.today()
        self._receta: Optional["Receta"] = None

    @property
    def id_historial(self) -> int:
        return self._id

    @property
    def id_turno(self) -> int:
        return self._id_turno

    @property
    def id_paciente(self) -> int:
        return self._id_paciente

    @property
    def diagnostico(self) -> str:
        return self._diagnostico

    @diagnostico.setter
    def diagnostico(self, value: str) -> None:
        self._diagnostico = (value or "").strip()

    @property
    def tratamiento(self) -> str:
        return self._tratamiento

    @tratamiento.setter
    def tratamiento(self, value: str) -> None:
        self._tratamiento = (value or "").strip()

    @property
    def notas(self) -> str:
        return self._notas

    @notas.setter
    def notas(self, value: str) -> None:
        self._notas = (value or "").strip()

    @property
    def observaciones(self) -> str:
        return self._observaciones

    @observaciones.setter
    def observaciones(self, value: str) -> None:
        self._observaciones = (value or "").strip()

    @property
    def fecha_registro(self) -> date:
        return self._fecha_registro

    @property
    def receta(self) -> Optional["Receta"]:
        return self._receta

    def vincular_receta(self, receta: "Receta") -> None:
        """Asocia una receta a este historial."""
        self._receta = receta

    def __repr__(self) -> str:
        return f"HistorialClinico(id={self._id}, turno={self._id_turno}, pac={self._id_paciente})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HistorialClinico):
            return self._id == other._id
        return NotImplemented
