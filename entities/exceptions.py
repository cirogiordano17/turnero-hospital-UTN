"""
Excepciones de dominio del sistema de turnos.

Usar excepciones tipadas en lugar de booleanos permite que el Control
comunique el motivo exacto del error al Boundary sin mezclar lógica
de presentación con lógica de negocio.
"""


class EntidadNoEncontradaError(Exception):
    """Se lanza cuando una entidad buscada no existe en el sistema."""


class EstadoInvalidoError(Exception):
    """Se lanza al intentar una transición de estado no permitida."""


class DuplicadoError(Exception):
    """Se lanza al intentar registrar una entidad que ya existe."""


class ValidacionError(Exception):
    """Se lanza cuando los datos de entrada no cumplen las reglas de negocio."""
