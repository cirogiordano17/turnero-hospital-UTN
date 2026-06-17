"""Boundary (Persistencia) — DAO de Notificacion."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from boundary.persistence.database import Database


class NotificacionDAO:
    """Rol ECB: Boundary (Persistencia)."""

    def __init__(self, db: Database) -> None:
        self._db = db

    def insertar(self, id_turno: int, fecha_hora_envio: datetime,
                 medio_envio: str) -> Optional[int]:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "INSERT INTO Notificacion (id_turno, fecha_hora_envio, estado,"
                " medio_envio, intentos) VALUES (%s, %s, 'Pendiente', %s, 0)",
                (id_turno, fecha_hora_envio, medio_envio),
            )
            return self._db.get_last_insert_id() if filas else None

    def obtener_pendientes(self) -> list[dict]:
        """Notificaciones pendientes cuyo momento de envío ya llegó (máx 3 intentos)."""
        with self._db:
            return self._db.obtener_registros(
                """SELECT n.id_notificacion, n.id_turno, n.medio_envio, n.intentos,
                          t.fecha, t.hora_inicio, t.id_paciente,
                          p.nombre, p.apellido,
                          m.nombre AS medico_nombre, m.apellido AS medico_apellido
                   FROM Notificacion n
                   JOIN Turno t ON n.id_turno = t.id_turno
                   JOIN Paciente p ON t.id_paciente = p.id_paciente
                   JOIN Medico m ON t.matricula = m.matricula
                   WHERE n.estado = 'Pendiente'
                     AND n.fecha_hora_envio <= NOW()
                     AND n.intentos < 3
                   ORDER BY n.fecha_hora_envio"""
            )

    def marcar_enviado(self, id_notificacion: int) -> None:
        with self._db:
            self._db.ejecutar_consulta(
                "UPDATE Notificacion SET estado='Enviado', fecha_envio_real=NOW()"
                " WHERE id_notificacion=%s",
                (id_notificacion,),
            )

    def marcar_error(self, id_notificacion: int, motivo: str) -> None:
        with self._db:
            self._db.ejecutar_consulta(
                "UPDATE Notificacion SET estado='Error', motivo_error=%s,"
                " intentos=intentos+1 WHERE id_notificacion=%s",
                (motivo, id_notificacion),
            )

    def incrementar_intento(self, id_notificacion: int, motivo: str) -> None:
        with self._db:
            self._db.ejecutar_consulta(
                "UPDATE Notificacion SET intentos=intentos+1, motivo_error=%s"
                " WHERE id_notificacion=%s",
                (motivo, id_notificacion),
            )
