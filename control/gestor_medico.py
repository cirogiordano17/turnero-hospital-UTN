"""Control — Casos de uso de gestión de médicos."""
from __future__ import annotations
from datetime import date
from typing import Optional

from boundary.persistence.medico_dao import MedicoDAO
from boundary.persistence.especialidad_dao import EspecialidadDAO
from entities.medico import Medico
from entities.exceptions import EntidadNoEncontradaError, DuplicadoError, ValidacionError


class GestorMedico:
    """
    Orquesta los casos de uso de médicos: alta, baja, modificación,
    asignación de especialidades y consultas.

    Rol ECB: Control.
    """

    def __init__(self, medico_dao: MedicoDAO,
                 especialidad_dao: EspecialidadDAO) -> None:
        self._medico_dao = medico_dao
        self._especialidad_dao = especialidad_dao

    def registrar_medico(self, matricula: int, nombre: str, apellido: str,
                         telefono: str, email: str, fecha_alta: date,
                         especialidades_ids: Optional[list[int]] = None) -> Medico:
        """
        Registra un nuevo médico y le asigna especialidades opcionales.

        Raises:
            DuplicadoError: si ya existe un médico con esa matrícula.
            ValidacionError: si los datos no son válidos.
        """
        if self._medico_dao.buscar_por_matricula(matricula):
            raise DuplicadoError(f"Ya existe un médico con matrícula {matricula}")

        medico = Medico(matricula, nombre, apellido, telefono, email, fecha_alta)

        ok = self._medico_dao.insertar(
            medico.matricula, medico.nombre, medico.apellido,
            medico.telefono, medico.email, medico.fecha_alta,
        )
        if not ok:
            raise RuntimeError("No se pudo persistir el médico")

        for esp_id in (especialidades_ids or []):
            self._medico_dao.asignar_especialidad(matricula, esp_id)

        return medico

    def modificar_medico(self, matricula: int, nombre: str, apellido: str,
                          telefono: str, email: str, fecha_alta: date) -> Medico:
        """
        Modifica los datos personales de un médico existente.

        Raises:
            EntidadNoEncontradaError: si el médico no existe.
            ValidacionError: si los datos no son válidos.
        """
        row = self._medico_dao.buscar_por_matricula(matricula)
        if not row:
            raise EntidadNoEncontradaError(f"Médico con matrícula {matricula} no encontrado")

        medico = Medico(matricula, nombre, apellido, telefono, email, fecha_alta)

        ok = self._medico_dao.actualizar(
            medico.matricula, medico.nombre, medico.apellido,
            medico.telefono, medico.email, medico.fecha_alta,
        )
        if not ok:
            raise RuntimeError("No se pudo actualizar el médico")
        return medico

    def dar_de_baja(self, matricula: int) -> None:
        """
        Da de baja lógica (soft-delete) a un médico.

        Raises:
            EntidadNoEncontradaError: si el médico no existe.
        """
        row = self._medico_dao.buscar_por_matricula(matricula)
        if not row:
            raise EntidadNoEncontradaError(f"Médico con matrícula {matricula} no encontrado")
        self._medico_dao.dar_de_baja(matricula)

    def asignar_especialidad(self, matricula: int, id_especialidad: int) -> None:
        """Asocia una especialidad a un médico."""
        if not self._medico_dao.buscar_por_matricula(matricula):
            raise EntidadNoEncontradaError(f"Médico {matricula} no encontrado")
        if not self._especialidad_dao.buscar_por_id(id_especialidad):
            raise EntidadNoEncontradaError(f"Especialidad {id_especialidad} no encontrada")
        self._medico_dao.asignar_especialidad(matricula, id_especialidad)

    def listar_medicos(self) -> list[dict]:
        return self._medico_dao.listar_activos()

    def obtener_medico(self, matricula: int) -> dict:
        row = self._medico_dao.buscar_por_matricula(matricula)
        if not row:
            raise EntidadNoEncontradaError(f"Médico {matricula} no encontrado")
        return row
