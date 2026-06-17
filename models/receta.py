from datetime import date
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from detalle_receta import DetalleDeReceta


class Receta:
    """Clase que representa una receta médica"""
    
    def __init__(self, nro_receta: int, fecha_emision: date, 
                 observaciones: str = ""):
        self.__nroReceta = nro_receta
        self.__fechaEmision = fecha_emision
        self.__observaciones = observaciones
        self.__detalles: List['DetalleDeReceta'] = []
    
    # Getters
    def get_nro_receta(self) -> int:
        """Obtiene el número de receta"""
        return self.__nroReceta
    
    def get_fecha_emision(self) -> date:
        """Obtiene la fecha de emisión"""
        return self.__fechaEmision
    
    def get_observaciones(self) -> str:
        """Obtiene las observaciones"""
        return self.__observaciones
    
    def get_detalles(self) -> List['DetalleDeReceta']:
        """Obtiene los detalles de la receta"""
        return self.__detalles.copy()
    
    # Setters
    def set_observaciones(self, observaciones: str) -> None:
        """Modifica las observaciones"""
        if observaciones and len(observaciones) > 0:
            self.__observaciones = observaciones
        else:
            raise ValueError("Las observaciones no pueden estar vacías")
    
    # Métodos de negocio
    def agregar_detalle(self, detalle: 'DetalleDeReceta') -> None:
        """Agrega un detalle (medicamento) a la receta"""
        if detalle not in self.__detalles:
            self.__detalles.append(detalle)
    
    def __repr__(self) -> str:
        return f"Receta({self.__nroReceta}, {self.__fechaEmision}, {len(self.__detalles)} items)"