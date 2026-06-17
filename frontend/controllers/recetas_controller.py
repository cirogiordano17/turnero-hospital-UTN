"""Boundary (UI) — Adaptador delgado entre la vista de Recetas y GestorReceta."""
from __future__ import annotations
from typing import Optional

from boundary.persistence.database import Database
from boundary.persistence.receta_dao import RecetaDAO
from boundary.services.pdf_service import PDFService
from control.gestor_receta import GestorReceta


def _build_gestor() -> GestorReceta:
    return GestorReceta(RecetaDAO(Database()), PDFService())


class RecetasController:
    """Boundary (UI) — Delega en GestorReceta. Sin lógica de negocio."""

    def __init__(self) -> None:
        self._gestor = _build_gestor()

    def id_receta_de_turno(self, id_turno: int) -> Optional[int]:
        return self._gestor.obtener_id_receta_de_turno(id_turno)

    def generar_pdf(self, id_receta: int, output_path: str) -> bool:
        try:
            return self._gestor.generar_pdf(id_receta, output_path)
        except Exception:
            return False
