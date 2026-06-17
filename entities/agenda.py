"""Entity — Agenda de un médico en un consultorio."""
from __future__ import annotations
from datetime import time
from entities.exceptions import ValidacionError

DURACION_TURNO_MINUTOS = 30  # configurable, no hardcodeado en lógica


class Agenda:
    """
    Define el horario regular en que un médico atiende en un consultorio.

    A partir de una Agenda, el GestorAgenda genera los Turnos libres.
    La capacidad máxima (cantidad de slots) se calcula automáticamente
    dividiendo la duración del horario por DURACION_TURNO_MINUTOS.

    Rol ECB: Entity.
    """

    def __init__(self, id_agenda: int, matricula_medico: int,
                 id_consultorio: int, dia_semana: str,
                 hora_inicio: time, hora_fin: time) -> None:
        if hora_fin <= hora_inicio:
            raise ValidacionError("La hora de fin debe ser posterior a la de inicio")
        self._id = id_agenda
        self._matricula_medico = matricula_medico
        self._id_consultorio = id_consultorio
        self.dia_semana = dia_semana
        self._hora_inicio = hora_inicio
        self._hora_fin = hora_fin

    @property
    def id_agenda(self) -> int:
        return self._id

    @property
    def matricula_medico(self) -> int:
        return self._matricula_medico

    @property
    def id_consultorio(self) -> int:
        return self._id_consultorio

    @property
    def dia_semana(self) -> str:
        return self._dia_semana

    @dia_semana.setter
    def dia_semana(self, value: str) -> None:
        dias_validos = {"Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"}
        if not value or value.strip() not in dias_validos:
            raise ValidacionError(f"Día de semana inválido: '{value}'")
        self._dia_semana = value.strip()

    @property
    def hora_inicio(self) -> time:
        return self._hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, value: time) -> None:
        if value >= self._hora_fin:
            raise ValidacionError("La hora de inicio debe ser anterior a la de fin")
        self._hora_inicio = value

    @property
    def hora_fin(self) -> time:
        return self._hora_fin

    @hora_fin.setter
    def hora_fin(self, value: time) -> None:
        if value <= self._hora_inicio:
            raise ValidacionError("La hora de fin debe ser posterior a la de inicio")
        self._hora_fin = value

    @property
    def capacidad_turnos(self) -> int:
        """Cantidad de slots de DURACION_TURNO_MINUTOS que caben en el horario."""
        minutos_inicio = self._hora_inicio.hour * 60 + self._hora_inicio.minute
        minutos_fin = self._hora_fin.hour * 60 + self._hora_fin.minute
        return (minutos_fin - minutos_inicio) // DURACION_TURNO_MINUTOS

    def __repr__(self) -> str:
        return (
            f"Agenda(id={self._id}, medico={self._matricula_medico}, "
            f"dia={self._dia_semana}, {self._hora_inicio}-{self._hora_fin})"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Agenda):
            return self._id == other._id
        return NotImplemented
