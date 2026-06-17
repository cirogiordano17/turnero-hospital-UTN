"""Boundary (Persistencia) — DAO de Medico."""
from __future__ import annotations
from datetime import date
from typing import Optional
from boundary.persistence.database import Database


class MedicoDAO:
    """
    Data Access Object para la tabla Medico y Medico_Especialidad.

    Rol ECB: Boundary (Persistencia).
    """

    def __init__(self, db: Database) -> None:
        self._db = db

    def buscar_por_matricula(self, matricula: int) -> Optional[dict]:
        with self._db:
            return self._db.obtener_registro(
                "SELECT matricula, nombre, apellido, telefono, email,"
                " fecha_ingreso, activo FROM Medico WHERE matricula = %s",
                (matricula,),
            )

    def listar_activos(self) -> list[dict]:
        with self._db:
            return self._db.obtener_registros(
                "SELECT matricula, nombre, apellido, telefono, email, fecha_ingreso"
                " FROM Medico WHERE activo = 1 ORDER BY nombre, apellido"
            )

    def insertar(self, matricula: int, nombre: str, apellido: str,
                 telefono: str, email: str, fecha_alta: date) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "INSERT INTO Medico (matricula, nombre, apellido, telefono, email,"
                " fecha_ingreso, activo) VALUES (%s, %s, %s, %s, %s, %s, 1)",
                (matricula, nombre, apellido, telefono, email, fecha_alta),
            )
            return bool(filas and filas > 0)

    def actualizar(self, matricula: int, nombre: str, apellido: str,
                   telefono: str, email: str, fecha_alta: date) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "UPDATE Medico SET nombre=%s, apellido=%s, telefono=%s,"
                " email=%s, fecha_ingreso=%s WHERE matricula=%s",
                (nombre, apellido, telefono, email, fecha_alta, matricula),
            )
            return bool(filas and filas > 0)

    def dar_de_baja(self, matricula: int) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "UPDATE Medico SET activo = 0 WHERE matricula = %s", (matricula,)
            )
            return bool(filas and filas > 0)

    def obtener_especialidades(self, matricula: int) -> list[dict]:
        with self._db:
            return self._db.obtener_registros(
                "SELECT e.id_especialidad, e.nombre FROM Especialidad e"
                " JOIN Medico_Especialidad me ON e.id_especialidad = me.id_especialidad"
                " WHERE me.matricula = %s ORDER BY e.nombre",
                (matricula,),
            )

    def asignar_especialidad(self, matricula: int, id_especialidad: int) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "INSERT IGNORE INTO Medico_Especialidad (matricula, id_especialidad)"
                " VALUES (%s, %s)",
                (matricula, id_especialidad),
            )
            return filas is not None
