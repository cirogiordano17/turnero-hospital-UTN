from typing import List, Optional, Dict
from datetime import time
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.agenda import Agenda
from data.database import Database


class GestorAgenda:
    """Clase gestora de operaciones ABMC de agendas"""
    
    def __init__(self):
        self.__agendas: List[Agenda] = []
        self.__agendas_bd: List[Dict] = []  # Almacenar datos de BD
    
    # ========== CARGAR DE BASE DE DATOS ==========
    def cargar_agendas_bd(self) -> bool:
        """
        Carga todas las agendas de la base de datos
        
        Returns:
            True si se cargaron correctamente, False en caso contrario
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            query = """
            SELECT a.id_agenda, a.matricula, a.id_consultorio, a.dia_semana,
                   a.hora_inicio, a.hora_fin, a.activa,
                   m.nombre as medico_nombre, m.apellido as medico_apellido,
                   c.numero as consultorio_numero
            FROM Agenda a
            JOIN Medico m ON a.matricula = m.matricula
            JOIN Consultorio c ON a.id_consultorio = c.id_consultorio
            ORDER BY a.matricula, a.dia_semana
            """
            
            agendas = db.obtener_registros(query)
            
            if agendas:
                self.__agendas_bd = agendas
                print(f"[OK] Se cargaron {len(agendas)} agenda(s) de la base de datos")
                return True
            else:
                print("[INFO] No hay agendas en la base de datos")
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al cargar agendas: {str(e)}")
            return False
        
        finally:
            db.desconectar()
    
    # ========== LISTAR AGENDAS DE BD ==========
    def listar_agendas_bd(self) -> bool:
        """
        Lista todas las agendas de la base de datos
        
        Returns:
            True si se listaron correctamente
        """
        if not self.__agendas_bd:
            if not self.cargar_agendas_bd():
                return False
        
        if self.__agendas_bd:
            print(f"\n[INFO] Total de agendas: {len(self.__agendas_bd)}\n")
            for agenda in self.__agendas_bd:
                self._mostrar_agenda_bd(agenda)
            return True
        else:
            print("[INFO] No hay agendas registradas")
            return False
    
    # ========== ALTA (CREATE) ==========
    def alta_agenda(self, medico, consultorio, dia_semana: str,
                   hora_inicio: time, hora_fin: time) -> Optional[Agenda]:
        """
        Da de alta una nueva agenda en el sistema
        
        Args:
            medico: Objeto Médico
            consultorio: Objeto Consultorio
            dia_semana: Día de la semana (Lunes, Martes, etc.)
            hora_inicio: Hora de inicio (HH:MM)
            hora_fin: Hora de fin (HH:MM)
        
        Returns:
            Agenda creada o None si hay error
        """
        try:
            if not medico or not consultorio:
                print("[ERROR] Médico y consultorio son obligatorios")
                return None
            
            if not dia_semana or not hora_inicio or not hora_fin:
                print("[ERROR] Día, hora inicio y hora fin son obligatorios")
                return None
            
            # Validar que no exista una agenda duplicada
            for a in self.__agendas:
                if (a.get_medico() == medico and 
                    a.get_consultorio() == consultorio and
                    a.get_dia_semana().lower() == dia_semana.lower()):
                    print(f"[ERROR] Ya existe agenda para este médico, consultorio y día")
                    return None
            
            # Validar que hora_fin > hora_inicio
            if hora_fin <= hora_inicio:
                print("[ERROR] La hora de fin debe ser mayor a la hora de inicio")
                return None
            
            # Crear nueva agenda
            nro_agenda = len(self.__agendas) + 1
            nueva_agenda = Agenda(
                nro_agenda,
                medico,
                consultorio,
                dia_semana,
                hora_inicio,
                hora_fin
            )
            
            self.__agendas.append(nueva_agenda)
            
            print(f"[OK] Agenda #{nro_agenda} dada de alta exitosamente")
            print(f"     Médico: {medico.get_nombre()} {medico.get_apellido()}")
            print(f"     Consultorio: {consultorio.get_numero()}")
            print(f"     {dia_semana}: {hora_inicio} - {hora_fin}")
            return nueva_agenda
        
        except Exception as e:
            print(f"[ERROR] Error al dar de alta agenda: {str(e)}")
            return None
    
    # ========== BAJA (DELETE) ==========
    def baja_agenda_bd(self, id_agenda: int) -> bool:
        """
        Da de baja una agenda en la base de datos
        
        Args:
            id_agenda: ID de agenda en BD a dar de baja
        
        Returns:
            True si se eliminó, False en caso contrario
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            # Verificar que la agenda existe
            query_check = """
            SELECT a.id_agenda, m.nombre as medico_nombre, m.apellido as medico_apellido,
                   c.numero as consultorio_numero
            FROM Agenda a
            JOIN Medico m ON a.matricula = m.matricula
            JOIN Consultorio c ON a.id_consultorio = c.id_consultorio
            WHERE a.id_agenda = %s
            """
            
            agenda = db.obtener_registro(query_check, (id_agenda,))
            
            if not agenda:
                print(f"[ERROR] No se encontró agenda con ID {id_agenda}")
                db.desconectar()
                return False
            
            # Eliminar la agenda
            query = "DELETE FROM Agenda WHERE id_agenda = %s"
            resultado = db.ejecutar_consulta(query, (id_agenda,))
            
            if resultado is not None and resultado > 0:
                print(f"[OK] Agenda #{id_agenda} dada de baja exitosamente")
                print(f"     Médico: {agenda['medico_nombre']} {agenda['medico_apellido']}")
                print(f"     Consultorio: {agenda['consultorio_numero']}")
                # Recargar agendas de BD
                self.__agendas_bd = []
                db.desconectar()
                return True
            else:
                print("[ERROR] No se pudo eliminar la agenda")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al eliminar agenda: {str(e)}")
            db.desconectar()
            return False
    
    # ========== MODIFICACIÓN (UPDATE) ==========
    def modificar_agenda_bd(self, id_agenda: int, dia_semana: Optional[str] = None,
                           hora_inicio: Optional[time] = None,
                           hora_fin: Optional[time] = None) -> bool:
        """
        Modifica una agenda en la base de datos
        
        Args:
            id_agenda: ID de agenda en BD a modificar
            dia_semana: Nuevo día de la semana (opcional)
            hora_inicio: Nueva hora de inicio (opcional)
            hora_fin: Nueva hora de fin (opcional)
        
        Returns:
            True si se modificó, False en caso contrario
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            # Verificar que la agenda existe
            query_check = "SELECT id_agenda FROM Agenda WHERE id_agenda = %s"
            agenda = db.obtener_registro(query_check, (id_agenda,))
            
            if not agenda:
                print(f"[ERROR] No se encontró agenda con ID {id_agenda}")
                db.desconectar()
                return False
            
            datos_actualizar = {}
            
            if dia_semana:
                datos_actualizar['dia_semana'] = dia_semana
            if hora_inicio:
                datos_actualizar['hora_inicio'] = hora_inicio
            if hora_fin:
                datos_actualizar['hora_fin'] = hora_fin
            
            if not datos_actualizar:
                print("[ERROR] No hay datos para actualizar")
                db.desconectar()
                return False
            
            # Construir la consulta UPDATE dinámicamente
            campos = ", ".join([f"{campo} = %s" for campo in datos_actualizar.keys()])
            valores = list(datos_actualizar.values())
            valores.append(id_agenda)
            
            query = f"UPDATE Agenda SET {campos} WHERE id_agenda = %s"
            resultado = db.ejecutar_consulta(query, tuple(valores))
            
            if resultado is not None and resultado > 0:
                print(f"[OK] Agenda #{id_agenda} modificada exitosamente")
                # Recargar agendas de BD
                self.__agendas_bd = []
                db.desconectar()
                return True
            else:
                print("[ERROR] No se pudo modificar la agenda")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al modificar agenda: {str(e)}")
            db.desconectar()
            return False
    
    # ========== CONSULTA (READ) ==========
    def consultar_agendas_medico_bd(self, matricula: int) -> bool:
        """
        Consulta agendas de un médico desde BD
        
        Args:
            matricula: Matrícula del médico
        
        Returns:
            True si se encontraron agendas
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            query = """
            SELECT a.id_agenda, a.matricula, a.dia_semana, a.hora_inicio, a.hora_fin,
                   m.nombre as medico_nombre, m.apellido as medico_apellido,
                   c.numero as consultorio_numero
            FROM Agenda a
            JOIN Medico m ON a.matricula = m.matricula
            JOIN Consultorio c ON a.id_consultorio = c.id_consultorio
            WHERE a.matricula = %s
            ORDER BY a.dia_semana
            """
            
            agendas = db.obtener_registros(query, (matricula,))
            
            if agendas:
                print(f"\n[OK] Se encontraron {len(agendas)} agenda(s):\n")
                for agenda in agendas:
                    self._mostrar_agenda_bd(agenda)
                db.desconectar()
                return True
            else:
                print(f"[ERROR] No se encontraron agendas para matrícula {matricula}")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al consultar agendas: {str(e)}")
            db.desconectar()
            return False
    
    # ========== MÉTODOS AUXILIARES ==========
    def _buscar_por_numero(self, nro_agenda: int) -> Optional[Agenda]:
        """Busca una agenda por número en memoria"""
        for agenda in self.__agendas:
            if agenda.get_nro_agenda() == nro_agenda:
                return agenda
        return None
    
    def _mostrar_agenda_bd(self, agenda: Dict) -> None:
        """Muestra los datos de una agenda de BD formateados"""
        print(f"   ID Agenda: {agenda['id_agenda']}")
        print(f"   Médico: {agenda['medico_nombre']} {agenda['medico_apellido']} (Mat: {agenda['matricula']})")
        print(f"   Consultorio: #{agenda['consultorio_numero']}")
        print(f"   Día: {agenda['dia_semana']}")
        print(f"   Horario: {agenda['hora_inicio']} - {agenda['hora_fin']}")
        if 'activa' in agenda:
            estado = "Activa" if agenda['activa'] else "Inactiva"
            print(f"   Estado: {estado}")
        print()
    
    def get_agendas(self) -> List[Agenda]:
        """Retorna la lista de agendas en memoria"""
        return self.__agendas.copy()
    
    def get_agendas_bd(self) -> List[Dict]:
        """Retorna la lista de agendas de BD"""
        return self.__agendas_bd.copy()
    
    def __repr__(self) -> str:
        return f"GestorAgenda(Agendas en memoria: {len(self.__agendas)}, Agendas en BD: {len(self.__agendas_bd)})"
