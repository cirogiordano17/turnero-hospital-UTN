from .estado_turno import EstadoTurno


class Inasistencia(EstadoTurno):
    """Estado: Paciente no asistió"""
    
    def __init__(self):
        super().__init__("Inasistencia", "Paciente no asistió")