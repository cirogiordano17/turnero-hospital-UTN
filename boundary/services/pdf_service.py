"""Boundary (Servicio externo) — Generación de PDF de recetas médicas."""
from __future__ import annotations
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ASSETS = os.path.join(_BASE, "frontend", "assets")


class PDFService:
    """
    Genera el PDF de una receta médica a partir de los datos provistos.

    Separar la generación de PDF del GestorReceta permite:
    - Cambiar la librería (ReportLab → WeasyPrint) sin tocar lógica de negocio.
    - Testear GestorReceta sin generar archivos físicos.

    Rol ECB: Boundary (Servicio externo).
    """

    def generar_receta(self, cabecera: dict, detalles: list[dict],
                       output_path: str) -> bool:
        """
        Genera el PDF de una receta.

        Args:
            cabecera: dict con claves: id_receta, fecha_emision, p_nom, p_ape,
                      id_paciente, m_nom, m_ape, matricula, fecha, hora_inicio,
                      hora_fin, consultorio, diag.
            detalles: lista de dicts con claves: cantidad, dosis, indicaciones,
                      nombre, presentacion.
            output_path: ruta completa del archivo PDF a generar.

        Returns:
            True si el PDF se generó correctamente.
        """
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas as rl_canvas
            from reportlab.lib.units import cm
            from reportlab.lib import colors
        except ImportError:
            logger.error("ReportLab no instalado: pip install reportlab")
            return False

        try:
            c = rl_canvas.Canvas(output_path, pagesize=A4)
            w, h = A4
            y = h - 2 * cm

            logo_path = os.path.join(_ASSETS, "logo.png")
            firma_path = os.path.join(_ASSETS, "firma.png")

            # Encabezado
            if os.path.exists(logo_path):
                try:
                    c.drawImage(logo_path, 2*cm, y-1.5*cm, width=3*cm, height=1.5*cm,
                                preserveAspectRatio=True, mask="auto")
                except Exception:
                    pass

            c.setFont("Helvetica-Bold", 14)
            c.drawString(6*cm, y, "RECETA MÉDICA")
            c.setFont("Helvetica", 10)
            c.drawRightString(w-2*cm, y, f"Nº Receta: {cabecera['id_receta']}")
            y -= 0.6*cm
            c.drawRightString(w-2*cm, y, f"Fecha: {cabecera['fecha_emision']}")
            y -= 1.0*cm

            # Caja datos paciente/médico
            c.rect(2*cm, y-2.3*cm, w-4*cm, 2.3*cm, stroke=1, fill=0)
            c.setFont("Helvetica-Bold", 11)
            c.drawString(2.2*cm, y-0.5*cm, "Paciente:")
            c.setFont("Helvetica", 11)
            c.drawString(4.2*cm, y-0.5*cm,
                         f"{cabecera['p_nom']} {cabecera['p_ape']}  (ID: {cabecera['id_paciente']})")
            c.setFont("Helvetica-Bold", 11)
            c.drawString(2.2*cm, y-1.2*cm, "Médico:")
            c.setFont("Helvetica", 11)
            c.drawString(4.2*cm, y-1.2*cm,
                         f"Dr/a. {cabecera['m_nom']} {cabecera['m_ape']}  Mat: {cabecera['matricula']}")
            c.setFont("Helvetica", 10)
            c.drawString(2.2*cm, y-1.9*cm,
                         f"Turno: {cabecera['fecha']} | {cabecera['hora_inicio']} - "
                         f"{cabecera['hora_fin']} | Consultorio {cabecera['consultorio']}")
            y -= 2.8*cm

            # Prescripción
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2*cm, y, "Prescripción")
            y -= 0.4*cm
            c.line(2*cm, y, w-2*cm, y)
            y -= 0.4*cm

            col_x = [2*cm, 3.5*cm, 10.5*cm, 15.5*cm]
            c.setFont("Helvetica-Bold", 10)
            for txt, cx in zip(["Cant", "Monodroga", "Presentación", "Dosis/día"], col_x):
                c.drawString(cx, y, txt)
            y -= 0.35*cm
            c.line(2*cm, y, w-2*cm, y)
            y -= 0.3*cm

            c.setFont("Helvetica", 10)
            for item in (detalles or []):
                if y < 4*cm:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y = h - 2*cm
                c.drawString(col_x[0], y, str(item.get("cantidad", "")))
                c.drawString(col_x[1], y, item.get("nombre", ""))
                c.drawString(col_x[2], y, item.get("presentacion", ""))
                c.drawString(col_x[3], y, item.get("dosis", ""))
                y -= 0.45*cm
                if item.get("indicaciones"):
                    c.setFont("Helvetica-Oblique", 9)
                    c.drawString(col_x[1], y, f"Indicaciones: {item['indicaciones']}")
                    c.setFont("Helvetica", 10)
                    y -= 0.4*cm

            y -= 0.2*cm
            c.line(2*cm, y, w-2*cm, y)
            y -= 0.6*cm

            # Diagnóstico
            c.setFont("Helvetica-Bold", 11)
            c.drawString(2*cm, y, "Diagnóstico:")
            y -= 0.5*cm
            box_h = 2.2*cm
            box_y = y - box_h
            c.rect(2*cm, box_y, w-4*cm, box_h, stroke=1, fill=0)
            diag = (cabecera.get("diag") or "").strip()
            if diag:
                self._wrap_text(c, diag, 2.2*cm, box_y + box_h - 0.7*cm, w - 4.4*cm)
            y = box_y - 0.6*cm

            # QR + Firma
            if y < 6*cm:
                c.showPage()
                y = h - 2*cm
            self._bloque_qr_firma(c, cabecera, firma_path, y, w)

            c.showPage()
            c.save()
            return True

        except Exception as exc:
            logger.error("Error al generar PDF de receta %s: %s", cabecera.get("id_receta"), exc)
            return False

    # -- Helpers privados --

    @staticmethod
    def _wrap_text(c, text: str, x: float, y: float, max_w: float) -> None:
        from reportlab.pdfbase.pdfmetrics import stringWidth
        c.setFont("Helvetica", 10)
        line = ""
        for word in text.split():
            test = (line + " " + word).strip()
            if stringWidth(test, "Helvetica", 10) <= max_w:
                line = test
            else:
                c.drawString(x, y, line)
                y -= 0.45*cm
                line = word
        if line:
            c.drawString(x, y, line)

    @staticmethod
    def _bloque_qr_firma(c, cab: dict, firma_path: str,
                          block_top: float, w: float) -> None:
        from reportlab.lib.units import cm
        size = 3.2*cm
        try:
            from reportlab.graphics.shapes import Drawing
            from reportlab.graphics import renderPDF
            from reportlab.graphics.barcode import qr as qrbar
            qr_text = f"RECETA:{cab['id_receta']}|PAC:{cab['p_nom']} {cab['p_ape']}|F:{cab['fecha_emision']}"
            qr = qrbar.QrCodeWidget(qr_text)
            bounds = qr.getBounds()
            d = Drawing(size, size,
                        transform=[size/(bounds[2]-bounds[0]), 0, 0,
                                   size/(bounds[3]-bounds[1]), 0, 0])
            d.add(qr)
            renderPDF.draw(d, c, 2*cm, block_top - size)
        except Exception:
            pass

        sig_w, sig_h = 5*cm, 2*cm
        sig_x = w - 2*cm - sig_w
        sig_y = block_top - 1.6*cm
        if os.path.exists(firma_path):
            try:
                c.drawImage(firma_path, sig_x, sig_y, width=sig_w, height=sig_h,
                            preserveAspectRatio=True, mask="auto")
            except Exception:
                c.line(sig_x, sig_y + 0.2*cm, sig_x + sig_w, sig_y + 0.2*cm)
        else:
            c.line(sig_x, sig_y + 0.2*cm, sig_x + sig_w, sig_y + 0.2*cm)
        c.setFont("Helvetica", 10)
        c.drawCentredString(sig_x + sig_w/2, sig_y - 0.4*cm,
                            f"Dr/a. {cab['m_nom']} {cab['m_ape']}  -  Mat. {cab['matricula']}")
