"""Boundary (Persistencia) — DAO de Turno. Centraliza todas las queries SQL de Turno."""
from __future__ import annotations
from datetime import date
from typing import Optional
from boundary.persistence.database import Database


class TurnoDAO:
    """
    Data Access Object para la tabla Turno.

    Centraliza todas las queries SQL relacionadas con turnos.
    El Control (GestorTurno) usa este DAO sin conocer detalles de SQL.

    Rol ECB: Boundary (Persistencia).
    """

    _QUERY_BASE = """
        SELECT t.id_turno,
               t.matricula, t.id_paciente, t.id_consultorio, t.id_agenda,
               t.id_especialidad, t.fecha, t.hora_inicio, t.hora_fin,
               t.estado, t.observaciones,
               CONCAT(p.nombre, ' ', p.apellido) AS paciente,
               CONCAT(m.nombre, ' ', m.apellido) AS medico,
               c.numero AS consultorio,
               e.nombre AS especialidad
        FROM Turno t
        JOIN Medico m ON t.matricula = m.matricula
        LEFT JOIN Paciente p ON t.id_paciente = p.id_paciente
        JOIN Consultorio c ON t.id_consultorio = c.id_consultorio
        LEFT JOIN Especialidad e ON t.id_especialidad = e.id_especialidad
    """

    def __init__(self, db: Database) -> None:
        self._db = db

    def buscar_por_id(self, id_turno: int) -> Optional[dict]:
        with self._db:
            return self._db.obtener_registro(
                self._QUERY_BASE + " WHERE t.id_turno = %s", (id_turno,)
            )

    def listar_libres_por_medico(self, matricula: int) -> list[dict]:
        """Turnos Libre, fecha >= hoy, ordenados por fecha y hora."""
        with self._db:
            return self._db.obtener_registros(
                self._QUERY_BASE +
                " WHERE t.matricula = %s AND t.estado = 'Libre' AND t.fecha >= CURDATE()"
                " ORDER BY t.fecha, t.hora_inicio LIMIT 50",
                (matricula,),
            )

    def listar_por_filtros(self, filtro_fecha: str, filtro_estado: str) -> list[dict]:
        """
        Retorna turnos con paciente asignado, combinando filtros de fecha y estado.

        filtro_fecha: 'hoy' | 'proximos' | 'todos'
        filtro_estado: 'programados' | 'atendidos' | 'cancelados' | 'inasistencia' | 'todos_estados'
        """
        condiciones = ["t.id_paciente IS NOT NULL"]
        params: list = []

        hoy = date.today()
        if filtro_fecha == "hoy":
            condiciones.append("t.fecha = %s")
            params.append(hoy)
        elif filtro_fecha == "proximos":
            condiciones.append("t.fecha > %s")
            params.append(hoy)

        estados_map = {
            "programados": "Programado",
            "atendidos": "Atendido",
            "cancelados": "Cancelado",
            "inasistencia": "Inasistencia",
        }
        if filtro_estado in estados_map:
            condiciones.append("t.estado = %s")
            params.append(estados_map[filtro_estado])
        else:
            condiciones.append("t.estado IN ('Programado','Atendido','Cancelado','Inasistencia')")

        where = " WHERE " + " AND ".join(condiciones)
        order = " ORDER BY t.fecha DESC, t.hora_inicio DESC LIMIT 100"

        with self._db:
            return self._db.obtener_registros(
                self._QUERY_BASE + where + order, tuple(params)
            )

    def listar_por_paciente(self, id_paciente: int) -> list[dict]:
        with self._db:
            return self._db.obtener_registros(
                self._QUERY_BASE + " WHERE t.id_paciente = %s ORDER BY t.fecha DESC, t.hora_inicio DESC",
                (id_paciente,),
            )

    def programar(self, id_turno: int, id_paciente: int,
                  id_especialidad: Optional[int], observaciones: str) -> bool:
        """Asigna paciente al turno y lo pasa a estado Programado."""
        with self._db:
            if id_especialidad is not None:
                filas = self._db.ejecutar_consulta(
                    "UPDATE Turno SET id_paciente = %s, id_especialidad = %s,"
                    " estado = 'Programado', observaciones = %s"
                    " WHERE id_turno = %s AND estado = 'Libre'",
                    (id_paciente, id_especialidad, observaciones, id_turno),
                )
            else:
                filas = self._db.ejecutar_consulta(
                    "UPDATE Turno SET id_paciente = %s, estado = 'Programado',"
                    " observaciones = %s WHERE id_turno = %s AND estado = 'Libre'",
                    (id_paciente, observaciones, id_turno),
                )
            return bool(filas and filas > 0)

    def cambiar_estado(self, id_turno: int, nuevo_estado: str) -> bool:
        with self._db:
            filas = self._db.ejecutar_consulta(
                "UPDATE Turno SET estado = %s WHERE id_turno = %s",
                (nuevo_estado, id_turno),
            )
            return bool(filas and filas > 0)

    def marcar_inasistencias_vencidas(self) -> int:
        """
        Marca como Inasistencia todos los turnos Programados cuya fecha ya pasó.
        Retorna la cantidad de filas afectadas.
        """
        with self._db:
            filas = self._db.ejecutar_consulta(
                "UPDATE Turno SET estado = 'Inasistencia'"
                " WHERE estado = 'Programado' AND fecha < CURDATE()",
            )
            return filas or 0

    def insertar_turno_libre(self, matricula: int, id_consultorio: int,
                              id_agenda: int, fecha: date,
                              hora_inicio, hora_fin) -> Optional[int]:
        """Inserta un slot Libre. Retorna el id_turno generado."""
        with self._db:
            filas = self._db.ejecutar_consulta(
                "INSERT INTO Turno (matricula, id_consultorio, id_agenda, fecha,"
                " hora_inicio, hora_fin, estado)"
                " VALUES (%s, %s, %s, %s, %s, %s, 'Libre')",
                (matricula, id_consultorio, id_agenda, fecha, hora_inicio, hora_fin),
            )
            return self._db.get_last_insert_id() if filas else None

    def listar_especialidades(self) -> list[dict]:
        """Retorna id y nombre de todas las especialidades (para dropdowns)."""
        with self._db:
            return self._db.obtener_registros(
                "SELECT id_especialidad, nombre FROM Especialidad ORDER BY nombre"
            )

    def listar_medicos_por_especialidad(self, id_especialidad: int) -> list[dict]:
        """Retorna médicos activos que atienden la especialidad dada."""
        with self._db:
            return self._db.obtener_registros(
                """SELECT m.matricula,
                          CONCAT(m.nombre, ' ', m.apellido) AS nombre_completo,
                          GROUP_CONCAT(e.nombre ORDER BY e.nombre SEPARATOR ', ') AS especialidades
                   FROM Medico m
                   JOIN Medico_Especialidad me ON m.matricula = me.matricula
                   JOIN Especialidad e ON me.id_especialidad = e.id_especialidad
                   WHERE me.id_especialidad = %s AND m.activo = 1
                   GROUP BY m.matricula, m.nombre, m.apellido
                   ORDER BY m.nombre""",
                (id_especialidad,),
            )
