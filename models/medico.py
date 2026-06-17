from datetime import date
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from especialidad import Especialidad
    from paciente import Paciente
    from turno import Turno


class Medico:
    """Clase que representa un médico del sistema"""
    
    def __init__(self, matricula: int, nombre: str, apellido: str, 
                 telefono: str, email: str, fecha_alta: date, 
                 fecha_baja: Optional[date] = None):
        self.__matricula = matricula
        self.__nombre = nombre
        self.__apellido = apellido
        self.__telefono = telefono
        self.__email = email
        self.__fechaDeAlta = fecha_alta
        self.__fechaDeBaja = fecha_baja
        self.__especialidades: List['Especialidad'] = []
        self.__pacientes: List['Paciente'] = []
        self.__turnos: List['Turno'] = []
    
    # Getters
    def get_matricula(self) -> int:
        """Obtiene la matrícula del médico"""
        return self.__matricula
    
    def get_nombre(self) -> str:
        """Obtiene el nombre del médico"""
        return self.__nombre
    
    def get_apellido(self) -> str:
        """Obtiene el apellido del médico"""
        return self.__apellido
    
    def get_telefono(self) -> str:
        """Obtiene el teléfono del médico"""
        return self.__telefono
    
    def get_email(self) -> str:
        """Obtiene el email del médico"""
        return self.__email
    
    def get_fecha_alta(self) -> date:
        """Obtiene la fecha de alta"""
        return self.__fechaDeAlta
    
    def get_fecha_baja(self) -> Optional[date]:
        """Obtiene la fecha de baja"""
        return self.__fechaDeBaja
    
    def get_especialidades(self) -> List['Especialidad']:
        """Obtiene la lista de especialidades"""
        return self.__especialidades.copy()
    
    def get_pacientes(self) -> List['Paciente']:
        """Obtiene la lista de pacientes"""
        return self.__pacientes.copy()
    
    def get_turnos(self) -> List['Turno']:
        """Obtiene la lista de turnos"""
        return self.__turnos.copy()
    
    # Setters
    def set_nombre(self, nombre: str) -> None:
        """Modifica el nombre del médico"""
        if nombre and len(nombre) > 0:
            self.__nombre = nombre
        else:
            raise ValueError("El nombre no puede estar vacío")
    
    def set_apellido(self, apellido: str) -> None:
        """Modifica el apellido del médico"""
        if apellido and len(apellido) > 0:
            self.__apellido = apellido
        else:
            raise ValueError("El apellido no puede estar vacío")
    
    def set_telefono(self, telefono: str) -> None:
        """Modifica el teléfono del médico"""
        if telefono and len(telefono) > 0:
            self.__telefono = telefono
        else:
            raise ValueError("El teléfono no puede estar vacío")
    
    def set_email(self, email: str) -> None:
        """Modifica el email del médico"""
        if "@" in email:
            self.__email = email
        else:
            raise ValueError("El email no es válido")
    
    def set_fecha_baja(self, fecha_baja: Optional[date]) -> None:
        """Modifica la fecha de baja"""
        self.__fechaDeBaja = fecha_baja
    
    # Métodos de negocio
    def asignar_especialidad(self, especialidad: 'Especialidad') -> None:
        """Asigna una especialidad al médico"""
        if especialidad not in self.__especialidades:
            self.__especialidades.append(especialidad)
            especialidad.asociar_medico(self)
    
    def agregar_paciente(self, paciente: 'Paciente') -> None:
        """Agrega un paciente a la lista del médico"""
        if paciente not in self.__pacientes:
            self.__pacientes.append(paciente)
            paciente.set_medico(self)
    
    def agregar_turno(self, turno: 'Turno') -> None:
        """Agrega un turno a la lista del médico"""
        if turno not in self.__turnos:
            self.__turnos.append(turno)
    
    def listar_turnos(self) -> List['Turno']:
        """Retorna la lista de turnos del médico"""
        return self.__turnos.copy()
    
    def __repr__(self) -> str:
        return f"Medico({self.__nombre} {self.__apellido}, Mat: {self.__matricula})"