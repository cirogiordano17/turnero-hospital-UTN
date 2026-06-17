import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import sys, os
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)
from frontend.widgets.scrollable_frame import ScrollableFrame


class CrearPacienteDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.window = tk.Toplevel(parent)
        self.window.title("Crear Nuevo Paciente")
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        w, h = min(500, int(sw * 0.9)), min(480, int(sh * 0.85))
        self.window.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.window.resizable(True, True)
        self.window.minsize(420, 350)

        container = ttk.Frame(self.window)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(container, text="Registrar Nuevo Paciente", font=("Arial", 14, "bold")).pack(pady=(0, 10))

        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", side="bottom", pady=(10, 0))
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="✓ Crear", command=self._crear_paciente).pack(side="right", padx=5)

        scroll = ScrollableFrame(container)
        scroll.pack(fill="both", expand=True)
        form_frame = scroll.inner
        
        # ID Paciente
        ttk.Label(form_frame, text="ID Paciente:").grid(row=0, column=0, sticky="w", pady=8)
        self.entry_id = ttk.Entry(form_frame, width=30)
        self.entry_id.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=8)
        self.entry_nombre = ttk.Entry(form_frame, width=30)
        self.entry_nombre.grid(row=1, column=1, sticky="ew", padx=(10, 0))
        
        # Apellido
        ttk.Label(form_frame, text="Apellido:").grid(row=2, column=0, sticky="w", pady=8)
        self.entry_apellido = ttk.Entry(form_frame, width=30)
        self.entry_apellido.grid(row=2, column=1, sticky="ew", padx=(10, 0))
        
        # Teléfono
        ttk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="w", pady=8)
        self.entry_telefono = ttk.Entry(form_frame, width=30)
        self.entry_telefono.grid(row=3, column=1, sticky="ew", padx=(10, 0))
        
        # Fecha de Nacimiento
        ttk.Label(form_frame, text="Fecha Nacimiento (YYYY-MM-DD):").grid(row=4, column=0, sticky="w", pady=8)
        self.entry_nacimiento = ttk.Entry(form_frame, width=30)
        self.entry_nacimiento.grid(row=4, column=1, sticky="ew", padx=(10, 0))
        
        # Dirección
        ttk.Label(form_frame, text="Dirección:").grid(row=5, column=0, sticky="nw", pady=8)
        self.text_direccion = tk.Text(form_frame, height=3, width=30)
        self.text_direccion.grid(row=5, column=1, sticky="ew", padx=(10, 0))
        
        form_frame.columnconfigure(1, weight=1)
    
    def _crear_paciente(self):
        """Valida y crea el paciente"""
        id_paciente = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        telefono = self.entry_telefono.get().strip()
        nacimiento = self.entry_nacimiento.get().strip()
        direccion = self.text_direccion.get("1.0", tk.END).strip()
        
        # Validaciones
        if not id_paciente:
            messagebox.showwarning("Advertencia", "El ID del paciente es obligatorio")
            return
        
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return
        
        if not apellido:
            messagebox.showwarning("Advertencia", "El apellido es obligatorio")
            return
        
        if not nacimiento:
            messagebox.showwarning("Advertencia", "La fecha de nacimiento es obligatoria")
            return
        
        if not direccion:
            messagebox.showwarning("Advertencia", "La dirección es obligatoria")
            return
        
        # Crear paciente
        ok, msg = self.controller.crear(
            id_paciente,
            nombre,
            apellido,
            telefono,
            nacimiento,
            direccion
        )
        
        if ok:
            messagebox.showinfo("Éxito", "✓ Paciente creado exitosamente")
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg)
