from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from laboratorio import Laboratorio


class Medicamento:
    """Clase que representa un medicamento"""
    
    def __init__(self, numero_medicamento: int, nombre: str, 
                 dosis: str, formato: str):
        self.__numeroMedicamento = numero_medicamento
        self.__nombre = nombre
        self.__dosis = dosis
        self.__formato = formato
        self.__laboratorio: Optional['Laboratorio'] = None
    
    # Getters
    def get_numero_medicamento(self) -> int:
        """Obtiene el número del medicamento"""
        return self.__numeroMedicamento
    
    def get_nombre(self) -> str:
        """Obtiene el nombre del medicamento"""
        return self.__nombre
    
    def get_dosis(self) -> str:
        """Obtiene la dosis del medicamento"""
        return self.__dosis
    
    def get_formato(self) -> str:
        """Obtiene el formato del medicamento"""
        return self.__formato
    
    def get_laboratorio(self) -> Optional['Laboratorio']:
        """Obtiene el laboratorio"""
        return self.__laboratorio
    
    # Setters
    def set_nombre(self, nombre: str) -> None:
        """Modifica el nombre del medicamento"""
        if nombre and len(nombre) > 0:
            self.__nombre = nombre
        else:
            raise ValueError("El nombre no puede estar vacío")
    
    def set_dosis(self, dosis: str) -> None:
        """Modifica la dosis del medicamento"""
        if dosis and len(dosis) > 0:
            self.__dosis = dosis
        else:
            raise ValueError("La dosis no puede estar vacía")
    
    def set_formato(self, formato: str) -> None:
        """Modifica el formato del medicamento"""
        if formato and len(formato) > 0:
            self.__formato = formato
        else:
            raise ValueError("El formato no puede estar vacío")
    
    def set_laboratorio(self, laboratorio: Optional['Laboratorio']) -> None:
        """Asigna un laboratorio"""
        self.__laboratorio = laboratorio
    
    # Métodos de negocio
    def registrar_medicamento(self) -> None:
        """Registra el medicamento en el sistema"""
        print(f"✓ Medicamento {self.__nombre} ({self.__dosis}) registrado")
    
    def modificar_medicamento(self) -> None:
        """Modifica los datos del medicamento"""
        print(f"✓ Medicamento {self.__nombre} modificado")
    
    def __repr__(self) -> str:
        return f"Medicamento({self.__nombre}, {self.__dosis})"