from .estado_turno import EstadoTurno


class Libre(EstadoTurno):
    """Estado: Turno disponible"""
    
    def __init__(self):
        super().__init__("Libre", "Turno disponible")
    
    def programar(self):
        """Transiciona a estado Programado"""
        from .programado import Programado
        return Programado()