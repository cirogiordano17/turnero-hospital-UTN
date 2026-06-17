from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from medico import Medico


class Especialidad:
    """Clase que representa una especialidad médica"""
    
    def __init__(self, nro_especialidad: int, nombre: str, descripcion: str):
        self.__nroEspecialidad = nro_especialidad
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__medicos: List['Medico'] = []
    
    # Getters
    def get_nro_especialidad(self) -> int:
        """Obtiene el número de especialidad"""
        return self.__nroEspecialidad
    
    def get_nombre(self) -> str:
        """Obtiene el nombre de la especialidad"""
        return self.__nombre
    
    def get_descripcion(self) -> str:
        """Obtiene la descripción de la especialidad"""
        return self.__descripcion
    
    def get_medicos(self) -> List['Medico']:
        """Obtiene la lista de médicos"""
        return self.__medicos.copy()
    
    # Setters
    def set_nombre(self, nombre: str) -> None:
        """Modifica el nombre de la especialidad"""
        if nombre and len(nombre) > 0:
            self.__nombre = nombre
        else:
            raise ValueError("El nombre no puede estar vacío")
    
    def set_descripcion(self, descripcion: str) -> None:
        """Modifica la descripción de la especialidad"""
        if descripcion and len(descripcion) > 0:
            self.__descripcion = descripcion
        else:
            raise ValueError("La descripción no puede estar vacía")
    
    # Métodos de negocio
    def registrar_especialidad(self) -> None:
        """Registra la especialidad en el sistema"""
        print(f"✓ Especialidad {self.__nombre} registrada")
    
    def asociar_medico(self, medico: 'Medico') -> None:
        """Asocia un médico a esta especialidad"""
        if medico not in self.__medicos:
            self.__medicos.append(medico)
    
    def __repr__(self) -> str:
        return f"Especialidad({self.__nombre})"