from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from turno import Turno

from .states.notificacion_pendiente import Pendiente
from .states.notificacion_enviada import Enviado
from .states.notificacion_error import Error


class Notificacion:
    """Clase que representa una notificación de turno"""
    
    def __init__(self, nro_notificacion: int, turno: 'Turno',
                 fecha_hora_envio: datetime):
        self.__nroNotificacion = nro_notificacion
        self.__turno = turno
        self.__fechaHoraEnvio = fecha_hora_envio
        self.__estado_notificacion = Pendiente()
        turno.agregar_notificacion(self)
    
    # Getters
    def get_nro_notificacion(self) -> int:
        """Obtiene el número de notificación"""
        return self.__nroNotificacion
    
    def get_turno(self) -> 'Turno':
        """Obtiene el turno asociado"""
        return self.__turno
    
    def get_fecha_hora_envio(self) -> datetime:
        """Obtiene la fecha y hora de envío"""
        return self.__fechaHoraEnvio
    
    def get_estado_notificacion(self):
        """Obtiene el estado de la notificación"""
        return self.__estado_notificacion
    
    # Setters
    def set_estado_notificacion(self, estado_notificacion) -> None:
        """Modifica el estado de la notificación"""
        self.__estado_notificacion = estado_notificacion
    
    # Métodos de negocio
    def enviar_recordatorio(self) -> None:
        """Envía el recordatorio del turno"""
        self.__estado_notificacion = Enviado()
        print(f"✓ Recordatorio enviado el {self.__fechaHoraEnvio}")
    
    def registrar_error(self) -> None:
        """Registra un error en el envío"""
        self.__estado_notificacion = Error()
        print(f"✗ Error registrado en notificación {self.__nroNotificacion}")
    
    def marcar_pendiente(self) -> None:
        """Marca la notificación como pendiente"""
        self.__estado_notificacion = Pendiente()
        print(f"⏳ Notificación {self.__nroNotificacion} marcada como pendiente")
    
    def __repr__(self) -> str:
        return f"Notificacion({self.__nroNotificacion}, Estado: {self.__estado_notificacion})"