"""Boundary (Persistencia) — DAO de Receta."""
from __future__ import annotations
from datetime import date
from typing import Optional
from boundary.persistence.database import Database


class RecetaDAO:
    """Rol ECB: Boundary (Persistencia)."""

    def __init__(self, db: Database) -> None:
        self._db = db

    def buscar_por_turno(self, id_turno: int) -> Optional[dict]:
        with self._db:
            return self._db.obtener_registro(
                """SELECT r.id_receta, r.id_historial, r.fecha_emision, r.observaciones
                   FROM Receta r
                   JOIN Historial_clinico h ON h.id_historial = r.id_historial
                   WHERE h.id_turno = %s
                   ORDER BY r.id_receta DESC LIMIT 1""",
                (id_turno,),
            )

    def buscar_por_id(self, id_receta: int) -> Optional[dict]:
        """Retorna cabecera de receta con datos de turno, paciente y médico."""
        with self._db:
            return self._db.obtener_registro(
                """SELECT r.id_receta, r.fecha_emision, r.observaciones,
                          p.nombre AS p_nom, p.apellido AS p_ape, p.id_paciente,
                          m.nombre AS m_nom, m.apellido AS m_ape, m.matricula,
                          t.fecha, t.hora_inicio, t.hora_fin,
                          c.numero AS consultorio,
                          h.diagnostico AS diag
                   FROM Receta r
                   JOIN Historial_clinico h ON h.id_historial = r.id_historial
                   JOIN Turno t ON t.id_turno = h.id_turno
                   JOIN Paciente p ON p.id_paciente = t.id_paciente
                   JOIN Medico m ON m.matricula = t.matricula
                   JOIN Consultorio c ON c.id_consultorio = t.id_consultorio
                   WHERE r.id_receta = %s""",
                (id_receta,),
            )

    def obtener_detalles(self, id_receta: int) -> list[dict]:
        with self._db:
            return self._db.obtener_registros(
                """SELECT d.cantidad, d.dosis, d.indicaciones,
                          med.nombre, med.presentacion
                   FROM Detalle_receta d
                   JOIN Medicamento med ON med.id_medicamento = d.id_medicamento
                   WHERE d.id_receta = %s""",
                (id_receta,),
            )

    def insertar(self, id_historial: int, fecha_emision: date,
                 observaciones: str = "") -> Optional[int]:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "INSERT INTO Receta (id_historial, fecha_emision, observaciones)"
                " VALUES (%s, %s, %s)",
                (id_historial, fecha_emision, observaciones),
            )
            return self._db.get_last_insert_id() if filas else None

    def insertar_detalle(self, id_receta: int, id_medicamento: int,
                         cantidad: int, dosis: str, indicaciones: str = "") -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "INSERT INTO Detalle_receta (id_receta, id_medicamento, cantidad,"
                " dosis, indicaciones) VALUES (%s,%s,%s,%s,%s)",
                (id_receta, id_medicamento, cantidad, dosis, indicaciones),
            )
            return bool(filas and filas > 0)

    def insertar_historial(self, id_turno: int, id_paciente: int,
                           diagnostico: str, tratamiento: str,
                           notas: str, observaciones: str) -> Optional[int]:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "INSERT INTO Historial_clinico (id_turno, id_paciente, diagnostico,"
                " tratamiento, notas, observaciones) VALUES (%s,%s,%s,%s,%s,%s)",
                (id_turno, id_paciente, diagnostico, tratamiento, notas, observaciones),
            )
            return self._db.get_last_insert_id() if filas else None
