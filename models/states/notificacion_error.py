from .estado_notificacion import EstadoNotificacion


class Error(EstadoNotificacion):
    """Estado: Error en notificación"""
    
    def __init__(self):
        super().__init__("Error", "Error al enviar notificación")