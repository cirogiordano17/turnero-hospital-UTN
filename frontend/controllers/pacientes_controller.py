"""Boundary (UI) — Adaptador delgado entre la vista de Pacientes y GestorPaciente."""
from __future__ import annotations
from datetime import date

from boundary.persistence.database import Database
from boundary.persistence.paciente_dao import PacienteDAO
from control.gestor_paciente import GestorPaciente
from entities.exceptions import EntidadNoEncontradaError, DuplicadoError, ValidacionError


def _build_gestor() -> GestorPaciente:
    return GestorPaciente(PacienteDAO(Database()))


class PacientesController:
    """Boundary (UI) — Delega en GestorPaciente. Sin lógica de negocio."""

    def __init__(self) -> None:
        self._gestor = _build_gestor()

    def crear(self, nro, nombre, apellido, tel, nacimiento, direccion) -> tuple[bool, str]:
        try:
            self._gestor.registrar_paciente(
                int(nro), nombre, apellido, tel,
                date.fromisoformat(nacimiento), direccion,
            )
            return True, "Paciente creado exitosamente"
        except (DuplicadoError, ValidacionError) as e:
            return False, str(e)
        except ValueError:
            return False, "ID o fecha inválida"
        except Exception as e:
            return False, f"Error: {e}"

    def modificar(self, id_paciente, nombre, apellido, telefono,
                  nacimiento, direccion) -> tuple[bool, str]:
        try:
            self._gestor.modificar_paciente(
                int(id_paciente), nombre, apellido, telefono,
                date.fromisoformat(nacimiento), direccion,
            )
            return True, "Paciente modificado exitosamente"
        except (EntidadNoEncontradaError, ValidacionError) as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error: {e}"

    def dar_de_baja(self, id_paciente) -> tuple[bool, str]:
        try:
            self._gestor.dar_de_baja(int(id_paciente))
            return True, "Paciente dado de baja"
        except EntidadNoEncontradaError as e:
            return False, str(e)

    def dar_de_baja_paciente(self, id_paciente) -> tuple[bool, str]:
        return self.dar_de_baja(id_paciente)

    def listar(self) -> list[dict]:
        return [
            {"id": r["id_paciente"], "nombre": r["nombre"],
             "apellido": r["apellido"], "telefono": r["telefono"],
             "nacimiento": str(r["fecha_nacimiento"]), "direccion": r["direccion"]}
            for r in self._gestor.listar_pacientes()
        ]

    def obtener_pacientes(self) -> list[dict]:
        return self.listar()

    def obtener_historial(self, id_paciente) -> list[dict]:
        try:
            return self._gestor.obtener_historial(int(id_paciente))
        except EntidadNoEncontradaError:
            return []
