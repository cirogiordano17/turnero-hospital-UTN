from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from agenda import Agenda


class Consultorio:
    """Clase que representa un consultorio"""
    
    def __init__(self, numero: int, piso: int, equipamiento: str):
        self.__numero = numero
        self.__piso = piso
        self.__equipamiento = equipamiento
        self.__agendas: List['Agenda'] = []
    
    # Getters
    def get_numero(self) -> int:
        """Obtiene el número del consultorio"""
        return self.__numero
    
    def get_piso(self) -> int:
        """Obtiene el piso del consultorio"""
        return self.__piso
    
    def get_equipamiento(self) -> str:
        """Obtiene el equipamiento del consultorio"""
        return self.__equipamiento
    
    def get_agendas(self) -> List['Agenda']:
        """Obtiene la lista de agendas"""
        return self.__agendas.copy()
    
    # Setters
    def set_equipamiento(self, equipamiento: str) -> None:
        """Modifica el equipamiento del consultorio"""
        if equipamiento and len(equipamiento) > 0:
            self.__equipamiento = equipamiento
        else:
            raise ValueError("El equipamiento no puede estar vacío")
    
    # Métodos de negocio
    def agregar_agenda(self, agenda: 'Agenda') -> None:
        """Agrega una agenda al consultorio"""
        if agenda not in self.__agendas:
            self.__agendas.append(agenda)
    
    def registrar_consultorio(self) -> None:
        """Registra el consultorio en el sistema"""
        print(f"✓ Consultorio {self.__numero} (Piso {self.__piso}) registrado")
    
    def consultar_disponibilidad(self) -> bool:
        """Verifica si el consultorio está disponible"""
        return len(self.__agendas) == 0
    
    def __repr__(self) -> str:
        return f"Consultorio({self.__numero}, Piso: {self.__piso})"