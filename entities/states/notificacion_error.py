from .estado_notificacion import EstadoNotificacion


class Error(EstadoNotificacion):
    def __init__(self) -> None:
        super().__init__("Error", "Error al enviar notificación")
