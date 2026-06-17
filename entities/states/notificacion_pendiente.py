from .estado_notificacion import EstadoNotificacion


class Pendiente(EstadoNotificacion):
    def __init__(self) -> None:
        super().__init__("Pendiente", "Notificación pendiente de envío")
