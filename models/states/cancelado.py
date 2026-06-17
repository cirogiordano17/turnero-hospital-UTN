from .estado_turno import EstadoTurno


class Cancelado(EstadoTurno):
    """Estado: Turno cancelado"""
    
    def __init__(self):
        super().__init__("Cancelado", "Turno cancelado")
    
    def liberar(self):
        """Transiciona a estado Libre"""
        from .libre import Libre
        return Libre()