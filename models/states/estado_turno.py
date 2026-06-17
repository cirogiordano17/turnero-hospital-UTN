from abc import ABC


class EstadoTurno(ABC):
    """Clase base abstracta para estados de turno (Patrón State)"""
    
    def __init__(self, nombre: str, descripcion: str):
        self.__nombre = nombre
        self.__descripcion = descripcion
    
    # Getters
    def get_nombre(self) -> str:
        """Obtiene el nombre del estado"""
        return self.__nombre
    
    def get_descripcion(self) -> str:
        """Obtiene la descripción del estado"""
        return self.__descripcion
    
    # Setters
    def set_nombre(self, nombre: str) -> None:
        """Modifica el nombre del estado"""
        if nombre and len(nombre) > 0:
            self.__nombre = nombre
        else:
            raise ValueError("El nombre no puede estar vacío")
    
    def __repr__(self) -> str:
        return self.__nombre