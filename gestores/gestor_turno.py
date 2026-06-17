from typing import List, Optional, Dict
from datetime import date, time
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.turno import Turno
from data.database import Database


class GestorTurno:
    """Clase gestora de operaciones ABMC de turnos"""
    
    def __init__(self):
        self.__turnos: List[Turno] = []
        self.__turnos_bd: List[Dict] = []
    
    # ========== CARGAR DE BASE DE DATOS ==========
    def cargar_turnos_bd(self) -> bool:
        """
        Carga todos los turnos de la base de datos
        
        Returns:
            True si se cargaron correctamente, False en caso contrario
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            query = """
            SELECT t.id_turno, t.id_paciente, t.matricula, t.id_consultorio,
                   t.fecha, t.hora_inicio, t.hora_fin, t.estado, t.observaciones,
                   p.nombre as paciente_nombre, p.apellido as paciente_apellido,
                   m.nombre as medico_nombre, m.apellido as medico_apellido,
                   c.numero as consultorio_numero
            FROM Turno t
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            JOIN Medico m ON t.matricula = m.matricula
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            ORDER BY t.fecha, t.hora_inicio
            """
            
            turnos = db.obtener_registros(query)
            
            if turnos:
                self.__turnos_bd = turnos
                print(f"[OK] Se cargaron {len(turnos)} turno(s) de la base de datos")
                return True
            else:
                print("[INFO] No hay turnos en la base de datos")
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al cargar turnos: {str(e)}")
            return False
        
        finally:
            db.desconectar()
    
    # ========== LISTAR TURNOS DE BD ==========
    def listar_turnos_bd(self) -> bool:
        """
        Lista todos los turnos de la base de datos
        
        Returns:
            True si se listaron correctamente
        """
        if not self.__turnos_bd:
            if not self.cargar_turnos_bd():
                return False
        
        if self.__turnos_bd:
            print(f"\n[INFO] Total de turnos: {len(self.__turnos_bd)}\n")
            for turno in self.__turnos_bd:
                self._mostrar_turno_bd(turno)
            return True
        else:
            print("[INFO] No hay turnos registrados")
            return False
    
    # ========== ALTA (CREATE) ==========
    def alta_turno(self, id_paciente: int, matricula: int, id_consultorio: int,
                   fecha: date, hora_inicio: time, hora_fin: time,
                   observaciones: str = "") -> bool:
        """
        Da de alta un nuevo turno en la base de datos

        Args:
            id_paciente: ID del paciente
            matricula: Matrícula del médico
            id_consultorio: ID del consultorio
            fecha: Fecha del turno
            hora_inicio: Hora de inicio del turno
            hora_fin: Hora de fin del turno
            observaciones: Observaciones (opcional)

        Returns:
            True si se creó exitosamente, False en caso contrario
        """
        db = Database()

        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False

        try:
            # Verificar que el paciente existe
            query_check_paciente = "SELECT id_paciente FROM Paciente WHERE id_paciente = %s AND activo = TRUE"
            paciente = db.obtener_registro(query_check_paciente, (id_paciente,))

            if not paciente:
                print(f"[ERROR] Paciente con ID {id_paciente} no existe o está inactivo")
                db.desconectar()
                return False

            # Verificar que el médico existe
            query_check_medico = "SELECT matricula FROM Medico WHERE matricula = %s AND activo = TRUE"
            medico = db.obtener_registro(query_check_medico, (matricula,))

            if not medico:
                print(f"[ERROR] Médico con matrícula {matricula} no existe o está inactivo")
                db.desconectar()
                return False

            # Verificar que el consultorio existe
            query_check_consultorio = "SELECT id_consultorio FROM Consultorio WHERE id_consultorio = %s"
            consultorio = db.obtener_registro(query_check_consultorio, (id_consultorio,))

            if not consultorio:
                print(f"[ERROR] Consultorio con ID {id_consultorio} no existe")
                db.desconectar()
                return False

            # Verificar que no existe un turno duplicado
            query_check_turno = """
            SELECT id_turno FROM Turno
            WHERE id_paciente = %s AND matricula = %s AND fecha = %s AND hora_inicio = %s
            """
            turno_existe = db.obtener_registro(query_check_turno, (id_paciente, matricula, fecha, hora_inicio))

            if turno_existe:
                print("[ERROR] Ya existe un turno para este paciente, médico y horario")
                db.desconectar()
                return False

            # Obtener id_agenda del médico
            query_agenda = "SELECT id_agenda FROM Agenda WHERE matricula = %s LIMIT 1"
            agenda = db.obtener_registro(query_agenda, (matricula,))
            
            if not agenda:
                print(f"[ERROR] No se encontró agenda para médico matrícula {matricula}")
                db.desconectar()
                return False
            
            id_agenda = agenda['id_agenda']
            
            # Crear el turno
            query = """
            INSERT INTO Turno (id_paciente, matricula, id_consultorio, id_agenda, fecha, hora_inicio, hora_fin, estado, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Programado', %s)
            """

            params = (id_paciente, matricula, id_consultorio, id_agenda, fecha, hora_inicio, hora_fin, observaciones)
            resultado = db.ejecutar_consulta(query, params)

            if resultado is not None and resultado > 0:
                id_turno_nuevo = resultado
                print(f"[OK] Turno creado exitosamente (ID: {id_turno_nuevo})")
                print(f"     Fecha: {fecha} de {hora_inicio} a {hora_fin}")
                print(f"     Consultorio: {id_consultorio}")
                
                # ✨ MOSTRAR NOTIFICACIÓN SIMULADA EN TERMINAL
                try:
                    self._mostrar_notificacion_terminal(id_turno_nuevo, id_paciente, matricula, fecha, hora_inicio, hora_fin, id_consultorio)
                except Exception as e:
                    print(f"     ⚠ Error al mostrar notificación: {str(e)}")
                
                self.__turnos_bd = []
                db.desconectar()
                return True
            else:
                print("[ERROR] No se pudo crear el turno")
                db.desconectar()
                return False

        except Exception as e:
            print(f"[ERROR] Error al crear turno: {str(e)}")
            db.desconectar()
            return False
    
    def _mostrar_notificacion_terminal(self, id_turno, id_paciente, matricula, fecha, hora_inicio, hora_fin, id_consultorio):
        """Muestra una notificación simulada en la terminal con todos los datos del turno"""
        
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return
        
        try:
            # Obtener datos completos del paciente, médico y especialidad
            query = """
            SELECT 
                p.nombre as paciente_nombre,
                p.apellido as paciente_apellido,
                p.telefono as paciente_telefono,
                p.direccion as paciente_direccion,
                p.fecha_nacimiento as paciente_nacimiento,
                m.nombre as medico_nombre,
                m.apellido as medico_apellido,
                me.id_especialidad,
                e.nombre as especialidad_nombre,
                c.numero as consultorio_numero,
                c.piso as consultorio_piso
            FROM Paciente p
            CROSS JOIN Medico m
            LEFT JOIN Medico_Especialidad me ON m.matricula = me.matricula
            LEFT JOIN Especialidad e ON me.id_especialidad = e.id_especialidad
            LEFT JOIN Consultorio c ON c.id_consultorio = %s
            WHERE p.id_paciente = %s AND m.matricula = %s
            LIMIT 1
            """
            
            datos = db.obtener_registro(query, (id_consultorio, id_paciente, matricula))
            
            if not datos:
                print("     ⚠ No se pudieron obtener los datos completos")
                return
            
            # Formatear fecha y hora
            from datetime import datetime, timedelta
            
            if isinstance(hora_inicio, str):
                hora_str = hora_inicio
            elif isinstance(hora_inicio, timedelta):
                total_seconds = int(hora_inicio.total_seconds())
                hora_str = f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}"
            else:
                hora_str = str(hora_inicio)[:5]
            
            if isinstance(hora_fin, str):
                hora_fin_str = hora_fin
            elif isinstance(hora_fin, timedelta):
                total_seconds = int(hora_fin.total_seconds())
                hora_fin_str = f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}"
            else:
                hora_fin_str = str(hora_fin)[:5]
            
            # Calcular edad
            if datos['paciente_nacimiento']:
                hoy = datetime.now().date()
                edad = hoy.year - datos['paciente_nacimiento'].year
                if (hoy.month, hoy.day) < (datos['paciente_nacimiento'].month, datos['paciente_nacimiento'].day):
                    edad -= 1
            else:
                edad = "N/A"
            
            # MOSTRAR NOTIFICACIÓN ESTILO BANNER
            print("\n" + "═" * 80)
            print("║" + " " * 78 + "║")
            print("║" + "📧 NOTIFICACIÓN DE TURNO PROGRAMADO".center(78) + "║")
            print("║" + " " * 78 + "║")
            print("═" * 80)
            
            print("\n👤 DATOS DEL PACIENTE")
            print("─" * 80)
            print(f"   Nombre completo:  {datos['paciente_nombre']} {datos['paciente_apellido']}")
            print(f"   Edad:             {edad} años")
            if datos['paciente_telefono']:
                print(f"   Teléfono:         {datos['paciente_telefono']}")
            if datos['paciente_direccion']:
                print(f"   Dirección:        {datos['paciente_direccion']}")
            
            print("\n🏥 DATOS DEL TURNO")
            print("─" * 80)
            print(f"   Nº de Turno:      #{id_turno}")
            print(f"   Fecha:            {fecha.strftime('%d/%m/%Y') if hasattr(fecha, 'strftime') else fecha}")
            print(f"   Horario:          {hora_str} - {hora_fin_str}")
            print(f"   Duración:         {hora_fin_str} - {hora_str}")
            print(f"   Estado:           PROGRAMADO ✓")
            
            print("\n👨‍⚕️ DATOS DEL MÉDICO")
            print("─" * 80)
            print(f"   Profesional:      Dr/a. {datos['medico_nombre']} {datos['medico_apellido']}")
            if datos['especialidad_nombre']:
                print(f"   Especialidad:     {datos['especialidad_nombre']}")
            print(f"   Matrícula:        {matricula}")
            
            print("\n📍 UBICACIÓN")
            print("─" * 80)
            print(f"   Consultorio:      Nº {datos['consultorio_numero']}")
            print(f"   Piso:             {datos['consultorio_piso']}")
            
            print("\n💬 MENSAJE AL PACIENTE")
            print("─" * 80)
            mensaje = f"""
   Estimado/a {datos['paciente_nombre']} {datos['paciente_apellido']}:
   
   Se ha programado exitosamente su turno médico con el/la Dr/a. 
   {datos['medico_apellido']}, {datos['medico_nombre']}.
   
   📅 Fecha: {fecha.strftime('%d/%m/%Y') if hasattr(fecha, 'strftime') else fecha}
   ⏰ Hora: {hora_str}
   🏥 Consultorio Nº {datos['consultorio_numero']} - Piso {datos['consultorio_piso']}
   {f"🩺 Especialidad: {datos['especialidad_nombre']}" if datos['especialidad_nombre'] else ""}
   
   Por favor, llegue 10 minutos antes de su turno.
   Si necesita cancelar, hágalo con 24hs de anticipación.
   
   ¡Gracias por confiar en nosotros!
            """
            print(mensaje)
            
            print("═" * 80)
            print("║" + "Sistema de Gestión de Turnos - Hospital DAO".center(78) + "║")
            print("═" * 80 + "\n")
            
        except Exception as e:
            print(f"     ⚠ Error al generar notificación: {str(e)}")
        finally:
            db.desconectar()
    
    # ========== BAJA (DELETE) ==========
    def baja_turno_bd(self, id_turno: int) -> bool:
        """
        Cancela un turno en la base de datos (cambia estado a 'Cancelado')
        
        Args:
            id_turno: ID del turno a cancelar
        
        Returns:
            True si se canceló, False en caso contrario
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            # Verificar que el turno existe
            query_check = """
            SELECT t.id_turno, p.nombre as paciente_nombre, p.apellido as paciente_apellido,
                   m.nombre as medico_nombre, m.apellido as medico_apellido,
                   t.fecha, t.hora_inicio, t.hora_fin, t.estado
            FROM Turno t
            JOIN Medico m ON t.matricula = m.matricula
            LEFT JOIN Paciente p ON t.id_paciente = p.id_paciente
            WHERE t.id_turno = %s
            """
            
            turno = db.obtener_registro(query_check, (id_turno,))
            
            if not turno:
                print(f"[ERROR] No se encontró turno con ID {id_turno}")
                db.desconectar()
                return False
            
            # Verificar que el turno no está ya cancelado
            if turno['estado'] == 'Cancelado':
                print(f"[ERROR] El turno #{id_turno} ya está cancelado")
                db.desconectar()
                return False
            
            # Cambiar el estado del turno a 'Cancelado'
            query = "UPDATE Turno SET estado = 'Cancelado' WHERE id_turno = %s"
            resultado = db.ejecutar_consulta(query, (id_turno,))
            
            if resultado is not None and resultado > 0:
                print(f"[OK] Turno #{id_turno} cancelado exitosamente")
                print(f"     Fecha: {turno['fecha']} a las {turno['hora_inicio']}")
                print(f"     Médico: Dr/Dra. {turno['medico_nombre']} {turno['medico_apellido']}")
                if turno['paciente_nombre']:
                    print(f"     Paciente: {turno['paciente_nombre']} {turno['paciente_apellido']}")
                print(f"     Nuevo estado: CANCELADO")
                self.__turnos_bd = []
                db.desconectar()
                return True
            else:
                print("[ERROR] No se pudo cancelar el turno")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al cancelar turno: {str(e)}")
            db.desconectar()
            return False
    
    # ========== MODIFICACIÓN (UPDATE) ==========
    def modificar_turno_bd(self, id_turno: int, fecha: Optional[date] = None,
                          hora_inicio: Optional[time] = None,
                          hora_fin: Optional[time] = None,
                          estado: Optional[str] = None,
                          observaciones: Optional[str] = None) -> bool:
        """
        Modifica un turno en la base de datos
        
        Args:
            id_turno: ID del turno a modificar
            fecha: Nueva fecha (opcional)
            hora_inicio: Nueva hora de inicio (opcional)
            hora_fin: Nueva hora de fin (opcional)
            estado: Nuevo estado (opcional)
            observaciones: Nuevas observaciones (opcional)
        
        Returns:
            True si se modificó, False en caso contrario
        """
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            # Verificar que el turno existe
            query_check = "SELECT id_turno FROM Turno WHERE id_turno = %s"
            turno = db.obtener_registro(query_check, (id_turno,))
            
            if not turno:
                print(f"[ERROR] No se encontró turno con ID {id_turno}")
                db.desconectar()
                return False
            
            datos_actualizar = {}
            
            if fecha:
                datos_actualizar['fecha'] = fecha
            if hora_inicio:
                datos_actualizar['hora_inicio'] = hora_inicio
            if hora_fin:
                datos_actualizar['hora_fin'] = hora_fin
            if estado:
                estados_validos = ['Libre', 'Programado', 'Atendido', 'Cancelado', 'Inasistencia']
                if estado not in estados_validos:
                    print(f"[ERROR] Estado '{estado}' no válido. Válidos: {', '.join(estados_validos)}")
                    db.desconectar()
                    return False
                datos_actualizar['estado'] = estado
            if observaciones:
                datos_actualizar['observaciones'] = observaciones
            
            if not datos_actualizar:
                print("[ERROR] No hay datos para actualizar")
                db.desconectar()
                return False
            
            campos = ", ".join([f"{campo} = %s" for campo in datos_actualizar.keys()])
            valores = list(datos_actualizar.values())
            valores.append(id_turno)
            
            query = f"UPDATE Turno SET {campos} WHERE id_turno = %s"
            resultado = db.ejecutar_consulta(query, tuple(valores))
            
            if resultado is not None and resultado > 0:
                print(f"[OK] Turno #{id_turno} modificado exitosamente")
                self.__turnos_bd = []
                db.desconectar()
                return True
            else:
                print("[ERROR] No se pudo modificar el turno")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al modificar turno: {str(e)}")
            db.desconectar()
            return False
    
    # ========== CONSULTA (READ) ==========
    def consultar_turnos_paciente_bd(self, id_paciente: int) -> bool:
        """Consulta turnos de un paciente desde BD"""
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            query = """
            SELECT t.id_turno, t.fecha, t.hora_inicio, t.hora_fin, t.estado, t.observaciones,
                   m.nombre as medico_nombre, m.apellido as medico_apellido,
                   c.numero as consultorio_numero
            FROM Turno t
            JOIN Medico m ON t.matricula = m.matricula
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE t.id_paciente = %s
            ORDER BY t.fecha, t.hora_inicio
            """
            
            turnos = db.obtener_registros(query, (id_paciente,))
            
            if turnos:
                print(f"\n[OK] Se encontraron {len(turnos)} turno(s) para paciente ID {id_paciente}:\n")
                for turno in turnos:
                    self._mostrar_turno_bd(turno)
                db.desconectar()
                return True
            else:
                print(f"[ERROR] No se encontraron turnos para paciente ID {id_paciente}")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al consultar turnos: {str(e)}")
            db.desconectar()
            return False
    
    def consultar_turnos_medico_bd(self, matricula: int) -> bool:
        """Consulta turnos de un médico desde BD"""
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            query = """
            SELECT t.id_turno, t.matricula, t.fecha, t.hora_inicio, t.hora_fin, t.estado, t.observaciones,
                   p.nombre as paciente_nombre, p.apellido as paciente_apellido,
                   c.numero as consultorio_numero
            FROM Turno t
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE t.matricula = %s
            ORDER BY t.fecha, t.hora_inicio
            """
            
            turnos = db.obtener_registros(query, (matricula,))
            
            if turnos:
                print(f"\n[OK] Se encontraron {len(turnos)} turno(s) para médico matrícula {matricula}:\n")
                for turno in turnos:
                    self._mostrar_turno_bd(turno)
                db.desconectar()
                return True
            else:
                print(f"[ERROR] No se encontraron turnos para médico matrícula {matricula}")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al consultar turnos: {str(e)}")
            db.desconectar()
            return False
    
    def consultar_turnos_fecha_bd(self, fecha: date) -> bool:
        """Consulta turnos de una fecha específica desde BD"""
        db = Database()
        
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            print("[ERROR] No se pudo conectar a la base de datos")
            return False
        
        try:
            query = """
            SELECT t.id_turno, t.hora_inicio, t.hora_fin, t.estado, t.observaciones,
                   p.nombre as paciente_nombre, p.apellido as paciente_apellido,
                   m.nombre as medico_nombre, m.apellido as medico_apellido,
                   c.numero as consultorio_numero
            FROM Turno t
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            JOIN Medico m ON t.matricula = m.matricula
            JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
            WHERE t.fecha = %s
            ORDER BY t.hora_inicio
            """
            
            turnos = db.obtener_registros(query, (fecha,))
            
            if turnos:
                print(f"\n[OK] Se encontraron {len(turnos)} turno(s) para {fecha}:\n")
                for turno in turnos:
                    self._mostrar_turno_bd(turno)
                db.desconectar()
                return True
            else:
                print(f"[ERROR] No se encontraron turnos para {fecha}")
                db.desconectar()
                return False
        
        except Exception as e:
            print(f"[ERROR] Error al consultar turnos: {str(e)}")
            db.desconectar()
            return False
    
    # ========== MÉTODOS AUXILIARES ==========
    def _mostrar_turno_bd(self, turno: Dict) -> None:
        """Muestra los datos de un turno de BD formateados"""
        print(f"   ID Turno: {turno['id_turno']}")
        if 'paciente_nombre' in turno:
            print(f"   Paciente: {turno['paciente_nombre']} {turno['paciente_apellido']}")
        if 'medico_nombre' in turno:
            print(f"   Médico: {turno['medico_nombre']} {turno['medico_apellido']}")
        print(f"   Consultorio: #{turno['consultorio_numero']}")
        if 'fecha' in turno:
            print(f"   Fecha: {turno['fecha']}")
        print(f"   Horario: {turno['hora_inicio']} - {turno['hora_fin']}")
        print(f"   Estado: {turno['estado']}")
        if turno.get('observaciones'):
            print(f"   Observaciones: {turno['observaciones']}")
        print()

    def get_turnos_bd(self) -> List[Dict]:
        """Retorna la lista de turnos de BD"""
        return self.__turnos_bd.copy()
    
    def __repr__(self) -> str:
        return f"GestorTurno(Turnos en BD: {len(self.__turnos_bd)})"