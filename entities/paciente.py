"""Entity — Paciente del sistema."""
from __future__ import annotations
from datetime import date
from entities.exceptions import ValidacionError


class Paciente:
    """
    Representa un paciente con sus datos personales.

    Rol ECB: Entity.
    """

    def __init__(self, id_paciente: int, nombre: str, apellido: str,
                 telefono: str, fecha_nacimiento: date, direccion: str) -> None:
        self._id = id_paciente
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self._fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion

    # -- Identidad --

    @property
    def id_paciente(self) -> int:
        return self._id

    # -- Atributos modificables --

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value or not value.strip():
            raise ValidacionError("El nombre no puede estar vacío")
        self._nombre = value.strip()

    @property
    def apellido(self) -> str:
        return self._apellido

    @apellido.setter
    def apellido(self, value: str) -> None:
        if not value or not value.strip():
            raise ValidacionError("El apellido no puede estar vacío")
        self._apellido = value.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, value: str) -> None:
        self._telefono = (value or "").strip()

    @property
    def fecha_nacimiento(self) -> date:
        return self._fecha_nacimiento

    @property
    def direccion(self) -> str:
        return self._direccion

    @direccion.setter
    def direccion(self, value: str) -> None:
        self._direccion = (value or "").strip()

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"

    def __repr__(self) -> str:
        return f"Paciente(id={self._id}, nombre='{self.nombre_completo}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Paciente):
            return self._id == other._id
        return NotImplemented
