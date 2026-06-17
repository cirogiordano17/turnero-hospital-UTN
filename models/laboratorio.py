from typing import List, TYPE_CHECKING
from enums import TipoLaboratorioEnum

if TYPE_CHECKING:
    from medicamento import Medicamento


class Laboratorio:
    """Clase que representa un laboratorio farmacéutico"""
    
    def __init__(self, numero_laboratorio: int, nombre: str, 
                 direccion: str, telefono: str):
        self.__numeroLaboratorio = numero_laboratorio
        self.__nombre = nombre
        self.__direccion = direccion
        self.__telefono = telefono
        self.__medicamentos: List['Medicamento'] = []
    
    # Getters
    def get_numero_laboratorio(self) -> int:
        """Obtiene el número del laboratorio"""
        return self.__numeroLaboratorio
    
    def get_nombre(self) -> str:
        """Obtiene el nombre del laboratorio"""
        return self.__nombre
    
    def get_direccion(self) -> str:
        """Obtiene la dirección del laboratorio"""
        return self.__direccion
    
    def get_telefono(self) -> str:
        """Obtiene el teléfono del laboratorio"""
        return self.__telefono
    
    def get_medicamentos(self) -> List['Medicamento']:
        """Obtiene la lista de medicamentos"""
        return self.__medicamentos.copy()
    
    # Setters
    def set_nombre(self, nombre: str) -> None:
        """Modifica el nombre del laboratorio"""
        if nombre and len(nombre) > 0:
            self.__nombre = nombre
        else:
            raise ValueError("El nombre no puede estar vacío")
    
    def set_direccion(self, direccion: str) -> None:
        """Modifica la dirección del laboratorio"""
        if direccion and len(direccion) > 0:
            self.__direccion = direccion
        else:
            raise ValueError("La dirección no puede estar vacía")
    
    def set_telefono(self, telefono: str) -> None:
        """Modifica el teléfono del laboratorio"""
        if telefono and len(telefono) > 0:
            self.__telefono = telefono
        else:
            raise ValueError("El teléfono no puede estar vacío")
    
    # Métodos de negocio
    def agregar_medicamento(self, medicamento: 'Medicamento') -> None:
        """Agrega un medicamento al laboratorio"""
        if medicamento not in self.__medicamentos:
            self.__medicamentos.append(medicamento)
            medicamento.set_laboratorio(self)
    
    def procesar_tipo(self, tipo: TipoLaboratorioEnum) -> None:
        """Procesa un tipo de laboratorio"""
        print(f"✓ Procesando laboratorio de tipo: {tipo.value}")
    
    def __repr__(self) -> str:
        return f"Laboratorio({self.__nombre}, {len(self.__medicamentos)} medicamentos)"