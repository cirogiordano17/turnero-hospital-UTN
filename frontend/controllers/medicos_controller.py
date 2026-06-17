"""Boundary (UI) — Adaptador delgado entre la vista de Médicos y GestorMedico."""
from __future__ import annotations
from datetime import date

from boundary.persistence.database import Database
from boundary.persistence.medico_dao import MedicoDAO
from boundary.persistence.especialidad_dao import EspecialidadDAO
from control.gestor_medico import GestorMedico
from entities.exceptions import EntidadNoEncontradaError, DuplicadoError, ValidacionError


def _build_gestor() -> GestorMedico:
    db = Database()
    return GestorMedico(MedicoDAO(db), EspecialidadDAO(db))


class MedicosController:
    """Boundary (UI) — Delega en GestorMedico. Sin lógica de negocio."""

    def __init__(self) -> None:
        self._gestor = _build_gestor()

    def crear(self, matricula, nombre, apellido, tel, email,
              fecha_alta, especialidades_ids=None) -> tuple[bool, str]:
        try:
            self._gestor.registrar_medico(
                int(matricula), nombre, apellido, tel, email,
                date.fromisoformat(fecha_alta),
                especialidades_ids=[int(e) for e in (especialidades_ids or [])],
            )
            return True, "Médico creado exitosamente"
        except (DuplicadoError, ValidacionError) as e:
            return False, str(e)
        except ValueError:
            return False, "Matrícula o fecha inválida"
        except Exception as e:
            return False, f"Error: {e}"

    def modificar(self, matricula, nombre, apellido, telefono, email,
                  fecha_alta) -> tuple[bool, str]:
        try:
            self._gestor.modificar_medico(
                int(matricula), nombre, apellido, telefono, email,
                date.fromisoformat(fecha_alta),
            )
            return True, "Médico modificado exitosamente"
        except (EntidadNoEncontradaError, ValidacionError) as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error: {e}"

    def dar_de_baja(self, matricula) -> tuple[bool, str]:
        try:
            self._gestor.dar_de_baja(int(matricula))
            return True, "Médico dado de baja"
        except EntidadNoEncontradaError as e:
            return False, str(e)

    def listar(self) -> list[dict]:
        rows = self._gestor.listar_medicos()
        return [
            {"matricula": r["matricula"], "nombre": r["nombre"],
             "apellido": r["apellido"], "telefono": r["telefono"],
             "email": r["email"], "fecha_alta": str(r["fecha_ingreso"])}
            for r in rows
        ]
