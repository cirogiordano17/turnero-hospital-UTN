"""Boundary (UI) — Ventana principal y arranque de la aplicación."""
import tkinter as tk
from tkinter import ttk
from .views.turnos_view import TurnosView
from .views.pacientes_view import PacientesView
from .views.medicos_view import MedicosView
from .views.especialidades_view import EspecialidadesView
from .views.reportes_view import ReportesView
from .styles.theme import setup_theme

from boundary.persistence.database import Database
from boundary.persistence.notificacion_dao import NotificacionDAO
from boundary.persistence.paciente_dao import PacienteDAO
from boundary.services.email_service import EmailService
from control.gestor_notificacion import GestorNotificacion
from control.scheduler_notificaciones import SchedulerNotificaciones


def _build_scheduler(intervalo_minutos: int = 5) -> SchedulerNotificaciones:
    db = Database()
    gestor = GestorNotificacion(
        NotificacionDAO(db),
        PacienteDAO(db),
        EmailService(),
    )
    return SchedulerNotificaciones(gestor, intervalo_minutos)


def run_app() -> None:
    root = tk.Tk()
    root.title("Turnero Médico – Hospital DAO")
    root.geometry("1100x650")

    setup_theme()

    scheduler = _build_scheduler(intervalo_minutos=5)
    scheduler.iniciar()

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    nb.add(TurnosView(nb), text="Turnos")
    nb.add(PacientesView(nb), text="Pacientes")
    nb.add(MedicosView(nb), text="Médicos")
    nb.add(EspecialidadesView(nb), text="Especialidades")
    nb.add(ReportesView(nb), text="Reportes")

    def on_closing() -> None:
        scheduler.detener()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
