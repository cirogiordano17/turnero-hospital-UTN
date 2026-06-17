"""
Script principal - Ejemplo de uso del sistema de gestión médica
"""

from datetime import date, time, datetime
from data.database import Database
from models.medico import Medico
from models.paciente import Paciente
from models.especialidad import Especialidad
from models.consultorio import Consultorio
from models.agenda import Agenda
from models.turno import Turno
from gestores.gestor_turno import GestorTurno
from models.receta import Receta
from models.detalle_receta import DetalleDeReceta
from models.historial_clinico import HistorialClinico
from models.medicamento import Medicamento
from models.laboratorio import Laboratorio
from models.notificacion import Notificacion
from models.enums import TipoLaboratorioEnum


def main():
    print("=" * 60)
    print("SISTEMA DE GESTIÓN MÉDICA - DEMOSTRACIÓN")
    print("=" * 60)
    
    # ========== INICIALIZAR BASE DE DATOS ==========
    print("\n🗄️  Inicializando base de datos...")
    db = Database()
    
    # Conectar a la base de datos
    if db.conectar("127.0.0.1:3306/hospital_db"):
        print(f"   Estado: {db}")
        
        # ========== CONSULTAR DATOS ==========
        print("\n📋 Datos cargados en la base de datos:\n")
        
        # Consultar médicos
        print("   👨‍⚕️  MÉDICOS:")
        medicos = db.obtener_registros("SELECT * FROM Medico WHERE activo = TRUE")
        for medico in medicos:
            print(f"      - {medico['nombre']} {medico['apellido']} (Matrícula: {medico['matricula']})")
        
        # Consultar pacientes
        print("\n   👥 PACIENTES:")
        pacientes = db.obtener_registros("SELECT * FROM Paciente WHERE activo = TRUE")
        for paciente in pacientes:
            print(f"      - {paciente['nombre']} {paciente['apellido']}")
        
        # Consultar turnos
        print("\n   ⏰ TURNOS PROGRAMADOS:")
        turnos = db.obtener_registros("""
            SELECT t.id_turno, m.nombre as medico, p.nombre as paciente, 
                   t.fecha, t.hora, t.estado
            FROM Turno t
            JOIN Medico m ON t.matricula = m.matricula
            JOIN Paciente p ON t.id_paciente = p.id_paciente
            ORDER BY t.fecha, t.hora
        """)
        for turno in turnos:
            print(f"      - Turno #{turno['id_turno']}: {turno['paciente']} con Dr. {turno['medico']} "
                  f"el {turno['fecha']} a las {turno['hora']} ({turno['estado']})")
        
        # Consultar especialidades
        print("\n   📚 ESPECIALIDADES:")
        especialidades = db.obtener_registros("SELECT * FROM Especialidad")
        for esp in especialidades:
            print(f"      - {esp['nombre']}: {esp['descripcion']}")
        
        # Desconectar
        db.desconectar()
    else:
        print("   ✗ No se pudo conectar a la base de datos")

if __name__ == "__main__":
    main()