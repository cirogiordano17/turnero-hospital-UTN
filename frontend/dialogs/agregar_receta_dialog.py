import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
import sys, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from data.database import Database


class AgregarRecetaDialog:
    def __init__(self, parent):
        """Diálogo para crear una receta con sus detalles"""
        self.window = tk.Toplevel(parent)
        self.window.title("Agregar Receta")
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        w = min(720, int(screen_w * 0.9))
        h = min(620, int(screen_h * 0.85))
        self.window.geometry(f"{w}x{h}+{(screen_w-w)//2}+{(screen_h-h)//2}")
        self.window.resizable(True, True)
        self.window.minsize(580, 450)
        
        # Datos de la receta
        self.receta_data = None
        self.detalles_receta = []
        
        # Container principal
        container = ttk.Frame(self.window)
        container.pack(fill="both", expand=True)
        
        # Título
        titulo_frame = ttk.Frame(container)
        titulo_frame.pack(fill="x", padx=10, pady=(8, 8))
        ttk.Label(titulo_frame, text="Nueva Receta Médica", font=("Arial", 13, "bold")).pack()
        
        # Datos de la receta
        datos_frame = ttk.LabelFrame(container, text="Datos de la Receta", padding=10)
        datos_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        ttk.Label(datos_frame, text="Fecha vencimiento:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_fecha_venc = ttk.Entry(datos_frame, width=45)
        self.entry_fecha_venc.insert(0, str(date.today() + timedelta(days=30)))
        self.entry_fecha_venc.grid(row=0, column=1, sticky="ew", pady=5)
        
        ttk.Label(datos_frame, text="Observaciones:").grid(row=1, column=0, sticky="nw", pady=5)
        self.text_obs = tk.Text(datos_frame, height=2, width=45, font=("Arial", 9))
        self.text_obs.grid(row=1, column=1, sticky="ew", pady=5)
        
        datos_frame.columnconfigure(1, weight=1)
        
        # Medicamentos
        med_frame = ttk.LabelFrame(container, text="Medicamentos", padding=10)
        med_frame.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        
        # Botón agregar
        ttk.Button(med_frame, text="➕ Agregar Medicamento", 
                  command=self._agregar_medicamento).pack(anchor="w", pady=(0, 5))
        
        # Tabla
        cols = ("medicamento", "dosis", "cant", "indicacion")
        self.tree = ttk.Treeview(med_frame, columns=cols, show="headings", height=8)
        
        self.tree.heading("medicamento", text="Medicamento")
        self.tree.heading("dosis", text="Dosis")
        self.tree.heading("cant", text="Cant.")
        self.tree.heading("indicacion", text="Indicación")
        
        self.tree.column("medicamento", width=180)
        self.tree.column("dosis", width=100)
        self.tree.column("cant", width=60)
        self.tree.column("indicacion", width=250)
        
        scroll = ttk.Scrollbar(med_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        
        # Botón eliminar
        ttk.Button(med_frame, text="🗑️ Eliminar", 
                  command=self._eliminar_medicamento).pack(anchor="w", pady=(5, 0))
        
        # Botones
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        ttk.Frame(btn_frame).pack(side="left", expand=True)
        ttk.Button(btn_frame, text="Cancelar", command=self._cerrar, width=12).pack(side="left", padx=3)
        ttk.Button(btn_frame, text="✓ Guardar", command=self._guardar, width=12).pack(side="left", padx=3)
        
        self.window.protocol("WM_DELETE_WINDOW", self._cerrar)
    
    def _cerrar(self):
        self.window.destroy()
    
    def _agregar_medicamento(self):
        dialog = AgregarMedicamentoDialog(self.window)
        self.window.wait_window(dialog.window)
        
        if dialog.medicamento_data:
            self.detalles_receta.append(dialog.medicamento_data)
            self._actualizar_tabla()
    
    def _eliminar_medicamento(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un medicamento")
            return
        
        idx = self.tree.index(sel[0])
        del self.detalles_receta[idx]
        self._actualizar_tabla()
    
    def _actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for d in self.detalles_receta:
            self.tree.insert("", "end", values=(
                d['medicamento_nombre'],
                d['dosis'],
                d['cantidad'],
                d['indicacion']
            ))
    
    def _guardar(self):
        fecha_venc = self.entry_fecha_venc.get().strip()
        obs = self.text_obs.get("1.0", tk.END).strip()
        
        if not fecha_venc:
            messagebox.showwarning("Advertencia", "La fecha de vencimiento es obligatoria")
            return
        
        try:
            fecha_obj = date.fromisoformat(fecha_venc)
        except:
            messagebox.showwarning("Advertencia", "Fecha inválida (YYYY-MM-DD)")
            return
        
        if not self.detalles_receta:
            messagebox.showwarning("Advertencia", "Agrega al menos un medicamento")
            return
        
        self.receta_data = {
            'fecha_vencimiento': fecha_obj,
            'observaciones': obs,
            'detalles': self.detalles_receta.copy()
        }
        
        self._cerrar()


class AgregarMedicamentoDialog:
    def __init__(self, parent):
        self.medicamento_data = None
        self.window = tk.Toplevel(parent)
        self.window.title("Agregar Medicamento")
        self.window.geometry("580x420")
        self.window.resizable(False, False)
        
        container = ttk.Frame(self.window)
        container.pack(fill="both", expand=True)
        
        # Título
        ttk.Label(container, text="Agregar Medicamento", 
                 font=("Arial", 12, "bold")).pack(pady=(10, 15))
        
        # Formulario
        form = ttk.Frame(container, padding=10)
        form.pack(fill="both", expand=True)
        
        ttk.Label(form, text="Medicamento:").grid(row=0, column=0, sticky="w", pady=8)
        
        self.medicamentos = self._cargar_medicamentos()
        self.med_var = tk.StringVar()
        
        if self.medicamentos:
            nombres = [f"{m['nombre']} ({m['presentacion']})" for m in self.medicamentos]
            self.combo = ttk.Combobox(form, textvariable=self.med_var, 
                                     values=nombres, state="readonly", width=42)
            self.combo.grid(row=0, column=1, columnspan=2, sticky="ew", pady=8)
        else:
            ttk.Label(form, text="Sin medicamentos", foreground="red").grid(row=0, column=1, pady=8)
        
        # Dosis - ahora con valor numérico y unidad separados
        ttk.Label(form, text="Dosis:").grid(row=1, column=0, sticky="w", pady=8)
        
        # Frame para valor y unidad
        dosis_frame = ttk.Frame(form)
        dosis_frame.grid(row=1, column=1, columnspan=2, sticky="ew", pady=8)
        
        self.entry_dosis_valor = ttk.Entry(dosis_frame, width=15)
        self.entry_dosis_valor.insert(0, "1")
        self.entry_dosis_valor.pack(side="left", padx=(0, 5))
        
        # Combobox para unidad de medida
        self.unidad_var = tk.StringVar(value="mg")
        unidades = ["mg", "g", "ml", "mcg", "UI", "comprimido(s)", "cápsula(s)", "ampolla(s)", "gota(s)", "unidad(es)"]
        self.combo_unidad = ttk.Combobox(dosis_frame, textvariable=self.unidad_var, 
                                         values=unidades, state="readonly", width=15)
        self.combo_unidad.pack(side="left")
        
        ttk.Label(form, text="Cantidad:").grid(row=2, column=0, sticky="w", pady=8)
        self.entry_cant = ttk.Entry(form, width=45)
        self.entry_cant.insert(0, "1")
        self.entry_cant.grid(row=2, column=1, columnspan=2, sticky="ew", pady=8)
        
        ttk.Label(form, text="Indicación:").grid(row=3, column=0, sticky="nw", pady=8)
        self.text_ind = tk.Text(form, height=4, width=45, font=("Arial", 9))
        self.text_ind.insert("1.0", "Tomar cada 8 horas")
        self.text_ind.grid(row=3, column=1, columnspan=2, sticky="ew", pady=8)
        
        form.columnconfigure(1, weight=1)
        
        # Botones
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        ttk.Frame(btn_frame).pack(side="left", expand=True)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy, width=12).pack(side="left", padx=3)
        ttk.Button(btn_frame, text="✓ Agregar", command=self._agregar, width=12).pack(side="left", padx=3)
    
    def _cargar_medicamentos(self):
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            return []
        
        try:
            query = "SELECT id_medicamento, nombre, presentacion FROM Medicamento ORDER BY nombre"
            meds = db.obtener_registros(query)
            db.desconectar()
            return meds if meds else []
        except Exception as e:
            print(f"[ERROR] {e}")
            db.desconectar()
            return []
    
    def _agregar(self):
        if not self.medicamentos:
            messagebox.showerror("Error", "No hay medicamentos")
            return
        
        idx = self.combo.current()
        if idx < 0:
            messagebox.showwarning("Advertencia", "Selecciona un medicamento")
            return
        
        dosis_valor = self.entry_dosis_valor.get().strip()
        unidad = self.unidad_var.get().strip()
        cant = self.entry_cant.get().strip()
        ind = self.text_ind.get("1.0", tk.END).strip()
        
        if not dosis_valor or not unidad or not cant or not ind:
            messagebox.showwarning("Advertencia", "Completa todos los campos")
            return
        
        # Validar que dosis_valor sea un número (puede ser decimal)
        try:
            dosis_num = float(dosis_valor)
            if dosis_num <= 0:
                messagebox.showwarning("Advertencia", "La dosis debe ser un número mayor a 0")
                return
        except ValueError:
            messagebox.showwarning("Advertencia", "La dosis debe ser un número válido")
            return
        
        # Validar que cantidad sea un número entero
        try:
            cant_int = int(cant)
            if cant_int <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser un número mayor a 0")
                return
        except ValueError:
            messagebox.showwarning("Advertencia", "La cantidad debe ser un número entero")
            return
        
        med = self.medicamentos[idx]
        
        # Concatenar dosis con unidad para guardar en BD
        dosis_completa = f"{dosis_valor} {unidad}"
        
        self.medicamento_data = {
            'id_medicamento': med['id_medicamento'],
            'medicamento_nombre': med['nombre'],
            'presentacion': med['presentacion'],
            'dosis': dosis_completa,  # Ej: "500 mg" o "2.5 ml"
            'cantidad': cant_int,
            'indicacion': ind
        }
        
        self.window.destroy()
