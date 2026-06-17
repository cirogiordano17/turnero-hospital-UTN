from enum import Enum


class EstadoNotificacionEnum(Enum):
    """Enumeración para estados de notificaciones"""
    ENVIADO = "enviado"
    PENDIENTE = "pendiente"
    ERROR = "error"


class TipoLaboratorioEnum(Enum):
    """Enumeración para tipos de laboratorio"""
    ANALISIS = "analisis"
    IMAGENES = "imagenes"