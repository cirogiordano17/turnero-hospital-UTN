"""Entity — Especialidad médica."""
from __future__ import annotations
from entities.exceptions import ValidacionError


class Especialidad:
    """
    Representa una especialidad médica (Cardiología, Pediatría, etc.).

    Actúa como un catálogo: los médicos se asocian a especialidades
    y los pacientes buscan turnos filtrando por ellas.

    Rol ECB: Entity.
    """

    def __init__(self, id_especialidad: int, nombre: str, descripcion: str = "") -> None:
        self._id = id_especialidad
        self.nombre = nombre
        self.descripcion = descripcion

    # -- Identidad --

    @property
    def id_especialidad(self) -> int:
        return self._id

    # -- Atributos --

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value or not value.strip():
            raise ValidacionError("El nombre de la especialidad no puede estar vacío")
        self._nombre = value.strip()

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value: str) -> None:
        self._descripcion = (value or "").strip()

    def __repr__(self) -> str:
        return f"Especialidad(id={self._id}, nombre='{self._nombre}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Especialidad):
            return self._id == other._id
        return NotImplemented
