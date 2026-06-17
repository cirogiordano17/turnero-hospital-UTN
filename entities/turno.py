"""Entity — Turno médico con ciclo de vida modelado mediante Patrón State."""
from __future__ import annotations
from datetime import date, time
from typing import List
from entities.states.estado_turno import EstadoTurno
from entities.states.libre import Libre
from entities.states.programado import Programado
from entities.states.cambio_estado import CambioEstado
from entities.exceptions import EstadoInvalidoError, ValidacionError


class Turno:
    """
    Representa un slot de tiempo en la agenda de un médico.

    El ciclo de vida del turno está modelado con el Patrón State:
        Libre → Programado → Atendido
                           → Cancelado → (puede liberarse)
                           → Inasistencia

    Los cambios de estado quedan registrados en el historial de `cambios`,
    permitiendo trazabilidad completa.

    IMPORTANTE: el constructor NO agrega este turno a las listas de médico
    ni paciente. Esa responsabilidad pertenece al Control (GestorTurno),
    evitando side effects ocultos que dificultan el testing.

    Rol ECB: Entity.
    """

    def __init__(self, id_turno: int, matricula_medico: int,
                 id_consultorio: int, id_agenda: int,
                 fecha: date, hora_inicio: time, hora_fin: time,
                 estado: str = "Libre",
                 id_paciente: int | None = None,
                 id_especialidad: int | None = None,
                 observaciones: str = "") -> None:
        if hora_fin <= hora_inicio:
            raise ValidacionError("La hora de fin debe ser posterior a la de inicio")
        self._id = id_turno
        self._matricula_medico = matricula_medico
        self._id_consultorio = id_consultorio
        self._id_agenda = id_agenda
        self._fecha = fecha
        self._hora_inicio = hora_inicio
        self._hora_fin = hora_fin
        self._id_paciente = id_paciente
        self._id_especialidad = id_especialidad
        self._observaciones = observaciones
        self._estado: EstadoTurno = self._estado_desde_string(estado)
        self._cambios: List[CambioEstado] = []

    # -- Identidad --

    @property
    def id_turno(self) -> int:
        return self._id

    # -- Datos del turno --

    @property
    def matricula_medico(self) -> int:
        return self._matricula_medico

    @property
    def id_consultorio(self) -> int:
        return self._id_consultorio

    @property
    def id_agenda(self) -> int:
        return self._id_agenda

    @property
    def fecha(self) -> date:
        return self._fecha

    @property
    def hora_inicio(self) -> time:
        return self._hora_inicio

    @property
    def hora_fin(self) -> time:
        return self._hora_fin

    @property
    def id_paciente(self) -> int | None:
        return self._id_paciente

    @property
    def id_especialidad(self) -> int | None:
        return self._id_especialidad

    @property
    def observaciones(self) -> str:
        return self._observaciones

    @observaciones.setter
    def observaciones(self, value: str) -> None:
        self._observaciones = (value or "").strip()

    # -- Estado --

    @property
    def estado(self) -> EstadoTurno:
        return self._estado

    @property
    def nombre_estado(self) -> str:
        return self._estado.nombre

    @property
    def cambios(self) -> List[CambioEstado]:
        return list(self._cambios)

    # -- Transiciones de estado (Patrón State) --

    def programar(self, id_paciente: int, id_especialidad: int | None = None,
                  observaciones: str = "") -> None:
        """
        Asigna un paciente al turno y lo pasa a estado Programado.

        Raises:
            EstadoInvalidoError: si el turno no está en estado Libre.
        """
        if not isinstance(self._estado, Libre):
            raise EstadoInvalidoError(
                f"No se puede programar un turno en estado '{self._estado.nombre}'"
            )
        self._estado = self._estado.programar()
        self._id_paciente = id_paciente
        if id_especialidad is not None:
            self._id_especialidad = id_especialidad
        if observaciones:
            self._observaciones = observaciones
        self._registrar_cambio()

    def cancelar(self) -> None:
        """
        Cancela el turno.

        Raises:
            EstadoInvalidoError: si el turno no está en estado Programado.
        """
        if not isinstance(self._estado, Programado):
            raise EstadoInvalidoError(
                f"No se puede cancelar un turno en estado '{self._estado.nombre}'"
            )
        self._estado = self._estado.cancelar()
        self._registrar_cambio()

    def atender(self) -> None:
        """
        Registra que el paciente fue atendido.

        Raises:
            EstadoInvalidoError: si el turno no está en estado Programado.
        """
        if not isinstance(self._estado, Programado):
            raise EstadoInvalidoError(
                f"No se puede atender un turno en estado '{self._estado.nombre}'"
            )
        self._estado = self._estado.atender()
        self._registrar_cambio()

    def marcar_inasistencia(self) -> None:
        """
        Registra la inasistencia del paciente.

        Raises:
            EstadoInvalidoError: si el turno no está en estado Programado.
        """
        if not isinstance(self._estado, Programado):
            raise EstadoInvalidoError(
                f"No se puede marcar inasistencia en un turno en estado '{self._estado.nombre}'"
            )
        self._estado = self._estado.marcar_inasistencia()
        self._registrar_cambio()

    # -- Helpers internos --

    def _registrar_cambio(self) -> None:
        self._cambios.append(CambioEstado(self._estado))

    @staticmethod
    def _estado_desde_string(nombre: str) -> EstadoTurno:
        """Reconstruye el estado a partir del string almacenado en la BD."""
        from entities.states.atendido import Atendido
        from entities.states.cancelado import Cancelado
        from entities.states.inasistencia import Inasistencia
        mapa = {
            "Libre": Libre,
            "Programado": Programado,
            "Atendido": Atendido,
            "Cancelado": Cancelado,
            "Inasistencia": Inasistencia,
        }
        cls = mapa.get(nombre)
        if cls is None:
            raise ValidacionError(f"Estado de turno desconocido: '{nombre}'")
        return cls()

    def __repr__(self) -> str:
        return (
            f"Turno(id={self._id}, fecha={self._fecha}, "
            f"{self._hora_inicio}-{self._hora_fin}, estado={self._estado.nombre})"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Turno):
            return self._id == other._id
        return NotImplemented
