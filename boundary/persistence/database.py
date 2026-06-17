"""Boundary (Persistencia) — Singleton de acceso a MySQL."""
from __future__ import annotations
import os
import logging
from typing import Optional, Any
import mysql.connector
from mysql.connector import Error as MySQLError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class Database:
    """
    Singleton que gestiona la conexión a MySQL.

    Lee las credenciales exclusivamente desde variables de entorno
    (archivo .env), eliminando cualquier valor hardcodeado en el código.

    Uso con context manager (recomendado en DAOs):
        with Database() as db:
            resultado = db.obtener_registro(query, params)

    Rol ECB: Boundary (Persistencia).
    """

    _instance: Optional["Database"] = None

    def __new__(cls) -> "Database":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._configured = False
        return cls._instance

    def __init__(self) -> None:
        if self._configured:
            return
        self._host = os.getenv("DB_HOST", "127.0.0.1")
        self._port = int(os.getenv("DB_PORT", "3306"))
        self._user = os.getenv("DB_USER", "root")
        self._password = os.getenv("DB_PASSWORD", "1234")
        self._database = os.getenv("DB_NAME", "hospital_db")
        self.connection: Optional[mysql.connector.MySQLConnection] = None
        self.last_insert_id: int = 0
        self._configured = True

    # -- Ciclo de vida de la conexión --

    def conectar(self) -> bool:
        """Abre la conexión. Idempotente si ya está abierta."""
        if self.connection and self.connection.is_connected():
            return True
        try:
            self.connection = mysql.connector.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                database=self._database,
                charset="utf8mb4",
                collation="utf8mb4_unicode_ci",
            )
            return self.connection.is_connected()
        except MySQLError as exc:
            logger.error("Error al conectar a la base de datos: %s", exc)
            return False

    def desconectar(self) -> None:
        """Cierra la conexión si está abierta."""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    # -- Context manager --

    def __enter__(self) -> "Database":
        self.conectar()
        return self

    def __exit__(self, *_: Any) -> None:
        self.desconectar()

    # -- API de consultas --

    def ejecutar_consulta(self, query: str, params: tuple = ()) -> Optional[int]:
        """
        Ejecuta un INSERT / UPDATE / DELETE.

        Returns:
            Filas afectadas (>= 0) o None si ocurrió un error.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            self.last_insert_id = cursor.lastrowid
            affected = cursor.rowcount
            cursor.close()
            return affected
        except MySQLError as exc:
            logger.error("Error en consulta: %s | params: %s | error: %s", query, params, exc)
            self.connection.rollback()
            return None

    def get_last_insert_id(self) -> int:
        return self.last_insert_id

    def obtener_registro(self, query: str, params: tuple = ()) -> Optional[dict]:
        """
        Ejecuta un SELECT y retorna la primera fila como dict.

        Returns:
            Dict con los datos o None si no hay resultado / error.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            row = cursor.fetchone()
            cursor.close()
            return row
        except MySQLError as exc:
            logger.error("Error en consulta: %s | error: %s", query, exc)
            return None

    def obtener_registros(self, query: str, params: tuple = ()) -> list[dict]:
        """
        Ejecuta un SELECT y retorna todas las filas como lista de dicts.

        Returns:
            Lista de dicts (puede estar vacía). Nunca None.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cursor.close()
            return rows or []
        except MySQLError as exc:
            logger.error("Error en consulta: %s | error: %s", query, exc)
            return []

    def __repr__(self) -> str:
        estado = "conectado" if (self.connection and self.connection.is_connected()) else "desconectado"
        return f"Database({self._database}@{self._host}:{self._port} [{estado}])"
