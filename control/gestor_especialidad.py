"""Control — Casos de uso de gestión de especialidades."""
from __future__ import annotations
from typing import Optional

from boundary.persistence.especialidad_dao import EspecialidadDAO
from entities.especialidad import Especialidad
from entities.exceptions import EntidadNoEncontradaError, DuplicadoError


class GestorEspecialidad:
    """Rol ECB: Control."""

    def __init__(self, especialidad_dao: EspecialidadDAO) -> None:
        self._especialidad_dao = especialidad_dao

    def crear_especialidad(self, nombre: str, descripcion: str = "") -> Especialidad:
        especialidad = Especialidad(0, nombre, descripcion)
        id_nuevo = self._especialidad_dao.insertar(especialidad.nombre, especialidad.descripcion)
        if not id_nuevo:
            raise RuntimeError("No se pudo crear la especialidad")
        return Especialidad(id_nuevo, nombre, descripcion)

    def modificar_especialidad(self, id_especialidad: int, nombre: str,
                                descripcion: str) -> Especialidad:
        if not self._especialidad_dao.buscar_por_id(id_especialidad):
            raise EntidadNoEncontradaError(f"Especialidad #{id_especialidad} no encontrada")
        especialidad = Especialidad(id_especialidad, nombre, descripcion)
        self._especialidad_dao.actualizar(id_especialidad, especialidad.nombre,
                                          especialidad.descripcion)
        return especialidad

    def eliminar_especialidad(self, id_especialidad: int) -> None:
        if not self._especialidad_dao.buscar_por_id(id_especialidad):
            raise EntidadNoEncontradaError(f"Especialidad #{id_especialidad} no encontrada")
        self._especialidad_dao.eliminar(id_especialidad)

    def listar_especialidades(self) -> list[dict]:
        return self._especialidad_dao.listar_todas()
