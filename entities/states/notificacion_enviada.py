from .estado_notificacion import EstadoNotificacion


class Enviado(EstadoNotificacion):
    def __init__(self) -> None:
        super().__init__("Enviado", "Notificación enviada correctamente")
