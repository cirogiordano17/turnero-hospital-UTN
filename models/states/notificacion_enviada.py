from .estado_notificacion import EstadoNotificacion


class Enviado(EstadoNotificacion):
    """Estado: Notificación enviada"""
    
    def __init__(self):
        super().__init__("Enviado", "Notificación enviada correctamente")