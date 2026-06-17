"""Control — Scheduler de procesamiento automático de notificaciones."""
from __future__ import annotations
import time
import logging
import threading
from datetime import datetime

from control.gestor_notificacion import GestorNotificacion

logger = logging.getLogger(__name__)


class SchedulerNotificaciones:
    """
    Ejecuta GestorNotificacion.procesar_pendientes() periódicamente
    en un hilo de background.

    Es un Control de tipo "proceso" (no interactivo): observa el tiempo
    y delega toda la lógica al GestorNotificacion.

    Rol ECB: Control.
    """

    def __init__(self, gestor: GestorNotificacion,
                 intervalo_minutos: int = 5) -> None:
        self._gestor = gestor
        self._intervalo = intervalo_minutos * 60
        self._activo = False
        self._thread: threading.Thread | None = None

    def iniciar(self) -> None:
        if self._activo:
            return
        self._activo = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("Scheduler de notificaciones iniciado (cada %d min)", intervalo_minutos := self._intervalo // 60)

    def detener(self) -> None:
        self._activo = False
        if self._thread:
            self._thread.join(timeout=2)

    def _loop(self) -> None:
        while self._activo:
            try:
                enviadas, fallidas = self._gestor.procesar_pendientes()
                if enviadas or fallidas:
                    logger.info("[%s] Notificaciones: %d enviadas, %d fallidas",
                                datetime.now().strftime("%H:%M:%S"), enviadas, fallidas)
            except Exception as exc:
                logger.error("Scheduler error: %s", exc)
            time.sleep(self._intervalo)
