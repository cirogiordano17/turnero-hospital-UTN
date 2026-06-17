"""Boundary (Persistencia) — DAO de Especialidad."""
from __future__ import annotations
from typing import Optional
from boundary.persistence.database import Database


class EspecialidadDAO:
    """Rol ECB: Boundary (Persistencia)."""

    def __init__(self, db: Database) -> None:
        self._db = db

    def listar_todas(self) -> list[dict]:
        with self._db:
            return self._db.obtener_registros(
                "SELECT id_especialidad, nombre, descripcion"
                " FROM Especialidad ORDER BY nombre"
            )

    def buscar_por_id(self, id_especialidad: int) -> Optional[dict]:
        with self._db:
            return self._db.obtener_registro(
                "SELECT id_especialidad, nombre, descripcion"
                " FROM Especialidad WHERE id_especialidad = %s",
                (id_especialidad,),
            )

    def insertar(self, nombre: str, descripcion: str) -> Optional[int]:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "INSERT INTO Especialidad (nombre, descripcion) VALUES (%s, %s)",
                (nombre, descripcion),
            )
            return self._db.get_last_insert_id() if filas else None

    def actualizar(self, id_especialidad: int, nombre: str, descripcion: str) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "UPDATE Especialidad SET nombre=%s, descripcion=%s"
                " WHERE id_especialidad=%s",
                (nombre, descripcion, id_especialidad),
            )
            return bool(filas and filas > 0)

    def eliminar(self, id_especialidad: int) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "DELETE FROM Especialidad WHERE id_especialidad = %s",
                (id_especialidad,),
            )
            return bool(filas and filas > 0)
