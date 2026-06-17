from typing import List, Optional
from datetime import date
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from models.paciente import Paciente


class GestorPaciente:
    """Clase gestora de operaciones ABMC de pacientes"""
    
    def __init__(self):
        self.__pacientes: List[Paciente] = []
    
    # ========== ALTA (CREATE) ==========
    def alta_paciente(self, nro_paciente: int, nombre: str, apellido: str, 
                      telefono: str, fecha_nacimiento: date, 
                      direccion: str) -> Optional[Paciente]:
        """
        Da de alta un nuevo paciente en el sistema
        
        Args:
            nro_paciente: ID del paciente
            nombre: Nombre del paciente
            apellido: Apellido del paciente
            telefono: Teléfono del paciente
            fecha_nacimiento: Fecha de nacimiento
            direccion: Dirección del paciente
        
        Returns:
            Paciente creado o None si hay error
        """
        try:
            if not nombre or not apellido:
                print("[ERROR] El nombre y apellido son obligatorios")
                return None
            
            # Verificar que no exista un paciente con el mismo ID
            if self._buscar_por_id(nro_paciente):
                print(f"[ERROR] Ya existe un paciente con el ID {nro_paciente}")
                return None
            
            # Verificar que no exista un paciente con los mismos datos
            for p in self.__pacientes:
                if (p.get_nombre().lower() == nombre.lower() and 
                    p.get_apellido().lower() == apellido.lower()):
                    print(f"[ERROR] Ya existe un paciente con el nombre {nombre} {apellido}")
                    return None
            
            # Crear nuevo paciente
            nuevo_paciente = Paciente(
                nro_paciente,
                nombre,
                apellido,
                telefono,
                fecha_nacimiento,
                direccion
            )
            
            self.__pacientes.append(nuevo_paciente)
            
            print(f"[OK] Paciente {nombre} {apellido} dado de alta exitosamente (ID: {nro_paciente})")
            return nuevo_paciente
        
        except Exception as e:
            print(f"[ERROR] Error al dar de alta paciente: {str(e)}")
            return None
    
    # ========== BAJA (DELETE) ==========
    def baja_paciente(self, nro_paciente: int) -> bool:
        """
        Da de baja un paciente del sistema
        
        Args:
            nro_paciente: Número de paciente a dar de baja
        
        Returns:
            True si se eliminó, False en caso contrario
        """
        try:
            for i, paciente in enumerate(self.__pacientes):
                if paciente.get_nro_paciente() == nro_paciente:
                    nombre = paciente.get_nombre()
                    apellido = paciente.get_apellido()
                    self.__pacientes.pop(i)
                    print(f"[OK] Paciente {nombre} {apellido} dado de baja exitosamente")
                    return True
            
            print(f"[ERROR] No se encontró paciente con ID {nro_paciente}")
            return False
        
        except Exception as e:
            print(f"[ERROR] Error al dar de baja paciente: {str(e)}")
            return False
    
    # ========== MODIFICACIÓN (UPDATE) ==========
    def modificar_paciente(self, nro_paciente: int, nombre: Optional[str] = None,
                          apellido: Optional[str] = None, telefono: Optional[str] = None,
                          direccion: Optional[str] = None) -> bool:
        """
        Modifica los datos de un paciente
        
        Args:
            nro_paciente: Número de paciente a modificar
            nombre: Nuevo nombre (opcional)
            apellido: Nuevo apellido (opcional)
            telefono: Nuevo teléfono (opcional)
            direccion: Nueva dirección (opcional)
        
        Returns:
            True si se modificó, False en caso contrario
        """
        try:
            paciente = self._buscar_por_id(nro_paciente)
            
            if not paciente:
                print(f"[ERROR] No se encontró paciente con ID {nro_paciente}")
                return False
            
            # Actualizar solo los campos proporcionados
            if nombre:
                paciente.set_nombre(nombre)
            if apellido:
                paciente.set_apellido(apellido)
            if telefono:
                paciente.set_telefono(telefono)
            if direccion:
                paciente.set_direccion(direccion)
            
            print(f"[OK] Paciente ID {nro_paciente} modificado exitosamente")
            return True
        
        except Exception as e:
            print(f"[ERROR] Error al modificar paciente: {str(e)}")
            return False
    
    # ========== CONSULTA (READ) ==========
    def consultar_paciente(self, nro_paciente: int) -> Optional[Paciente]:
        """
        Consulta un paciente por ID
        
        Args:
            nro_paciente: Número de paciente
        
        Returns:
            Paciente encontrado o None
        """
        paciente = self._buscar_por_id(nro_paciente)
        if paciente:
            self._mostrar_paciente(paciente)
            return paciente
        else:
            print(f"[ERROR] No se encontró paciente con ID {nro_paciente}")
            return None
    
    def consultar_por_nombre(self, nombre: str) -> List[Paciente]:
        """
        Consulta pacientes por nombre (búsqueda parcial)
        
        Args:
            nombre: Nombre a buscar
        
        Returns:
            Lista de pacientes encontrados
        """
        resultados = [p for p in self.__pacientes 
                     if nombre.lower() in p.get_nombre().lower()]
        
        if resultados:
            print(f"\n[OK] Se encontraron {len(resultados)} paciente(s):")
            for paciente in resultados:
                self._mostrar_paciente(paciente)
        else:
            print(f"[ERROR] No se encontraron pacientes con el nombre '{nombre}'")
        
        return resultados
    
    def listar_todos_pacientes(self) -> List[Paciente]:
        """
        Lista todos los pacientes del sistema
        
        Returns:
            Lista de todos los pacientes
        """
        if not self.__pacientes:
            print("[INFO] No hay pacientes registrados")
            return []
        
        print(f"\n[INFO] Total de pacientes: {len(self.__pacientes)}\n")
        for paciente in self.__pacientes:
            self._mostrar_paciente(paciente)
        
        return self.__pacientes.copy()
    
    # ========== MÉTODOS AUXILIARES ==========
    def _buscar_por_id(self, nro_paciente: int) -> Optional[Paciente]:
        """Busca un paciente por ID"""
        for paciente in self.__pacientes:
            if paciente.get_nro_paciente() == nro_paciente:
                return paciente
        return None
    
    def _mostrar_paciente(self, paciente: Paciente) -> None:
        """Muestra los datos de un paciente formateados"""
        print(f"   ID: {paciente.get_nro_paciente()}")
        print(f"   Nombre: {paciente.get_nombre()} {paciente.get_apellido()}")
        print(f"   Teléfono: {paciente.get_telefono()}")
        print(f"   Fecha de nacimiento: {paciente.get_fecha_nacimiento()}")
        print(f"   Dirección: {paciente.get_direccion()}")
        if paciente.get_medico():
            print(f"   Médico asignado: {paciente.get_medico()}")
        print()
    
    def get_pacientes(self) -> List[Paciente]:
        """Retorna la lista de pacientes"""
        return self.__pacientes.copy()
    
    def __repr__(self) -> str:
        return f"GestorPaciente(Total pacientes: {len(self.__pacientes)})"