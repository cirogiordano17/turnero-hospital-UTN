from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from receta import Receta
    from medicamento import Medicamento


class DetalleDeReceta:
    """Clase que representa un detalle (medicamento) en una receta"""
    
    def __init__(self, nro_item: int, receta: 'Receta', 
                 medicamento: 'Medicamento', indicacion: str):
        self.__nroItem = nro_item
        self.__receta = receta
        self.__medicamento = medicamento
        self.__indicacion = indicacion
        receta.agregar_detalle(self)
    
    # Getters
    def get_nro_item(self) -> int:
        """Obtiene el número de item"""
        return self.__nroItem
    
    def get_receta(self) -> 'Receta':
        """Obtiene la receta"""
        return self.__receta
    
    def get_medicamento(self) -> 'Medicamento':
        """Obtiene el medicamento"""
        return self.__medicamento
    
    def get_indicacion(self) -> str:
        """Obtiene la indicación"""
        return self.__indicacion
    
    # Setters
    def set_indicacion(self, indicacion: str) -> None:
        """Modifica la indicación"""
        if indicacion and len(indicacion) > 0:
            self.__indicacion = indicacion
        else:
            raise ValueError("La indicación no puede estar vacía")
    
    # Métodos de negocio
    def emitir_receta(self) -> None:
        """Emite el detalle de la receta"""
        print(f"✓ Receta emitida: {self.__medicamento.get_nombre()} - {self.__indicacion}")
    
    def agregar_medicamento(self) -> None:
        """Registra el medicamento en el sistema"""
        print(f"✓ Medicamento agregado: {self.__medicamento.get_nombre()}")
    
    def __repr__(self) -> str:
        return f"DetalleReceta({self.__nroItem}, {self.__medicamento.get_nombre()})"