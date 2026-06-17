from estado_notificacion import EstadoNotificacion


class Pendiente(EstadoNotificacion):
    """Estado: Notificación pendiente"""
    
    def __init__(self):
        super().__init__("Pendiente", "Notificación pendiente de envío")