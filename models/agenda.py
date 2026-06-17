from datetime import time
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from medico import Medico
    from consultorio import Consultorio
    from turno import Turno


class Agenda:
    """Clase que representa la agenda de un médico en un consultorio"""
    
    def __init__(self, nro_agenda: int, medico: 'Medico', 
                 consultorio: 'Consultorio', dia_semana: str,
                 hora_inicio: time, hora_fin: time):
        self.__nroAgenda = nro_agenda
        self.__medico = medico
        self.__consultorio = consultorio
        self.__deSemana = dia_semana
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin
        self.__turnos: List['Turno'] = []
    
    # Getters
    def get_nro_agenda(self) -> int:
        """Obtiene el número de agenda"""
        return self.__nroAgenda
    
    def get_medico(self) -> 'Medico':
        """Obtiene el médico de la agenda"""
        return self.__medico
    
    def get_consultorio(self) -> 'Consultorio':
        """Obtiene el consultorio de la agenda"""
        return self.__consultorio
    
    def get_dia_semana(self) -> str:
        """Obtiene el día de la semana"""
        return self.__deSemana
    
    def get_hora_inicio(self) -> time:
        """Obtiene la hora de inicio"""
        return self.__hora_inicio
    
    def get_hora_fin(self) -> time:
        """Obtiene la hora de fin"""
        return self.__hora_fin
    
    def get_turnos(self) -> List['Turno']:
        """Obtiene la lista de turnos"""
        return self.__turnos.copy()
    
    # Setters
    def set_dia_semana(self, dia_semana: str) -> None:
        """Modifica el día de la semana"""
        if dia_semana and len(dia_semana) > 0:
            self.__deSemana = dia_semana
        else:
            raise ValueError("El día no puede estar vacío")
    
    def set_hora_inicio(self, hora_inicio: time) -> None:
        """Modifica la hora de inicio"""
        self.__hora_inicio = hora_inicio
    
    def set_hora_fin(self, hora_fin: time) -> None:
        """Modifica la hora de fin"""
        self.__hora_fin = hora_fin
    
    # Métodos de negocio
    def verificar_disponibilidad(self) -> bool:
        """Verifica si hay espacios disponibles en la agenda"""
        return len(self.__turnos) < self._calcular_capacidad()
    
    def _calcular_capacidad(self) -> int:
        """Calcula la cantidad de turnos que caben en este horario"""
        diferencia = (self.__hora_fin.hour * 60 + self.__hora_fin.minute) - \
                     (self.__hora_inicio.hour * 60 + self.__hora_inicio.minute)
        return diferencia // 30  # Asumiendo turnos de 30 minutos
    
    def actualizar_agenda(self) -> None:
        """Actualiza la información de la agenda"""
        print(f"✓ Agenda {self.__nroAgenda} actualizada")
    
    def agregar_turno(self, turno: 'Turno') -> bool:
        """Agrega un turno a la agenda si hay disponibilidad"""
        if self.verificar_disponibilidad():
            self.__turnos.append(turno)
            return True
        return False
    
    def __repr__(self) -> str:
        return f"Agenda({self.__nroAgenda}, {self.__deSemana}, {self.__consultorio})"