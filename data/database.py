from typing import Optional
import mysql.connector
from mysql.connector import Error
from datetime import datetime


class Database:
    """Clase para manejar la conexión a la base de datos MySQL"""
    
    _instancia: Optional['Database'] = None
    
    def __init__(self):
        """Inicializa la conexión a la BD"""
        if not hasattr(self, '_initialized'):
            self.connection = None
            self.host = "127.0.0.1"
            self.port = 3306
            self.user = "root"
            self.password = "1234"  # ← CAMBIAR AQUÍ || si no tienes contraseña, dejar vacío: self.password = ""
            self.database = "hospital_db"
            self._initialized = True
    
    @classmethod
    def obtener_instancia(cls):
        """Obtiene la única instancia de Database"""
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia
    
    def conectar(self, connection_string=None):
        """
        Conecta a la base de datos
        
        Args:
            connection_string: Formato "host:puerto/database" (opcional)
        """
        try:
            if connection_string:
                # Parsear connection_string
                parts = connection_string.split('/')
                host_port = parts[0].split(':')
                self.host = host_port[0]
                self.port = int(host_port[1]) if len(host_port) > 1 else 3306
                self.database = parts[1] if len(parts) > 1 else "hospital_db"
            
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print(f"✓ Conectado a MySQL Server versión {db_info}")
                return True
            
        except Error as e:
            print(f"✗ Error al conectar a la base de datos: {e}")
            return False
    
    def desconectar(self):
        """Desconecta de la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Desconexión exitosa")
    
    def ejecutar_consulta(self, query, params=None):
        """
        Ejecuta una consulta SQL (INSERT, UPDATE, DELETE)
        
        Args:
            query: Consulta SQL
            params: Parámetros para la consulta (tupla)
        
        Returns:
            Número de filas afectadas o None si hay error
        """
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            
            # Guardar el ID del último registro insertado
            self.last_insert_id = cursor.lastrowid
            
            affected_rows = cursor.rowcount
            cursor.close()
            
            return affected_rows
        
        except Error as e:
            print(f"✗ Error en consulta: {e}")
            return None
    
    def get_last_insert_id(self):
        """Retorna el ID del último registro insertado"""
        return getattr(self, 'last_insert_id', 0)
    
    def obtener_registro(self, query, params=None):
        """
        Obtiene un registro de la base de datos
        
        Args:
            query: Consulta SELECT
            params: Parámetros para la consulta
        
        Returns:
            Un diccionario con el registro o None
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            resultado = cursor.fetchone()
            cursor.close()
            
            return resultado
        
        except Error as e:
            print(f"✗ Error en consulta: {e}")
            return None
    
    def obtener_registros(self, query, params=None):
        """
        Obtiene múltiples registros de la base de datos
        
        Args:
            query: Consulta SELECT
            params: Parámetros para la consulta
        
        Returns:
            Lista de diccionarios con los registros
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            resultados = cursor.fetchall()
            cursor.close()
            
            return resultados
        
        except Error as e:
            print(f"✗ Error en consulta: {e}")
            return None
    
    def __str__(self):
        if self.connection and self.connection.is_connected():
            return f"Conectado a {self.database} en {self.host}:{self.port}"
        return "No conectado"