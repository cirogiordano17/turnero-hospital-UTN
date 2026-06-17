import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import sys, os

# Agregar TPDAO al path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from data.database import Database
from frontend.widgets.scrollable_frame import ScrollableFrame


class CrearMedicoDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.window = tk.Toplevel(parent)
        self.window.title("Crear Nuevo Médico")
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        w, h = min(620, int(sw * 0.9)), min(620, int(sh * 0.85))
        self.window.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.window.resizable(True, True)
        self.window.minsize(480, 420)

        container = ttk.Frame(self.window, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Registrar Nuevo Médico", font=("Arial", 14, "bold")).pack(pady=(0, 10))

        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", side="bottom", pady=(10, 0))
        ttk.Frame(btn_frame).pack(side="left", expand=True)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy, width=12).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="✓ Crear", command=self._crear_medico, width=12).pack(side="left", padx=5)

        scroll = ScrollableFrame(container)
        scroll.pack(fill="both", expand=True)
        form_frame = scroll.inner
        
        # Matrícula
        ttk.Label(form_frame, text="Matrícula:").grid(row=0, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_matricula = ttk.Entry(form_frame, width=35, font=("Arial", 9))
        self.entry_matricula.grid(row=0, column=1, sticky="ew", pady=8)
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_nombre = ttk.Entry(form_frame, width=35, font=("Arial", 9))
        self.entry_nombre.grid(row=1, column=1, sticky="ew", pady=8)
        
        # Apellido
        ttk.Label(form_frame, text="Apellido:").grid(row=2, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_apellido = ttk.Entry(form_frame, width=35, font=("Arial", 9))
        self.entry_apellido.grid(row=2, column=1, sticky="ew", pady=8)
        
        # Teléfono
        ttk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_telefono = ttk.Entry(form_frame, width=35, font=("Arial", 9))
        self.entry_telefono.grid(row=3, column=1, sticky="ew", pady=8)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_email = ttk.Entry(form_frame, width=35, font=("Arial", 9))
        self.entry_email.grid(row=4, column=1, sticky="ew", pady=8)
        
        # Fecha de Alta
        ttk.Label(form_frame, text="Fecha Alta (YYYY-MM-DD):").grid(row=5, column=0, sticky="w", pady=8, padx=(0, 15))
        self.entry_fecha_alta = ttk.Entry(form_frame, width=35, font=("Arial", 9))
        self.entry_fecha_alta.insert(0, str(date.today()))
        self.entry_fecha_alta.grid(row=5, column=1, sticky="ew", pady=8)
        
        # Especialidades con checkboxes y scroll
        ttk.Label(form_frame, text="Especialidades:").grid(row=6, column=0, sticky="nw", pady=(8, 0), padx=(0, 15))
        
        # Frame para especialidades con Canvas y Scrollbar
        esp_outer_frame = ttk.LabelFrame(form_frame, text="Selecciona una o más", padding=5)
        esp_outer_frame.grid(row=6, column=1, sticky="ew", pady=8)
        
        # Canvas para scroll
        canvas = tk.Canvas(esp_outer_frame, height=150, highlightthickness=0)
        scrollbar = ttk.Scrollbar(esp_outer_frame, orient="vertical", command=canvas.yview)
        
        # Frame scrollable
        self.esp_frame_scroll = ttk.Frame(canvas)
        self.esp_frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.esp_frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cargar especialidades
        self.especialidades = self._cargar_especialidades()
        self.var_especialidades = {}
        
        if self.especialidades:
            for esp in self.especialidades:
                var = tk.BooleanVar()
                self.var_especialidades[esp['id']] = var
                
                checkbox = ttk.Checkbutton(
                    self.esp_frame_scroll,
                    text=f"{esp['nombre']} - {esp['descripcion']}",
                    variable=var
                )
                checkbox.pack(anchor="w", pady=2, padx=5)
        else:
            ttk.Label(self.esp_frame_scroll, text="No hay especialidades disponibles", foreground="gray").pack(anchor="w", padx=5)
        
        form_frame.columnconfigure(1, weight=1)
    
    def _cargar_especialidades(self):
        """Carga las especialidades desde la BD"""
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = "SELECT id_especialidad as id, nombre, descripcion FROM Especialidad ORDER BY nombre"
            especialidades = db.obtener_registros(query)
            db.desconectar()
            return especialidades if especialidades else []
        except Exception as e:
            print(f"[ERROR] Error al cargar especialidades: {str(e)}")
            db.desconectar()
            return []
    
    def _crear_medico(self):
        """Valida y crea el médico"""
        matricula = self.entry_matricula.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()
        fecha_alta = self.entry_fecha_alta.get().strip()
        
        # Validaciones
        if not matricula:
            messagebox.showwarning("Advertencia", "La matrícula es obligatoria")
            return
        
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
        
        # Obtener especialidades seleccionadas desde checkboxes
        especialidades_ids = [
            esp_id for esp_id, var in self.var_especialidades.items() if var.get()
        ]
        
        # Crear médico
        ok, msg = self.controller.crear(
            matricula,
            nombre,
            apellido,
            telefono,
            email,
            fecha_alta,
            especialidades_ids
        )
        
        if ok:
            messagebox.showinfo("Éxito", "✓ Médico creado exitosamente")
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg)
