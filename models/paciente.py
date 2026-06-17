from datetime import date
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from medico import Medico
    from turno import Turno
    from historial_clinico import HistorialClinico


class Paciente:
    """Clase que representa un paciente del sistema"""
    
    def __init__(self, nro_paciente: int, nombre: str, apellido: str, 
                 telefono: str, fecha_nacimiento: date, direccion: str):
        self.__nro_paciente = nro_paciente
        self.__nombre = nombre
        self.__apellido = apellido
        self.__telefono = telefono
        self.__fecha_nacimiento = fecha_nacimiento
        self.__direccion = direccion
        self.__medico: Optional['Medico'] = None
        self.__turnos: List['Turno'] = []
        self.__historiales: List['HistorialClinico'] = []
    
    # Getters
    def get_nro_paciente(self) -> int:
        """Obtiene el número de paciente"""
        return self.__nro_paciente
    
    def get_nombre(self) -> str:
        """Obtiene el nombre del paciente"""
        return self.__nombre
    
    def get_apellido(self) -> str:
        """Obtiene el apellido del paciente"""
        return self.__apellido
    
    def get_telefono(self) -> str:
        """Obtiene el teléfono del paciente"""
        return self.__telefono
    
    def get_fecha_nacimiento(self) -> date:
        """Obtiene la fecha de nacimiento"""
        return self.__fecha_nacimiento
    
    def get_direccion(self) -> str:
        """Obtiene la dirección del paciente"""
        return self.__direccion
    
    def get_medico(self) -> Optional['Medico']:
        """Obtiene el médico del paciente"""
        return self.__medico
    
    def get_turnos(self) -> List['Turno']:
        """Obtiene la lista de turnos"""
        return self.__turnos.copy()
    
    def get_historiales(self) -> List['HistorialClinico']:
        """Obtiene el historial clínico del paciente"""
        return self.__historiales.copy()
    
    # Setters
    def set_nombre(self, nombre: str) -> None:
        """Modifica el nombre del paciente"""
        if nombre and len(nombre) > 0:
            self.__nombre = nombre
        else:
            raise ValueError("El nombre no puede estar vacío")
    
    def set_apellido(self, apellido: str) -> None:
        """Modifica el apellido del paciente"""
        if apellido and len(apellido) > 0:
            self.__apellido = apellido
        else:
            raise ValueError("El apellido no puede estar vacío")
    
    def set_telefono(self, telefono: str) -> None:
        """Modifica el teléfono del paciente"""
        if telefono and len(telefono) > 0:
            self.__telefono = telefono
        else:
            raise ValueError("El teléfono no puede estar vacío")
    
    def set_direccion(self, direccion: str) -> None:
        """Modifica la dirección del paciente"""
        if direccion and len(direccion) > 0:
            self.__direccion = direccion
        else:
            raise ValueError("La dirección no puede estar vacía")
    
    def set_medico(self, medico: Optional['Medico']) -> None:
        """Asigna un médico al paciente"""
        self.__medico = medico
    
    # Métodos de negocio
    def agregar_turno(self, turno: 'Turno') -> None:
        """Agrega un turno al paciente"""
        if turno not in self.__turnos:
            self.__turnos.append(turno)
    
    def agregar_historial(self, historial: 'HistorialClinico') -> None:
        """Agrega un historial al paciente"""
        if historial not in self.__historiales:
            self.__historiales.append(historial)
    
    def registrar_paciente(self) -> None:
        """Registra el paciente en el sistema"""
        print(f"✓ Paciente {self.__nombre} {self.__apellido} registrado")
    
    def modificar_paciente(self) -> None:
        """Modifica los datos del paciente"""
        print(f"✓ Paciente {self.__nombre} {self.__apellido} modificado")
    
    def eliminar_paciente(self) -> None:
        """Elimina el paciente del sistema"""
        print(f"✓ Paciente {self.__nombre} {self.__apellido} eliminado")
    
    def obtener_historial(self) -> List['HistorialClinico']:
        """Retorna el historial clínico del paciente"""
        return self.__historiales.copy()
    
    def __repr__(self) -> str:
        return f"Paciente({self.__nombre} {self.__apellido}, #: {self.__nro_paciente})"