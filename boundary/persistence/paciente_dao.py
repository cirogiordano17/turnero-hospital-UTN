"""Boundary (Persistencia) — DAO de Paciente."""
from __future__ import annotations
from datetime import date
from typing import Optional
from boundary.persistence.database import Database


class PacienteDAO:
    """
    Data Access Object para la tabla Paciente e Historial_clinico.

    Rol ECB: Boundary (Persistencia).
    """

    def __init__(self, db: Database) -> None:
        self._db = db

    def buscar_por_id(self, id_paciente: int) -> Optional[dict]:
        with self._db:
            return self._db.obtener_registro(
                "SELECT id_paciente, nombre, apellido, telefono,"
                " fecha_nacimiento, direccion, activo"
                " FROM Paciente WHERE id_paciente = %s",
                (id_paciente,),
            )

    def listar_activos(self) -> list[dict]:
        with self._db:
            return self._db.obtener_registros(
                "SELECT id_paciente, nombre, apellido, telefono,"
                " fecha_nacimiento, direccion"
                " FROM Paciente WHERE activo = 1 ORDER BY nombre, apellido"
            )

    def insertar(self, id_paciente: int, nombre: str, apellido: str,
                 telefono: str, fecha_nacimiento: date, direccion: str) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "INSERT INTO Paciente (id_paciente, nombre, apellido, telefono,"
                " fecha_nacimiento, direccion, activo) VALUES (%s,%s,%s,%s,%s,%s,1)",
                (id_paciente, nombre, apellido, telefono, fecha_nacimiento, direccion),
            )
            return bool(filas and filas > 0)

    def actualizar(self, id_paciente: int, nombre: str, apellido: str,
                   telefono: str, fecha_nacimiento: date, direccion: str) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "UPDATE Paciente SET nombre=%s, apellido=%s, telefono=%s,"
                " fecha_nacimiento=%s, direccion=%s WHERE id_paciente=%s",
                (nombre, apellido, telefono, fecha_nacimiento, direccion, id_paciente),
            )
            return bool(filas and filas > 0)

    def dar_de_baja(self, id_paciente: int) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "UPDATE Paciente SET activo = 0 WHERE id_paciente = %s",
                (id_paciente,),
            )
            return bool(filas and filas > 0)

    def obtener_historial(self, id_paciente: int) -> list[dict]:
        with self._db:
            return self._db.obtener_registros(
                """SELECT h.id_historial, h.diagnostico, h.tratamiento,
                          h.notas, h.observaciones, h.fecha_registro,
                          t.fecha, t.hora_inicio,
                          CONCAT(m.nombre, ' ', m.apellido) AS medico
                   FROM Historial_clinico h
                   JOIN Turno t ON h.id_turno = t.id_turno
                   JOIN Medico m ON t.matricula = m.matricula
                   WHERE h.id_paciente = %s
                   ORDER BY h.fecha_registro DESC""",
                (id_paciente,),
            )

    def obtener_contacto_principal(self, id_paciente: int) -> Optional[dict]:
        with self._db:
            return self._db.obtener_registro(
                "SELECT tipo_contacto, valor_contacto FROM Contactos_Paciente"
                " WHERE id_paciente = %s AND activo = TRUE"
                " ORDER BY es_principal DESC LIMIT 1",
                (id_paciente,),
            )
