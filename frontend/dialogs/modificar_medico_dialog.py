import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)
from frontend.widgets.scrollable_frame import ScrollableFrame


class ModificarMedicoDialog:
    def __init__(self, parent, controller, medico_data):
        self.controller = controller
        self.medico_data = medico_data
        self.window = tk.Toplevel(parent)
        self.window.title("Modificar Médico")
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        w, h = min(600, int(sw * 0.9)), min(560, int(sh * 0.85))
        self.window.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.window.resizable(True, True)
        self.window.minsize(480, 400)

        container = ttk.Frame(self.window, padding=15)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text=f"Modificar Médico: {medico_data['nombre']} {medico_data['apellido']}",
            font=("Arial", 13, "bold")
        ).pack(pady=(0, 10))

        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", side="bottom", pady=(10, 0))
        btn_frame.columnconfigure(0, weight=1)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).grid(row=0, column=1, padx=5, sticky="e")
        ttk.Button(btn_frame, text="✓ Guardar Cambios", command=self._modificar_medico).grid(row=0, column=2, padx=5, sticky="e")

        scroll = ScrollableFrame(container)
        scroll.pack(fill="both", expand=True)
        form_frame = ttk.LabelFrame(scroll.inner, text="Datos del Médico", padding=15)
        form_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Matrícula (NO EDITABLE)
        matric_label_title = ttk.Label(form_frame, text="Matrícula:", font=("Arial", 9, "bold"))
        matric_label_title.grid(row=0, column=0, sticky="w", pady=10, padx=(0, 15))
        
        matric_value_label = ttk.Label(form_frame, text=str(medico_data['matricula']), font=("Arial", 10))
        matric_value_label.grid(row=0, column=1, sticky="w", pady=10, padx=(0, 0))
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:", font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_nombre = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_nombre.insert(0, medico_data['nombre'])
        self.entry_nombre.grid(row=1, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Apellido
        ttk.Label(form_frame, text="Apellido:", font=("Arial", 9)).grid(row=2, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_apellido = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_apellido.insert(0, medico_data['apellido'])
        self.entry_apellido.grid(row=2, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Teléfono
        ttk.Label(form_frame, text="Teléfono:", font=("Arial", 9)).grid(row=3, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_telefono = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_telefono.insert(0, medico_data['telefono'])
        self.entry_telefono.grid(row=3, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Email
        ttk.Label(form_frame, text="Email:", font=("Arial", 9)).grid(row=4, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_email = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_email.insert(0, medico_data['email'])
        self.entry_email.grid(row=4, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        # Fecha de Alta
        ttk.Label(form_frame, text="Fecha Alta (YYYY-MM-DD):", font=("Arial", 9)).grid(row=5, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_fecha_alta = ttk.Entry(form_frame, width=30, font=("Arial", 9))
        self.entry_fecha_alta.insert(0, medico_data['fecha_alta'])
        self.entry_fecha_alta.grid(row=5, column=1, sticky="ew", padx=(0, 0), pady=10)
        
        form_frame.columnconfigure(1, weight=1)
    
    def _modificar_medico(self):
        """Valida y modifica el médico"""
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()
        fecha_alta = self.entry_fecha_alta.get().strip()
        
        # Validaciones
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio")
            return
        
        if not apellido:
            messagebox.showwarning("Advertencia", "El apellido es obligatorio")
            return
        
        if not email:
            messagebox.showwarning("Advertencia", "El email es obligatorio")
            return
        
        if "@" not in email:
            messagebox.showwarning("Advertencia", "El email no es válido")
            return
        
        if not fecha_alta:
            messagebox.showwarning("Advertencia", "La fecha de alta es obligatoria")
            return
        
        # Modificar médico
        ok, msg = self.controller.modificar(
            self.medico_data['matricula'],
            nombre,
            apellido,
            telefono,
            email,
            fecha_alta
        )
        
        if ok:
            messagebox.showinfo("Éxito", "✓ Médico modificado exitosamente")
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg)
