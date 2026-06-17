"""Boundary (Persistencia) — DAO de Agenda."""
from __future__ import annotations
from datetime import time
from typing import Optional
from boundary.persistence.database import Database


class AgendaDAO:
    """Rol ECB: Boundary (Persistencia)."""

    def __init__(self, db: Database) -> None:
        self._db = db

    def listar_por_medico(self, matricula: int) -> list[dict]:
        with self._db:
            return self._db.obtener_registros(
                """SELECT a.id_agenda, a.matricula, a.id_consultorio,
                          a.dia_semana, a.hora_inicio, a.hora_fin,
                          c.numero AS consultorio_numero,
                          CONCAT(m.nombre, ' ', m.apellido) AS medico
                   FROM Agenda a
                   JOIN Medico m ON a.matricula = m.matricula
                   JOIN Consultorio c ON a.id_consultorio = c.id_consultorio
                   WHERE a.matricula = %s
                   ORDER BY FIELD(a.dia_semana,'Lunes','Martes','Miércoles',
                                  'Jueves','Viernes','Sábado','Domingo')""",
                (matricula,),
            )

    def listar_todas(self) -> list[dict]:
        with self._db:
            return self._db.obtener_registros(
                """SELECT a.id_agenda, a.matricula, a.id_consultorio,
                          a.dia_semana, a.hora_inicio, a.hora_fin,
                          c.numero AS consultorio_numero,
                          CONCAT(m.nombre, ' ', m.apellido) AS medico
                   FROM Agenda a
                   JOIN Medico m ON a.matricula = m.matricula
                   JOIN Consultorio c ON a.id_consultorio = c.id_consultorio
                   ORDER BY m.apellido, m.nombre"""
            )

    def buscar_por_id(self, id_agenda: int) -> Optional[dict]:
        with self._db:
            return self._db.obtener_registro(
                "SELECT * FROM Agenda WHERE id_agenda = %s", (id_agenda,)
            )

    def insertar(self, matricula: int, id_consultorio: int, dia_semana: str,
                 hora_inicio: time, hora_fin: time) -> Optional[int]:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "INSERT INTO Agenda (matricula, id_consultorio, dia_semana,"
                " hora_inicio, hora_fin) VALUES (%s,%s,%s,%s,%s)",
                (matricula, id_consultorio, dia_semana, hora_inicio, hora_fin),
            )
            return self._db.get_last_insert_id() if filas else None

    def actualizar(self, id_agenda: int, dia_semana: str,
                   hora_inicio: time, hora_fin: time) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "UPDATE Agenda SET dia_semana=%s, hora_inicio=%s, hora_fin=%s"
                " WHERE id_agenda=%s",
                (dia_semana, hora_inicio, hora_fin, id_agenda),
            )
            return bool(filas and filas > 0)

    def eliminar(self, id_agenda: int) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "DELETE FROM Agenda WHERE id_agenda = %s", (id_agenda,)
            )
            return bool(filas and filas > 0)
