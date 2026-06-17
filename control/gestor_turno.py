"""Control — Casos de uso del ciclo de vida de los turnos."""
from __future__ import annotations
from datetime import date, timedelta
from typing import Optional

from boundary.persistence.turno_dao import TurnoDAO
from boundary.persistence.medico_dao import MedicoDAO
from boundary.persistence.paciente_dao import PacienteDAO
from entities.exceptions import (
    EntidadNoEncontradaError, EstadoInvalidoError, DuplicadoError,
)


class GestorTurno:
    """
    Orquesta todos los casos de uso relacionados con el ciclo de vida
    de un Turno: programar, cancelar, atender, inasistencia, y consultas.

    Principio de Responsabilidad Única: esta clase cambia únicamente cuando
    cambian las reglas de negocio de los turnos.

    Principio de Inversión de Dependencias: recibe los DAOs por constructor
    (inyección de dependencia), no los crea internamente.
    Esto permite reemplazarlos por mocks en tests unitarios.

    Rol ECB: Control.
    """

    def __init__(self, turno_dao: TurnoDAO, medico_dao: MedicoDAO,
                 paciente_dao: PacienteDAO) -> None:
        self._turno_dao = turno_dao
        self._medico_dao = medico_dao
        self._paciente_dao = paciente_dao

    # ── Caso de uso: Programar turno ────────────────────────────────────────

    def programar_turno(self, id_turno: int, id_paciente: int,
                        id_especialidad: Optional[int] = None,
                        observaciones: str = "") -> dict:
        """
        Asigna un paciente a un turno Libre.

        Raises:
            EntidadNoEncontradaError: si el turno o el paciente no existen.
            EstadoInvalidoError: si el turno no está en estado Libre.

        Returns:
            Dict con los datos del turno programado.
        """
        turno = self._turno_dao.buscar_por_id(id_turno)
        if not turno:
            raise EntidadNoEncontradaError(f"Turno #{id_turno} no encontrado")

        if turno["estado"] != "Libre":
            raise EstadoInvalidoError(
                f"El turno #{id_turno} no está disponible (estado: {turno['estado']})"
            )

        paciente = self._paciente_dao.buscar_por_id(id_paciente)
        if not paciente:
            raise EntidadNoEncontradaError(f"Paciente #{id_paciente} no encontrado")

        ok = self._turno_dao.programar(id_turno, id_paciente, id_especialidad, observaciones)
        if not ok:
            raise RuntimeError(f"No se pudo persistir el turno #{id_turno}")

        return self._turno_dao.buscar_por_id(id_turno)

    # ── Caso de uso: Cancelar turno ─────────────────────────────────────────

    def cancelar_turno(self, id_turno: int) -> bool:
        """
        Cancela un turno Programado.

        Raises:
            EntidadNoEncontradaError: si el turno no existe.
            EstadoInvalidoError: si el turno ya está cancelado u en otro estado final.
        """
        turno = self._turno_dao.buscar_por_id(id_turno)
        if not turno:
            raise EntidadNoEncontradaError(f"Turno #{id_turno} no encontrado")

        if turno["estado"] != "Programado":
            raise EstadoInvalidoError(
                f"No se puede cancelar un turno en estado '{turno['estado']}'"
            )

        return self._turno_dao.cambiar_estado(id_turno, "Cancelado")

    # ── Caso de uso: Registrar inasistencia manual ──────────────────────────

    def registrar_inasistencia(self, id_turno: int) -> bool:
        """
        Registra la inasistencia de un paciente a un turno Programado.

        Raises:
            EntidadNoEncontradaError / EstadoInvalidoError.
        """
        turno = self._turno_dao.buscar_por_id(id_turno)
        if not turno:
            raise EntidadNoEncontradaError(f"Turno #{id_turno} no encontrado")
        if turno["estado"] != "Programado":
            raise EstadoInvalidoError(
                f"No se puede marcar inasistencia en estado '{turno['estado']}'"
            )
        return self._turno_dao.cambiar_estado(id_turno, "Inasistencia")

    # ── Caso de uso: Marcar inasistencias automáticas ───────────────────────

    def marcar_inasistencias_automaticas(self) -> int:
        """
        Marca como Inasistencia todos los turnos Programados cuya fecha ya pasó.

        Returns:
            Cantidad de turnos afectados.
        """
        return self._turno_dao.marcar_inasistencias_vencidas()

    # ── Caso de uso: Consultar turnos ────────────────────────────────────────

    def obtener_turnos_libres(self, matricula: int) -> list[dict]:
        """
        Retorna turnos libres de un médico a partir de hoy,
        filtrando los del día actual que ya pasaron en hora.
        """
        from datetime import datetime, time as time_t
        turnos = self._turno_dao.listar_libres_por_medico(matricula)
        hoy = date.today()
        hora_actual = datetime.now().time()

        resultado = []
        for t in turnos:
            hora = t["hora_inicio"]
            if isinstance(hora, timedelta):
                s = int(hora.total_seconds())
                hora = time_t(s // 3600, (s % 3600) // 60)
            if t["fecha"] == hoy and hora <= hora_actual:
                continue
            resultado.append(t)
        return resultado

    def obtener_turnos_filtrados(self, filtro_fecha: str = "todos",
                                  filtro_estado: str = "todos_estados") -> list[dict]:
        """Retorna turnos con paciente asignado según los filtros combinados."""
        self.marcar_inasistencias_automaticas()
        return self._turno_dao.listar_por_filtros(filtro_fecha, filtro_estado)

    def obtener_turnos_paciente(self, id_paciente: int) -> list[dict]:
        return self._turno_dao.listar_por_paciente(id_paciente)

    # ── Caso de uso: Obtener datos para la UI ────────────────────────────────

    def obtener_especialidades(self) -> list[dict]:
        return self._turno_dao.listar_especialidades()

    def obtener_medicos_por_especialidad(self, id_especialidad: int) -> list[dict]:
        return self._turno_dao.listar_medicos_por_especialidad(id_especialidad)
