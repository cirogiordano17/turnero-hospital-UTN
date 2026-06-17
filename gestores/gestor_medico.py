from typing import List, Optional
from datetime import date
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.medico import Medico
from models.especialidad import Especialidad


class GestorMedico:
    """Clase gestora de operaciones ABMC de médicos"""
    
    def __init__(self):
        self.__medicos: List[Medico] = []
    
    # ========== ALTA (CREATE) ==========
    def alta_medico(self, matricula: int, nombre: str, apellido: str, telefono: str,
                    email: str, fecha_alta: date) -> Optional[Medico]:
        """
        Da de alta un nuevo médico en el sistema
        
        Args:
            matricula: Matrícula del médico
            nombre: Nombre del médico
            apellido: Apellido del médico
            telefono: Teléfono del médico
            email: Email del médico
            fecha_alta: Fecha de alta en el sistema
        
        Returns:
            Médico creado o None si hay error
        """
        try:
            if not nombre or not apellido or not email:
                print("[ERROR] El nombre, apellido y email son obligatorios")
                return None
            
            # Validar formato de email
            if "@" not in email:
                print("[ERROR] El email no es válido")
                return None
            
            # Verificar que no exista un médico con la misma matrícula
            if self._buscar_por_matricula(matricula):
                print(f"[ERROR] Ya existe un médico con la matrícula {matricula}")
                return None
            
            # Verificar que no exista un médico con el mismo email
            for m in self.__medicos:
                if m.get_email().lower() == email.lower():
                    print(f"[ERROR] Ya existe un médico con el email {email}")
                    return None
            
            # Crear nuevo médico
            nuevo_medico = Medico(
                matricula,
                nombre,
                apellido,
                telefono,
                email,
                fecha_alta
            )
            
            self.__medicos.append(nuevo_medico)
            
            print(f"[OK] Médico {nombre} {apellido} dado de alta exitosamente (Matrícula: {matricula})")
            return nuevo_medico
        
        except Exception as e:
            print(f"[ERROR] Error al dar de alta médico: {str(e)}")
            return None
    
    # ========== BAJA (DELETE) ==========
    def baja_medico(self, matricula: int) -> bool:
        """
        Da de baja un médico del sistema (baja lógica)
        
        Args:
            matricula: Matrícula del médico a dar de baja
        
        Returns:
            True si se eliminó, False en caso contrario
        """
        try:
            medico = self._buscar_por_matricula(matricula)
            
            if not medico:
                print(f"[ERROR] No se encontró médico con matrícula {matricula}")
                return False
            
            # Baja lógica: asignar fecha de baja
            medico.set_fecha_baja(date.today())
            
            nombre = medico.get_nombre()
            apellido = medico.get_apellido()
            print(f"[OK] Médico {nombre} {apellido} dado de baja exitosamente")
            return True
        
        except Exception as e:
            print(f"[ERROR] Error al dar de baja médico: {str(e)}")
            return False
    
    # ========== MODIFICACIÓN (UPDATE) ==========
    def modificar_medico(self, matricula: int, nombre: Optional[str] = None,
                        apellido: Optional[str] = None, telefono: Optional[str] = None,
                        email: Optional[str] = None) -> bool:
        """
        Modifica los datos de un médico
        
        Args:
            matricula: Matrícula del médico a modificar
            nombre: Nuevo nombre (opcional)
            apellido: Nuevo apellido (opcional)
            telefono: Nuevo teléfono (opcional)
            email: Nuevo email (opcional)
        
        Returns:
            True si se modificó, False en caso contrario
        """
        try:
            medico = self._buscar_por_matricula(matricula)
            
            if not medico:
                print(f"[ERROR] No se encontró médico con matrícula {matricula}")
                return False
            
            # Validar email si se proporciona
            if email and "@" not in email:
                print("[ERROR] El email no es válido")
                return False
            
            # Actualizar solo los campos proporcionados
            if nombre:
                medico.set_nombre(nombre)
            if apellido:
                medico.set_apellido(apellido)
            if telefono:
                medico.set_telefono(telefono)
            if email:
                medico.set_email(email)
            
            print(f"[OK] Médico matrícula {matricula} modificado exitosamente")
            return True
        
        except Exception as e:
            print(f"[ERROR] Error al modificar médico: {str(e)}")
            return False
    
    # ========== CONSULTA (READ) ==========
    def consultar_medico(self, matricula: int) -> Optional[Medico]:
        """
        Consulta un médico por matrícula
        
        Args:
            matricula: Matrícula del médico
        
        Returns:
            Médico encontrado o None
        """
        medico = self._buscar_por_matricula(matricula)
        if medico:
            self._mostrar_medico(medico)
            return medico
        else:
            print(f"[ERROR] No se encontró médico con matrícula {matricula}")
            return None
    
    def consultar_por_nombre(self, nombre: str) -> List[Medico]:
        """
        Consulta médicos por nombre (búsqueda parcial)
        
        Args:
            nombre: Nombre a buscar
        
        Returns:
            Lista de médicos encontrados
        """
        resultados = [m for m in self.__medicos 
                     if nombre.lower() in m.get_nombre().lower()]
        
        if resultados:
            print(f"\n[OK] Se encontraron {len(resultados)} médico(s):")
            for medico in resultados:
                self._mostrar_medico(medico)
        else:
            print(f"[ERROR] No se encontraron médicos con el nombre '{nombre}'")
        
        return resultados
    
    def consultar_por_especialidad(self, nombre_especialidad: str) -> List[Medico]:
        """
        Consulta médicos por especialidad
        
        Args:
            nombre_especialidad: Nombre de la especialidad a buscar
        
        Returns:
            Lista de médicos que tienen esa especialidad
        """
        resultados = []
        nombre_lower = nombre_especialidad.lower()
        
        for m in self.__medicos:
            if m.get_fecha_baja() is None:  # Solo activos
                especialidades = [e.get_nombre().lower() for e in m.get_especialidades()]
                if any(nombre_lower in esp for esp in especialidades):
                    resultados.append(m)
        
        if resultados:
            print(f"\n[OK] Se encontraron {len(resultados)} médico(s) en {nombre_especialidad}:")
            for medico in resultados:
                self._mostrar_medico(medico)
        else:
            print(f"[ERROR] No se encontraron médicos en {nombre_especialidad}")
        
        return resultados
    
    def listar_todos_medicos(self, solo_activos: bool = True) -> List[Medico]:
        """
        Lista todos los médicos del sistema
        
        Args:
            solo_activos: Si True, muestra solo médicos activos (sin baja)
        
        Returns:
            Lista de médicos
        """
        if solo_activos:
            medicos = [m for m in self.__medicos if m.get_fecha_baja() is None]
        else:
            medicos = self.__medicos
        
        if not medicos:
            print("[INFO] No hay médicos registrados")
            return []
        
        estado = "activos" if solo_activos else "registrados"
        print(f"\n[INFO] Total de médicos {estado}: {len(medicos)}\n")
        for medico in medicos:
            self._mostrar_medico(medico)
        
        return medicos.copy()
    
    # ========== GESTIÓN DE ESPECIALIDADES ==========
    def asignar_especialidad(self, matricula: int, especialidad: 'Especialidad') -> bool:
        """
        Asigna una especialidad a un médico
        
        Args:
            matricula: Matrícula del médico
            especialidad: Especialidad a asignar
        
        Returns:
            True si se asignó, False en caso contrario
        """
        try:
            medico = self._buscar_por_matricula(matricula)
            
            if not medico:
                print(f"[ERROR] No se encontró médico con matrícula {matricula}")
                return False
            
            medico.asignar_especialidad(especialidad)
            print(f"[OK] Especialidad {especialidad.get_nombre()} asignada a {medico.get_nombre()}")
            return True
        
        except Exception as e:
            print(f"[ERROR] Error al asignar especialidad: {str(e)}")
            return False
    
    # ========== MÉTODOS AUXILIARES ==========
    def _buscar_por_matricula(self, matricula: int) -> Optional[Medico]:
        """Busca un médico por matrícula"""
        for medico in self.__medicos:
            if medico.get_matricula() == matricula:
                return medico
        return None
    
    def _mostrar_medico(self, medico: Medico) -> None:
        """Muestra los datos de un médico formateados"""
        print(f"   Matrícula: {medico.get_matricula()}")
        print(f"   Nombre: {medico.get_nombre()} {medico.get_apellido()}")
        print(f"   Teléfono: {medico.get_telefono()}")
        print(f"   Email: {medico.get_email()}")
        print(f"   Fecha de alta: {medico.get_fecha_alta()}")
        if medico.get_fecha_baja():
            print(f"   Fecha de baja: {medico.get_fecha_baja()}")
        especialidades = medico.get_especialidades()
        if especialidades:
            esp_nombres = ", ".join([e.get_nombre() for e in especialidades])
            print(f"   Especialidades: {esp_nombres}")
        print()
    
    def get_medicos(self) -> List[Medico]:
        """Retorna la lista de médicos activos"""
        return [m for m in self.__medicos if m.get_fecha_baja() is None]
    
    def __repr__(self) -> str:
        activos = len([m for m in self.__medicos if m.get_fecha_baja() is None])
        return f"GestorMedico(Médicos activos: {activos}, Total: {len(self.__medicos)})"
