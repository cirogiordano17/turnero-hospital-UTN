"""Control — Casos de uso de gestión de pacientes."""
from __future__ import annotations
from datetime import date

from boundary.persistence.paciente_dao import PacienteDAO
from entities.paciente import Paciente
from entities.exceptions import EntidadNoEncontradaError, DuplicadoError


class GestorPaciente:
    """
    Orquesta los casos de uso de pacientes: alta, baja, modificación,
    consulta de historial clínico.

    Rol ECB: Control.
    """

    def __init__(self, paciente_dao: PacienteDAO) -> None:
        self._paciente_dao = paciente_dao

    def registrar_paciente(self, id_paciente: int, nombre: str, apellido: str,
                           telefono: str, fecha_nacimiento: date,
                           direccion: str) -> Paciente:
        """
        Registra un nuevo paciente.

        Raises:
            DuplicadoError: si ya existe un paciente con ese ID.
        """
        if self._paciente_dao.buscar_por_id(id_paciente):
            raise DuplicadoError(f"Ya existe un paciente con ID {id_paciente}")

        paciente = Paciente(id_paciente, nombre, apellido, telefono,
                            fecha_nacimiento, direccion)

        ok = self._paciente_dao.insertar(
            paciente.id_paciente, paciente.nombre, paciente.apellido,
            paciente.telefono, paciente.fecha_nacimiento, paciente.direccion,
        )
        if not ok:
            raise RuntimeError("No se pudo persistir el paciente")
        return paciente

    def modificar_paciente(self, id_paciente: int, nombre: str, apellido: str,
                           telefono: str, fecha_nacimiento: date,
                           direccion: str) -> Paciente:
        """
        Modifica los datos de un paciente existente.

        Raises:
            EntidadNoEncontradaError: si el paciente no existe.
        """
        if not self._paciente_dao.buscar_por_id(id_paciente):
            raise EntidadNoEncontradaError(f"Paciente #{id_paciente} no encontrado")

        paciente = Paciente(id_paciente, nombre, apellido, telefono,
                            fecha_nacimiento, direccion)

        ok = self._paciente_dao.actualizar(
            paciente.id_paciente, paciente.nombre, paciente.apellido,
            paciente.telefono, paciente.fecha_nacimiento, paciente.direccion,
        )
        if not ok:
            raise RuntimeError("No se pudo actualizar el paciente")
        return paciente

    def dar_de_baja(self, id_paciente: int) -> None:
        """
        Da de baja lógica (soft-delete) a un paciente.

        Raises:
            EntidadNoEncontradaError: si el paciente no existe.
        """
        if not self._paciente_dao.buscar_por_id(id_paciente):
            raise EntidadNoEncontradaError(f"Paciente #{id_paciente} no encontrado")
        self._paciente_dao.dar_de_baja(id_paciente)

    def listar_pacientes(self) -> list[dict]:
        return self._paciente_dao.listar_activos()

    def obtener_historial(self, id_paciente: int) -> list[dict]:
        """Retorna el historial clínico de un paciente."""
        if not self._paciente_dao.buscar_por_id(id_paciente):
            raise EntidadNoEncontradaError(f"Paciente #{id_paciente} no encontrado")
        return self._paciente_dao.obtener_historial(id_paciente)
