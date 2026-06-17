"""
Boundary (UI) — Adaptador delgado entre la vista de Turnos y GestorTurno.

Responsabilidad única: traducir las llamadas de la UI al Control.
No contiene lógica de negocio ni queries SQL.
"""
from __future__ import annotations
from typing import Optional

from boundary.persistence.database import Database
from boundary.persistence.turno_dao import TurnoDAO
from boundary.persistence.medico_dao import MedicoDAO
from boundary.persistence.paciente_dao import PacienteDAO
from control.gestor_turno import GestorTurno
from entities.exceptions import EntidadNoEncontradaError, EstadoInvalidoError


def _build_gestor() -> GestorTurno:
    db = Database()
    return GestorTurno(TurnoDAO(db), MedicoDAO(db), PacienteDAO(db))


class TurnoController:
    """Boundary (UI) — Delega en GestorTurno. Sin lógica de negocio."""

    def __init__(self) -> None:
        self._gestor = _build_gestor()

    def obtener_medicos(self) -> list[dict]:
        db = Database()
        with db:
            return db.obtener_registros(
                "SELECT matricula, nombre, apellido FROM Medico WHERE activo=1"
                " ORDER BY nombre, apellido"
            )

    def obtener_pacientes(self) -> list[dict]:
        db = Database()
        with db:
            return db.obtener_registros(
                "SELECT id_paciente, nombre, apellido FROM Paciente WHERE activo=1"
                " ORDER BY nombre, apellido"
            )

    def obtener_turnos_libres_medico(self, matricula: int) -> list[dict]:
        return self._gestor.obtener_turnos_libres(matricula)

    def obtener_turnos_con_doble_filtro(self, filtro_fecha: str = "todos",
                                         filtro_estado: str = "todos_estados") -> list[dict]:
        return self._gestor.obtener_turnos_filtrados(filtro_fecha, filtro_estado)

    def obtener_turnos_filtrados(self, filtro: str = "todos") -> list[dict]:
        mapa = {
            "hoy": ("hoy", "todos_estados"),
            "programados": ("todos", "programados"),
            "futuros": ("proximos", "programados"),
            "atendidos": ("todos", "atendidos"),
            "cancelados": ("todos", "cancelados"),
            "inasistencia": ("todos", "inasistencia"),
        }
        f_fecha, f_estado = mapa.get(filtro, ("todos", "todos_estados"))
        return self._gestor.obtener_turnos_filtrados(f_fecha, f_estado)

    def programar_turno_con_especialidad(self, id_paciente: int, matricula: int,
                                          id_turno: int, id_especialidad: int,
                                          observaciones: str = "") -> tuple[bool, str]:
        try:
            self._gestor.programar_turno(id_turno, id_paciente, id_especialidad, observaciones)
            return True, "Turno programado exitosamente"
        except (EntidadNoEncontradaError, EstadoInvalidoError) as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error inesperado: {e}"

    def programar_turno(self, id_paciente: int, matricula: int, id_turno: int,
                        observaciones: str = "") -> tuple[bool, str]:
        return self.programar_turno_con_especialidad(
            id_paciente, matricula, id_turno, None, observaciones
        )

    def cancelar_turno(self, id_turno: int) -> tuple[bool, str]:
        try:
            self._gestor.cancelar_turno(id_turno)
            return True, "Turno cancelado"
        except (EntidadNoEncontradaError, EstadoInvalidoError) as e:
            return False, str(e)

    def cambiar_estado_turno(self, id_turno: int, nuevo_estado: str) -> tuple[bool, str]:
        from boundary.persistence.turno_dao import TurnoDAO
        db = Database()
        dao = TurnoDAO(db)
        ok = dao.cambiar_estado(id_turno, nuevo_estado)
        return (True, "Estado actualizado") if ok else (False, "No se pudo cambiar estado")

    def marcar_inasistencias_automaticas(self) -> int:
        return self._gestor.marcar_inasistencias_automaticas()

    def obtener_especialidades(self) -> list[dict]:
        return self._gestor.obtener_especialidades()

    def obtener_medicos_por_especialidad(self, id_especialidad: int) -> list[dict]:
        return self._gestor.obtener_medicos_por_especialidad(id_especialidad)
