# -*- coding: utf-8 -*-
"""
Ejemplo de uso del ABMC de Médicos con entrada interactiva y almacenamiento en BD
"""

from datetime import date
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from gestores.gestor_medico import GestorMedico
from models.especialidad import Especialidad
from data.database import Database


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 60)
    print("SISTEMA ABMC DE MÉDICOS")
    print("=" * 60)
    print("\n1. Crear nuevos médicos")
    print("2. Listar médicos registrados (en memoria)")
    print("3. Listar médicos de la base de datos")
    print("4. Guardar médicos en base de datos")
    print("5. Modificar médico")
    print("6. Eliminar médico (marcar como inactivo)")
    print("7. Salir")
    print("\n" + "-" * 60)


def ingreso_cantidad_medicos() -> int:
    """Solicita la cantidad de médicos a crear"""
    while True:
        try:
            cantidad = int(input("\n¿Cuántos médicos deseas crear? "))
            if cantidad <= 0:
                print("[ERROR] La cantidad debe ser mayor a 0")
                continue
            return cantidad
        except ValueError:
            print("[ERROR] Ingresa un número válido")


def ingreso_datos_medico(numero: int) -> dict:
    """
    Solicita los datos de un médico
    
    Args:
        numero: Número de médico a ingresar
    
    Returns:
        Diccionario con los datos del médico
    """
    print(f"\n--- Médico #{numero} ---")
    
    # Matrícula
    while True:
        try:
            matricula = int(input("Matrícula: ").strip())
            if matricula <= 0:
                print("[ERROR] La matrícula debe ser un número positivo")
                continue
            break
        except ValueError:
            print("[ERROR] La matrícula debe ser un número válido")
    
    # Nombre
    while True:
        nombre = input("Nombre: ").strip()
        if nombre:
            break
        print("[ERROR] El nombre no puede estar vacío")
    
    # Apellido
    while True:
        apellido = input("Apellido: ").strip()
        if apellido:
            break
        print("[ERROR] El apellido no puede estar vacío")
    
    # Teléfono
    telefono = input("Teléfono: ").strip()
    
    # Email
    while True:
        email = input("Email: ").strip()
        if "@" in email:
            break
        print("[ERROR] El email debe contener @")
    
    # Fecha de ingreso
    while True:
        try:
            fecha_str = input("Fecha de ingreso (YYYY-MM-DD): ").strip()
            fecha_ingreso = date.fromisoformat(fecha_str)
            break
        except ValueError:
            print("[ERROR] Formato de fecha inválido. Usa YYYY-MM-DD")
    
    return {
        "matricula": matricula,
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "email": email,
        "fecha_alta": fecha_ingreso
    }


def crear_medicos_interactivo(gestor: GestorMedico) -> bool:
    """
    Permite crear múltiples médicos de forma interactiva
    
    Args:
        gestor: Instancia del GestorMedico
    
    Returns:
        True si se crearon médicos, False en caso contrario
    """
    cantidad = ingreso_cantidad_medicos()
    medicos_creados = []
    
    for i in range(1, cantidad + 1):
        datos = ingreso_datos_medico(i)
        
        medico = gestor.alta_medico(
            matricula=datos["matricula"],
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            telefono=datos["telefono"],
            email=datos["email"],
            fecha_alta=datos["fecha_alta"]
        )
        
        if medico:
            medicos_creados.append(medico)
    
    if medicos_creados:
        print(f"\n[OK] Se crearon {len(medicos_creados)} médico(s) exitosamente")
        return True
    else:
        print("\n[ERROR] No se pudo crear ningún médico")
        return False


def asignar_especialidades_interactivo(gestor: GestorMedico):
    """Permite asignar especialidades a los médicos creados"""
    medicos = gestor.get_medicos()
    
    if not medicos:
        print("[ERROR] No hay médicos para asignar especialidades")
        return
    
    # Crear especialidades disponibles
    especialidades = [
        Especialidad(1, "Cardiología", "Especialista del corazón"),
        Especialidad(2, "Neurología", "Especialista del sistema nervioso"),
        Especialidad(3, "Dermatología", "Especialista de la piel"),
        Especialidad(4, "Pediatría", "Especialista en medicina infantil"),
        Especialidad(5, "Oftalmología", "Especialista en enfermedades de los ojos"),
        Especialidad(6, "Psiquiatría", "Especialista en salud mental")
    ]
    
    print("\n--- Asignar Especialidades ---")
    print("\nEspecialidades disponibles:")
    for esp in especialidades:
        print(f"   {esp.get_nro_especialidad()}. {esp.get_nombre()}")
    
    for medico in medicos:
        print(f"\n¿Especialidades para {medico.get_nombre()} {medico.get_apellido()}?")
        print("(Ingresa los números separados por coma, ej: 1,3,5)")
        
        while True:
            try:
                entrada = input("Opción: ").strip()
                if not entrada:
                    break
                
                numeros = [int(x.strip()) for x in entrada.split(",")]
                
                for num in numeros:
                    if 1 <= num <= len(especialidades):
                        gestor.asignar_especialidad(
                            medico.get_matricula(),
                            especialidades[num - 1]
                        )
                    else:
                        print(f"[ERROR] {num} no es una opción válida")
                break
            except ValueError:
                print("[ERROR] Ingresa números válidos separados por coma")


def guardar_en_base_datos(gestor: GestorMedico) -> bool:
    """
    Guarda los médicos en la base de datos
    
    Args:
        gestor: Instancia del GestorMedico
    
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    medicos = gestor.get_medicos()
    
    if not medicos:
        print("[ERROR] No hay médicos para guardar")
        return False
    
    print("\n--- Conectando a Base de Datos ---")
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    guardados = 0
    
    for medico in medicos:
        try:
            query = """
            INSERT INTO Medico (matricula, nombre, apellido, telefono, email, fecha_ingreso, activo)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE)
            """
            
            params = (
                medico.get_matricula(),
                medico.get_nombre(),
                medico.get_apellido(),
                medico.get_telefono(),
                medico.get_email(),
                medico.get_fecha_alta()
            )
            
            resultado = db.ejecutar_consulta(query, params)
            
            if resultado is not None:
                # Asignar especialidades a la BD
                for especialidad in medico.get_especialidades():
                    query_esp = """
                    INSERT INTO Medico_especialidad (matricula, id_especialidad)
                    VALUES (%s, %s)
                    """
                    params_esp = (medico.get_matricula(), especialidad.get_nro_especialidad())
                    db.ejecutar_consulta(query_esp, params_esp)
                
                guardados += 1
                print(f"[OK] Médico {medico.get_nombre()} {medico.get_apellido()} guardado en BD")
        
        except Exception as e:
            print(f"[ERROR] Error al guardar {medico.get_nombre()}: {str(e)}")
    
    db.desconectar()
    
    if guardados > 0:
        print(f"\n[OK] {guardados} médico(s) guardado(s) en la base de datos")
        return True
    else:
        print("\n[ERROR] No se pudo guardar ningún médico")
        return False


def listar_medicos_bd() -> bool:
    """
    Lista todos los médicos de la base de datos
    
    Returns:
        True si se listaron correctamente, False en caso contrario
    """
    print("\n--- Conectando a Base de Datos ---")
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        query = """
        SELECT m.matricula, m.nombre, m.apellido, m.telefono, m.email, 
               m.fecha_ingreso, m.activo,
               GROUP_CONCAT(e.nombre SEPARATOR ', ') AS especialidades
        FROM Medico m
        LEFT JOIN Medico_especialidad me ON m.matricula = me.matricula
        LEFT JOIN Especialidad e ON me.id_especialidad = e.id_especialidad
        GROUP BY m.matricula, m.nombre, m.apellido, m.telefono, m.email, m.fecha_ingreso, m.activo
        ORDER BY m.nombre, m.apellido
        """
        
        medicos = db.obtener_registros(query)
        
        if medicos:
            print(f"\n[OK] Se encontraron {len(medicos)} médico(s) en la base de datos:\n")
            for medico in medicos:
                estado = "Activo" if medico['activo'] else "Inactivo"
                print(f"   Matrícula: {medico['matricula']}")
                print(f"   Nombre: {medico['nombre']} {medico['apellido']}")
                print(f"   Teléfono: {medico['telefono']}")
                print(f"   Email: {medico['email']}")
                print(f"   Fecha de ingreso: {medico['fecha_ingreso']}")
                print(f"   Estado: {estado}")
                if medico['especialidades']:
                    print(f"   Especialidades: {medico['especialidades']}")
                print()
            return True
        else:
            print("\n[INFO] No hay médicos registrados en la base de datos")
            return False
    
    except Exception as e:
        print(f"[ERROR] Error al listar médicos: {str(e)}")
        return False
    
    finally:
        db.desconectar()


def eliminar_medico_bd() -> bool:
    """
    Marca un médico como inactivo en la base de datos
    
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    print("\n--- Eliminar Médico ---")
    
    try:
        matricula = int(input("Ingresa la matrícula del médico a eliminar: ").strip())
    except ValueError:
        print("[ERROR] La matrícula debe ser un número válido")
        return False
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        # Verificar que el médico existe
        query_check = "SELECT matricula, nombre, apellido FROM Medico WHERE matricula = %s"
        medico = db.obtener_registro(query_check, (matricula,))
        
        if not medico:
            print(f"[ERROR] No se encontró médico con matrícula {matricula}")
            db.desconectar()
            return False
        
        # Actualizar activo a 0
        query = "UPDATE Medico SET activo = 0 WHERE matricula = %s"
        resultado = db.ejecutar_consulta(query, (matricula,))
        
        if resultado is not None and resultado > 0:
            print(f"[OK] Médico {medico['nombre']} {medico['apellido']} marcado como inactivo")
            db.desconectar()
            return True
        else:
            print("[ERROR] No se pudo marcar el médico como inactivo")
            db.desconectar()
            return False
    
    except Exception as e:
        print(f"[ERROR] Error al eliminar médico: {str(e)}")
        db.desconectar()
        return False


def modificar_medico_bd() -> bool:
    """
    Modifica los datos de un médico en la base de datos
    
    Returns:
        True si se modificó correctamente, False en caso contrario
    """
    print("\n--- Modificar Médico ---")
    
    try:
        matricula = int(input("Ingresa la matrícula del médico a modificar: ").strip())
    except ValueError:
        print("[ERROR] La matrícula debe ser un número válido")
        return False
    
    db = Database()
    
    if not db.conectar("127.0.0.1:3306/hospital_db"):
        print("[ERROR] No se pudo conectar a la base de datos")
        return False
    
    try:
        # Verificar que el médico existe
        query_check = "SELECT matricula, nombre, apellido, telefono, email, fecha_ingreso FROM Medico WHERE matricula = %s"
        medico = db.obtener_registro(query_check, (matricula,))
        
        if not medico:
            print(f"[ERROR] No se encontró médico con matrícula {matricula}")
            db.desconectar()
            return False
        
        print(f"\n[INFO] Médico encontrado: {medico['nombre']} {medico['apellido']}")
        print("\n¿Qué deseas modificar?")
        print("1. Nombre")
        print("2. Apellido")
        print("3. Teléfono")
        print("4. Email")
        print("5. Fecha de ingreso")
        print("6. Modificar todo")
        print("7. Cancelar")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        datos_actualizar = {}
        
        if opcion == "1":
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if nuevo_nombre:
                datos_actualizar['nombre'] = nuevo_nombre
            else:
                print("[ERROR] El nombre no puede estar vacío")
                db.desconectar()
                return False
        
        elif opcion == "2":
            nuevo_apellido = input("Nuevo apellido: ").strip()
            if nuevo_apellido:
                datos_actualizar['apellido'] = nuevo_apellido
            else:
                print("[ERROR] El apellido no puede estar vacío")
                db.desconectar()
                return False
        
        elif opcion == "3":
            nuevo_telefono = input("Nuevo teléfono: ").strip()
            datos_actualizar['telefono'] = nuevo_telefono
        
        elif opcion == "4":
            nuevo_email = input("Nuevo email: ").strip()
            if "@" in nuevo_email:
                datos_actualizar['email'] = nuevo_email
            else:
                print("[ERROR] El email no es válido")
                db.desconectar()
                return False
        
        elif opcion == "5":
            while True:
                try:
                    fecha_str = input("Nueva fecha de ingreso (YYYY-MM-DD): ").strip()
                    nueva_fecha = date.fromisoformat(fecha_str)
                    datos_actualizar['fecha_ingreso'] = nueva_fecha
                    break
                except ValueError:
                    print("[ERROR] Formato de fecha inválido. Usa YYYY-MM-DD")
        
        elif opcion == "6":
            # Modificar todos los campos
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if nuevo_nombre:
                datos_actualizar['nombre'] = nuevo_nombre
            
            nuevo_apellido = input("Nuevo apellido: ").strip()
            if nuevo_apellido:
                datos_actualizar['apellido'] = nuevo_apellido
            
            nuevo_telefono = input("Nuevo teléfono: ").strip()
            if nuevo_telefono:
                datos_actualizar['telefono'] = nuevo_telefono
            
            while True:
                nuevo_email = input("Nuevo email: ").strip()
                if "@" in nuevo_email:
                    datos_actualizar['email'] = nuevo_email
                    break
                print("[ERROR] El email no es válido")
            
            while True:
                try:
                    fecha_str = input("Nueva fecha de ingreso (YYYY-MM-DD): ").strip()
                    nueva_fecha = date.fromisoformat(fecha_str)
                    datos_actualizar['fecha_ingreso'] = nueva_fecha
                    break
                except ValueError:
                    print("[ERROR] Formato de fecha inválido. Usa YYYY-MM-DD")
        
        elif opcion == "7":
            print("[INFO] Modificación cancelada")
            db.desconectar()
            return False
        
        else:
            print("[ERROR] Opción no válida")
            db.desconectar()
            return False
        
        if not datos_actualizar:
            print("[ERROR] No hay datos para actualizar")
            db.desconectar()
            return False
        
        # Construir la consulta UPDATE dinámicamente
        campos = ", ".join([f"{campo} = %s" for campo in datos_actualizar.keys()])
        valores = list(datos_actualizar.values())
        valores.append(matricula)
        
        query = f"UPDATE Medico SET {campos} WHERE matricula = %s"
        resultado = db.ejecutar_consulta(query, tuple(valores))
        
        if resultado is not None and resultado > 0:
            print(f"[OK] Médico {medico['nombre']} {medico['apellido']} modificado exitosamente")
            db.desconectar()
            return True
        else:
            print("[ERROR] No se pudo modificar el médico")
            db.desconectar()
            return False
    
    except Exception as e:
        print(f"[ERROR] Error al modificar médico: {str(e)}")
        db.desconectar()
        return False


def main():
    gestor = GestorMedico()
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("=" * 60)
            print("CREAR NUEVOS MÉDICOS")
            print("=" * 60)
            crear_medicos_interactivo(gestor)
            asignar_especialidades_interactivo(gestor)
            input("\n[ENTER] para continuar...")
        
        elif opcion == "2":
            limpiar_pantalla()
            print("=" * 60)
            print("MÉDICOS REGISTRADOS (En Memoria)")
            print("=" * 60)
            gestor.listar_todos_medicos()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "3":
            limpiar_pantalla()
            print("=" * 60)
            print("MÉDICOS EN BASE DE DATOS")
            print("=" * 60)
            listar_medicos_bd()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "4":
            limpiar_pantalla()
            print("=" * 60)
            print("GUARDAR EN BASE DE DATOS")
            print("=" * 60)
            guardar_en_base_datos(gestor)
            input("\n[ENTER] para continuar...")
        
        elif opcion == "5":
            limpiar_pantalla()
            print("=" * 60)
            print("MODIFICAR MÉDICO")
            print("=" * 60)
            modificar_medico_bd()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "6":
            limpiar_pantalla()
            eliminar_medico_bd()
            input("\n[ENTER] para continuar...")
        
        elif opcion == "7":
            print("\n[OK] ¡Hasta luego!")
            break
        
        else:
            print("[ERROR] Opción no válida")
            input("\n[ENTER] para continuar...")


if __name__ == "__main__":
    main()
