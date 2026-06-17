from typing import List, Optional
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.especialidad import Especialidad


class GestorEspecialidad:
    """Clase gestora de operaciones ABMC de especialidades"""
    
    def __init__(self):
        self.__especialidades: List[Especialidad] = []
    
    # ========== ALTA (CREATE) ==========
    def alta_especialidad(self, nro_especialidad: int, nombre: str, 
                         descripcion: str) -> Optional[Especialidad]:
        """
        Da de alta una nueva especialidad en el sistema
        
        Args:
            nro_especialidad: Número de especialidad
            nombre: Nombre de la especialidad
            descripcion: Descripción de la especialidad
        
        Returns:
            Especialidad creada o None si hay error
        """
        try:
            if not nombre or not descripcion:
                print("[ERROR] El nombre y descripción son obligatorios")
                return None
            
            # Verificar que no exista una especialidad con el mismo número
            if self._buscar_por_numero(nro_especialidad):
                print(f"[ERROR] Ya existe una especialidad con el número {nro_especialidad}")
                return None
            
            # Verificar que no exista una especialidad con el mismo nombre
            for esp in self.__especialidades:
                if esp.get_nombre().lower() == nombre.lower():
                    print(f"[ERROR] Ya existe una especialidad con el nombre {nombre}")
                    return None
            
            # Crear nueva especialidad
            nueva_especialidad = Especialidad(
                nro_especialidad,
                nombre,
                descripcion
            )
            
            self.__especialidades.append(nueva_especialidad)
            
            print(f"[OK] Especialidad {nombre} dada de alta exitosamente (ID: {nro_especialidad})")
            return nueva_especialidad
        
        except Exception as e:
            print(f"[ERROR] Error al dar de alta especialidad: {str(e)}")
            return None
    
    # ========== BAJA (DELETE) ==========
    def baja_especialidad(self, nro_especialidad: int) -> bool:
        """
        Da de baja una especialidad del sistema
        
        Args:
            nro_especialidad: Número de especialidad a dar de baja
        
        Returns:
            True si se eliminó, False en caso contrario
        """
        try:
            for i, especialidad in enumerate(self.__especialidades):
                if especialidad.get_nro_especialidad() == nro_especialidad:
                    nombre = especialidad.get_nombre()
                    self.__especialidades.pop(i)
                    print(f"[OK] Especialidad {nombre} dada de baja exitosamente")
                    return True
            
            print(f"[ERROR] No se encontró especialidad con ID {nro_especialidad}")
            return False
        
        except Exception as e:
            print(f"[ERROR] Error al dar de baja especialidad: {str(e)}")
            return False
    
    # ========== MODIFICACIÓN (UPDATE) ==========
    def modificar_especialidad(self, nro_especialidad: int, nombre: Optional[str] = None,
                              descripcion: Optional[str] = None) -> bool:
        """
        Modifica los datos de una especialidad
        
        Args:
            nro_especialidad: Número de especialidad a modificar
            nombre: Nuevo nombre (opcional)
            descripcion: Nueva descripción (opcional)
        
        Returns:
            True si se modificó, False en caso contrario
        """
        try:
            especialidad = self._buscar_por_numero(nro_especialidad)
            
            if not especialidad:
                print(f"[ERROR] No se encontró especialidad con ID {nro_especialidad}")
                return False
            
            # Actualizar solo los campos proporcionados
            if nombre:
                # Verificar que no exista otra especialidad con el mismo nombre
                for esp in self.__especialidades:
                    if (esp.get_nombre().lower() == nombre.lower() and 
                        esp.get_nro_especialidad() != nro_especialidad):
                        print(f"[ERROR] Ya existe otra especialidad con el nombre {nombre}")
                        return False
                especialidad.set_nombre(nombre)
            
            if descripcion:
                especialidad.set_descripcion(descripcion)
            
            print(f"[OK] Especialidad ID {nro_especialidad} modificada exitosamente")
            return True
        
        except Exception as e:
            print(f"[ERROR] Error al modificar especialidad: {str(e)}")
            return False
    
    # ========== CONSULTA (READ) ==========
    def consultar_especialidad(self, nro_especialidad: int) -> Optional[Especialidad]:
        """
        Consulta una especialidad por ID
        
        Args:
            nro_especialidad: Número de especialidad
        
        Returns:
            Especialidad encontrada o None
        """
        especialidad = self._buscar_por_numero(nro_especialidad)
        if especialidad:
            self._mostrar_especialidad(especialidad)
            return especialidad
        else:
            print(f"[ERROR] No se encontró especialidad con ID {nro_especialidad}")
            return None
    
    def consultar_por_nombre(self, nombre: str) -> List[Especialidad]:
        """
        Consulta especialidades por nombre (búsqueda parcial)
        
        Args:
            nombre: Nombre a buscar
        
        Returns:
            Lista de especialidades encontradas
        """
        resultados = [e for e in self.__especialidades 
                     if nombre.lower() in e.get_nombre().lower()]
        
        if resultados:
            print(f"\n[OK] Se encontraron {len(resultados)} especialidad(es):")
            for especialidad in resultados:
                self._mostrar_especialidad(especialidad)
        else:
            print(f"[ERROR] No se encontraron especialidades con el nombre '{nombre}'")
        
        return resultados
    
    def listar_todas_especialidades(self) -> List[Especialidad]:
        """
        Lista todas las especialidades del sistema
        
        Returns:
            Lista de todas las especialidades
        """
        if not self.__especialidades:
            print("[INFO] No hay especialidades registradas")
            return []
        
        print(f"\n[INFO] Total de especialidades: {len(self.__especialidades)}\n")
        for especialidad in self.__especialidades:
            self._mostrar_especialidad(especialidad)
        
        return self.__especialidades.copy()
    
    # ========== MÉTODOS AUXILIARES ==========
    def _buscar_por_numero(self, nro_especialidad: int) -> Optional[Especialidad]:
        """Busca una especialidad por número"""
        for especialidad in self.__especialidades:
            if especialidad.get_nro_especialidad() == nro_especialidad:
                return especialidad
        return None
    
    def _mostrar_especialidad(self, especialidad: Especialidad) -> None:
        """Muestra los datos de una especialidad formateados"""
        print(f"   ID: {especialidad.get_nro_especialidad()}")
        print(f"   Nombre: {especialidad.get_nombre()}")
        print(f"   Descripción: {especialidad.get_descripcion()}")
        medicos = especialidad.get_medicos()
        if medicos:
            print(f"   Médicos: {len(medicos)}")
        print()
    
    def get_especialidades(self) -> List[Especialidad]:
        """Retorna la lista de especialidades"""
        return self.__especialidades.copy()
    
    def __repr__(self) -> str:
        return f"GestorEspecialidad(Total especialidades: {len(self.__especialidades)})"
