from datetime import date
from .estado_turno import EstadoTurno


class CambioEstado:
    """Clase que registra cambios de estado en turno"""
    
    def __init__(self, fecha_inicio: date, fecha_fin: date, 
                 estado_turno: EstadoTurno):
        self.__fechaHoraInicio = fecha_inicio
        self.__fechaHoraFin = fecha_fin
        self.__estado_turno = estado_turno
    
    # Getters
    def get_fecha_inicio(self) -> date:
        """Obtiene la fecha de inicio"""
        return self.__fechaHoraInicio
    
    def get_fecha_fin(self) -> date:
        """Obtiene la fecha de fin"""
        return self.__fechaHoraFin
    
    def get_estado_turno(self) -> EstadoTurno:
        """Obtiene el estado del turno"""
        return self.__estado_turno
    
    # Setters
    def set_fecha_inicio(self, fecha_inicio: date) -> None:
        """Modifica la fecha de inicio"""
        self.__fechaHoraInicio = fecha_inicio
    
    def set_fecha_fin(self, fecha_fin: date) -> None:
        """Modifica la fecha de fin"""
        self.__fechaHoraFin = fecha_fin
    
    def set_estado_turno(self, estado_turno: EstadoTurno) -> None:
        """Modifica el estado del turno"""
        self.__estado_turno = estado_turno
    
    # Métodos de negocio
    def registrar_cambio(self) -> None:
        """Registra el cambio de estado"""
        print(f"✓ Cambio de estado a {self.__estado_turno} registrado")
    
    def __repr__(self) -> str:
        return f"CambioEstado({self.__fechaHoraInicio}, {self.__estado_turno})"