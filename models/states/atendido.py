from .estado_turno import EstadoTurno


class Atendido(EstadoTurno):
    """Estado: Turno completado"""
    
    def __init__(self):
        super().__init__("Atendido", "Turno completado")