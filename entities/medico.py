"""Entity — Médico del sistema."""
from __future__ import annotations
from datetime import date
from typing import Optional
from entities.exceptions import ValidacionError


class Medico:
    """
    Representa un médico con sus datos personales y estado de actividad.

    Responsabilidad única: mantener el estado válido de los datos del médico.
    La lógica de negocio (buscar turnos, asignar especialidades) pertenece
    al Control (GestorMedico).

    Rol ECB: Entity.
    """

    def __init__(self, matricula: int, nombre: str, apellido: str,
                 telefono: str, email: str, fecha_alta: date,
                 fecha_baja: Optional[date] = None) -> None:
        self._matricula = matricula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self._fecha_alta = fecha_alta
        self._fecha_baja = fecha_baja

    # -- Identidad --

    @property
    def matricula(self) -> int:
        return self._matricula

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
        if not value or not value.strip():
            raise ValidacionError("El teléfono no puede estar vacío")
        self._telefono = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if not value or "@" not in value or "." not in value.split("@")[-1]:
            raise ValidacionError(f"El email '{value}' no es válido")
        self._email = value.strip().lower()

    # -- Atributos de ciclo de vida --

    @property
    def fecha_alta(self) -> date:
        return self._fecha_alta

    @property
    def fecha_baja(self) -> Optional[date]:
        return self._fecha_baja

    @fecha_baja.setter
    def fecha_baja(self, value: Optional[date]) -> None:
        if value is not None and value < self._fecha_alta:
            raise ValidacionError("La fecha de baja no puede ser anterior a la fecha de alta")
        self._fecha_baja = value

    @property
    def esta_activo(self) -> bool:
        """True si el médico no ha sido dado de baja."""
        return self._fecha_baja is None

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"

    def __repr__(self) -> str:
        return f"Medico(mat={self._matricula}, nombre='{self.nombre_completo}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Medico):
            return self._matricula == other._matricula
        return NotImplemented
