"""Control — Casos de uso de recetas médicas."""
from __future__ import annotations
from datetime import date
from typing import Optional

from boundary.persistence.receta_dao import RecetaDAO
from boundary.services.pdf_service import PDFService
from entities.exceptions import EntidadNoEncontradaError


class GestorReceta:
    """
    Orquesta la creación de historiales clínicos, recetas y generación de PDFs.

    Rol ECB: Control.
    """

    def __init__(self, receta_dao: RecetaDAO, pdf_service: PDFService) -> None:
        self._receta_dao = receta_dao
        self._pdf_service = pdf_service

    def registrar_atencion(self, id_turno: int, id_paciente: int,
                           diagnostico: str, tratamiento: str,
                           notas: str, observaciones: str) -> int:
        """
        Crea el historial clínico de un turno atendido.

        Returns:
            id_historial creado.

        Raises:
            RuntimeError: si falla la inserción.
        """
        id_historial = self._receta_dao.insertar_historial(
            id_turno, id_paciente, diagnostico, tratamiento, notas, observaciones
        )
        if not id_historial:
            raise RuntimeError("No se pudo crear el historial clínico")
        return id_historial

    def crear_receta(self, id_historial: int,
                     observaciones: str = "") -> int:
        """
        Crea una receta asociada a un historial clínico.

        Returns:
            id_receta creado.
        """
        id_receta = self._receta_dao.insertar(
            id_historial, date.today(), observaciones
        )
        if not id_receta:
            raise RuntimeError("No se pudo crear la receta")
        return id_receta

    def agregar_medicamento(self, id_receta: int, id_medicamento: int,
                             cantidad: int, dosis: str,
                             indicaciones: str = "") -> bool:
        return self._receta_dao.insertar_detalle(
            id_receta, id_medicamento, cantidad, dosis, indicaciones
        )

    def obtener_id_receta_de_turno(self, id_turno: int) -> Optional[int]:
        row = self._receta_dao.buscar_por_turno(id_turno)
        return row["id_receta"] if row else None

    def generar_pdf(self, id_receta: int, output_path: str) -> bool:
        """
        Genera el PDF de una receta.

        Raises:
            EntidadNoEncontradaError: si la receta no existe.
        """
        cabecera = self._receta_dao.buscar_por_id(id_receta)
        if not cabecera:
            raise EntidadNoEncontradaError(f"Receta #{id_receta} no encontrada")
        detalles = self._receta_dao.obtener_detalles(id_receta)
        return self._pdf_service.generar_receta(cabecera, detalles, output_path)
