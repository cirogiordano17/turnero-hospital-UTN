from datetime import date, time
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from medico import Medico
    from paciente import Paciente
    from consultorio import Consultorio
    from notificacion import Notificacion

from .states.libre import Libre
from .states.programado import Programado
from .states.cambio_estado import CambioEstado


class Turno:
    """Clase que representa un turno médico"""
    
    def __init__(self, nro_turno: int, medico: 'Medico', 
                 paciente: 'Paciente', consultorio: 'Consultorio',
                 fecha: date, hora_inicio: time, hora_fin: time):
        self.__nroTurno = nro_turno
        self.__medico = medico
        self.__paciente = paciente
        self.__consultorio = consultorio
        self.__fecha = fecha
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin
        self.__observaciones = ""
        self.__estado_turno = Libre()
        self.__cambios_estado: List[CambioEstado] = []
        self.__notificaciones: List['Notificacion'] = []
        
        # Agregar turno a listas relacionadas
        medico.agregar_turno(self)
        paciente.agregar_turno(self)
    
    # Getters
    def get_nro_turno(self) -> int:
        """Obtiene el número de turno"""
        return self.__nroTurno
    
    def get_medico(self) -> 'Medico':
        """Obtiene el médico del turno"""
        return self.__medico
    
    def get_paciente(self) -> 'Paciente':
        """Obtiene el paciente del turno"""
        return self.__paciente
    
    def get_consultorio(self) -> 'Consultorio':
        """Obtiene el consultorio del turno"""
        return self.__consultorio
    
    def get_fecha(self) -> date:
        """Obtiene la fecha del turno"""
        return self.__fecha
    
    def get_hora_inicio(self) -> time:
        """Obtiene la hora de inicio del turno"""
        return self.__hora_inicio
    
    def get_hora_fin(self) -> time:
        """Obtiene la hora de fin del turno"""
        return self.__hora_fin
    
    def get_observaciones(self) -> str:
        """Obtiene las observaciones"""
        return self.__observaciones
    
    def get_estado_turno(self):
        """Obtiene el estado del turno"""
        return self.__estado_turno
    
    def get_cambios_estado(self) -> List[CambioEstado]:
        """Obtiene los cambios de estado"""
        return self.__cambios_estado.copy()
    
    def get_notificaciones(self) -> List['Notificacion']:
        """Obtiene las notificaciones"""
        return self.__notificaciones.copy()
    
    # Setters
    def set_observaciones(self, observaciones: str) -> None:
        """Modifica las observaciones"""
        if observaciones and len(observaciones) > 0:
            self.__observaciones = observaciones
        else:
            raise ValueError("Las observaciones no pueden estar vacías")
    
    def set_hora_inicio(self, hora_inicio: time) -> None:
        """Modifica la hora de inicio"""
        if hora_inicio:
            self.__hora_inicio = hora_inicio
        else:
            raise ValueError("La hora de inicio no puede estar vacía")
    
    def set_hora_fin(self, hora_fin: time) -> None:
        """Modifica la hora de fin"""
        if hora_fin:
            self.__hora_fin = hora_fin
        else:
            raise ValueError("La hora de fin no puede estar vacía")
    
    def set_estado_turno(self, estado_turno) -> None:
        """Modifica el estado del turno"""
        self.__estado_turno = estado_turno
    
    # Métodos de negocio
    def programar_turno(self) -> None:
        """Programa el turno cambiando su estado a Programado"""
        estado_anterior = self.__estado_turno
        self.__estado_turno = self.__estado_turno.programar()
        cambio = CambioEstado(date.today(), date.today(), self.__estado_turno)
        self.__cambios_estado.append(cambio)
        print(f"✓ Turno {self.__nroTurno} programado ({estado_anterior} → {self.__estado_turno})")
    
    def cancelar_turno(self) -> None:
        """Cancela el turno"""
        if isinstance(self.__estado_turno, Programado):
            estado_anterior = self.__estado_turno
            self.__estado_turno = self.__estado_turno.cancelar()
            cambio = CambioEstado(date.today(), date.today(), self.__estado_turno)
            self.__cambios_estado.append(cambio)
            print(f"✓ Turno {self.__nroTurno} cancelado ({estado_anterior} → {self.__estado_turno})")
        else:
            print(f"✗ No se puede cancelar un turno en estado {self.__estado_turno}")
    
    def registrar_asistencia(self) -> None:
        """Registra la asistencia del paciente"""
        if isinstance(self.__estado_turno, Programado):
            estado_anterior = self.__estado_turno
            self.__estado_turno = self.__estado_turno.atender()
            cambio = CambioEstado(date.today(), date.today(), self.__estado_turno)
            self.__cambios_estado.append(cambio)
            print(f"✓ Asistencia registrada para turno {self.__nroTurno} ({estado_anterior} → {self.__estado_turno})")
        else:
            print(f"✗ No se puede registrar asistencia para un turno en estado {self.__estado_turno}")
    
    def registrar_inasistencia(self) -> None:
        """Registra la inasistencia del paciente"""
        if isinstance(self.__estado_turno, Programado):
            estado_anterior = self.__estado_turno
            self.__estado_turno = self.__estado_turno.ausente()
            cambio = CambioEstado(date.today(), date.today(), self.__estado_turno)
            self.__cambios_estado.append(cambio)
            print(f"✓ Inasistencia registrada para turno {self.__nroTurno} ({estado_anterior} → {self.__estado_turno})")
        else:
            print(f"✗ No se puede registrar inasistencia para un turno en estado {self.__estado_turno}")
    
    def agregar_notificacion(self, notificacion: 'Notificacion') -> None:
        """Agrega una notificación al turno"""
        if notificacion not in self.__notificaciones:
            self.__notificaciones.append(notificacion)
    
    def __repr__(self) -> str:
        return f"Turno({self.__nroTurno}, {self.__fecha} {self.__hora_inicio}-{self.__hora_fin}, Estado: {self.__estado_turno})"