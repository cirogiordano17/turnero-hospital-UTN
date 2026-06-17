from .estado_turno import EstadoTurno


class Programado(EstadoTurno):
    """Estado: Turno reservado"""
    
    def __init__(self):
        super().__init__("Programado", "Turno reservado")
    
    def cancelar(self):
        """Transiciona a estado Cancelado"""
        from .cancelado import Cancelado
        return Cancelado()
    
    def atender(self):
        """Transiciona a estado Atendido"""
        from .atendido import Atendido
        return Atendido()
    
    def ausente(self):
        """Transiciona a estado Inasistencia"""
        from .inasistencia import Inasistencia
        return Inasistencia()