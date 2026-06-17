from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from turno import Turno
    from paciente import Paciente
    from receta import Receta


class HistorialClinico:
    """Clase que representa el historial clínico de un turno"""
    
    def __init__(self, nro_historial: int, turno: 'Turno', 
                 paciente: 'Paciente'):
        self.__nroHistorial = nro_historial
        self.__turno = turno
        self.__paciente = paciente
        self.__tratamiento = ""
        self.__observaciones = ""
        self.__receta: Optional['Receta'] = None
        paciente.agregar_historial(self)
    
    # Getters
    def get_nro_historial(self) -> int:
        """Obtiene el número de historial"""
        return self.__nroHistorial
    
    def get_turno(self) -> 'Turno':
        """Obtiene el turno asociado"""
        return self.__turno
    
    def get_paciente(self) -> 'Paciente':
        """Obtiene el paciente"""
        return self.__paciente
    
    def get_tratamiento(self) -> str:
        """Obtiene el tratamiento"""
        return self.__tratamiento
    
    def get_observaciones(self) -> str:
        """Obtiene las observaciones"""
        return self.__observaciones
    
    def get_receta(self) -> Optional['Receta']:
        """Obtiene la receta"""
        return self.__receta
    
    # Setters
    def set_tratamiento(self, tratamiento: str) -> None:
        """Modifica el tratamiento"""
        if tratamiento and len(tratamiento) > 0:
            self.__tratamiento = tratamiento
        else:
            raise ValueError("El tratamiento no puede estar vacío")
    
    def set_observaciones(self, observaciones: str) -> None:
        """Modifica las observaciones"""
        if observaciones and len(observaciones) > 0:
            self.__observaciones = observaciones
        else:
            raise ValueError("Las observaciones no pueden estar vacías")
    
    # Métodos de negocio
    def registrar_diagnostico(self, diagnostico: str) -> None:
        """Registra el diagnóstico en el historial"""
        self.__observaciones = diagnostico
        print(f"✓ Diagnóstico registrado: {diagnostico}")
    
    def registrar_tratamiento(self, tratamiento: str) -> None:
        """Registra el tratamiento en el historial"""
        self.__tratamiento = tratamiento
        print(f"✓ Tratamiento registrado: {tratamiento}")
    
    def vincular_receta(self, receta: 'Receta') -> None:
        """Vincula una receta al historial clínico"""
        self.__receta = receta
        print(f"✓ Receta {receta.get_nro_receta()} vinculada al historial {self.__nroHistorial}")
    
    def __repr__(self) -> str:
        return f"HistorialClinico({self.__nroHistorial}, Turno: {self.__turno.get_nro_turno()})"