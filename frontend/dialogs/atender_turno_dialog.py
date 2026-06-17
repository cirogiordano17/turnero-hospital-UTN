import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import sys, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from data.database import Database
from .agregar_receta_dialog import AgregarRecetaDialog


class AtenderTurnoDialog:
    def __init__(self, parent, turno_data):
        """
        Diálogo para atender un turno y registrar historial clínico
        
        Args:
            parent: Ventana padre
            turno_data: Diccionario con datos del turno (id_turno, paciente, medico, fecha, etc.)
        """
        self.turno_data = turno_data
        self.recetas = []  # Lista de recetas agregadas
        self.window = tk.Toplevel(parent)
        self.window.title("Atender Turno - Registrar Historial Clínico")
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        w = min(720, int(screen_w * 0.9))
        h = min(700, int(screen_h * 0.85))
        self.window.geometry(f"{w}x{h}+{(screen_w-w)//2}+{(screen_h-h)//2}")
        self.window.resizable(True, True)
        self.window.minsize(600, 500)
        
        # Container principal con padding
        main_container = ttk.Frame(self.window, padding=10)
        main_container.pack(fill="both", expand=True)
        
        # Título (fijo arriba)
        titulo = ttk.Label(main_container, text="Registrar Atención y Historial Clínico", font=("Arial", 14, "bold"))
        titulo.pack(pady=(0, 10))
        
        # Frame con Canvas y Scrollbar para contenido scrollable
        canvas_frame = ttk.Frame(main_container)
        canvas_frame.pack(fill="both", expand=True)
        
        # Canvas sin ancho fijo
        self.canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        
        # Frame scrollable dentro del canvas
        scrollable_frame = ttk.Frame(self.canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        win_id = self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(win_id, width=e.width))
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind scroll del mouse
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Usar bind en lugar de bind_all para evitar conflictos
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        
        # Pack canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Ahora todo el contenido va en scrollable_frame
        # Frame de información del turno
        info_frame = ttk.LabelFrame(scrollable_frame, text="Información del Turno", padding=10)
        info_frame.pack(fill="x", pady=(0, 10), padx=5)
        
        info_text = f"""Paciente: {turno_data['paciente']}
Médico: {turno_data['medico']}
Consultorio: {turno_data['consultorio']}
Fecha: {turno_data['fecha']}
Horario: {turno_data['horario']}"""
        
        ttk.Label(info_frame, text=info_text, font=("Arial", 9), justify="left").pack(anchor="w")
        
        # Frame del formulario
        form_frame = ttk.LabelFrame(scrollable_frame, text="Datos del Historial Clínico", padding=10)
        form_frame.pack(fill="x", pady=(0, 10), padx=5)
        
        # Fecha de atención
        ttk.Label(form_frame, text="Fecha de atención:").grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))
        self.entry_fecha = ttk.Entry(form_frame, width=45, font=("Arial", 9))
        self.entry_fecha.insert(0, str(date.today()))
        self.entry_fecha.grid(row=0, column=1, sticky="ew", pady=6)
        
        # Diagnóstico
        ttk.Label(form_frame, text="Diagnóstico:").grid(row=1, column=0, sticky="nw", pady=6, padx=(0, 10))
        self.text_diagnostico = tk.Text(form_frame, height=3, width=45, font=("Arial", 9), wrap="word")
        self.text_diagnostico.grid(row=1, column=1, sticky="ew", pady=6)
        
        # Tratamiento
        ttk.Label(form_frame, text="Tratamiento:").grid(row=2, column=0, sticky="nw", pady=6, padx=(0, 10))
        self.text_tratamiento = tk.Text(form_frame, height=3, width=45, font=("Arial", 9), wrap="word")
        self.text_tratamiento.grid(row=2, column=1, sticky="ew", pady=6)
        
        # Observaciones
        ttk.Label(form_frame, text="Observaciones:").grid(row=3, column=0, sticky="nw", pady=6, padx=(0, 10))
        self.text_observaciones = tk.Text(form_frame, height=2, width=45, font=("Arial", 9), wrap="word")
        self.text_observaciones.grid(row=3, column=1, sticky="ew", pady=6)
        
        # Indicaciones
        ttk.Label(form_frame, text="Indicaciones:").grid(row=4, column=0, sticky="nw", pady=6, padx=(0, 10))
        self.text_indicaciones = tk.Text(form_frame, height=2, width=45, font=("Arial", 9), wrap="word")
        self.text_indicaciones.grid(row=4, column=1, sticky="ew", pady=6)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Frame de recetas
        recetas_frame = ttk.LabelFrame(scrollable_frame, text="Recetas Médicas", padding=10)
        recetas_frame.pack(fill="both", expand=True, pady=(0, 10), padx=5)
        
        # Botón para agregar receta
        btn_receta_frame = ttk.Frame(recetas_frame)
        btn_receta_frame.pack(fill="x", pady=(0, 8))
        
        ttk.Button(btn_receta_frame, text="➕ Agregar Receta", command=self._agregar_receta).pack(side="left")
        ttk.Label(btn_receta_frame, text="(Opcional)", font=("Arial", 8), foreground="gray").pack(side="left", padx=(10, 0))
        
        # Lista de recetas
        self.tree_recetas = ttk.Treeview(
            recetas_frame,
            columns=("nro", "fecha_venc", "medicamentos", "acciones"),
            show="headings",
            height=3
        )
        
        headers = [
            ("nro", "#", 35),
            ("fecha_venc", "Fecha Venc.", 90),
            ("medicamentos", "Medicamentos", 330),
            ("acciones", "Acciones", 90)
        ]
        
        for col, text, width in headers:
            self.tree_recetas.heading(col, text=text)
            self.tree_recetas.column(col, width=width)
        
        self.tree_recetas.pack(fill="both", expand=True)
        self.tree_recetas.bind("<Button-1>", self._on_receta_click)
        
        # Frame de botones (fijo abajo, fuera del scroll)
        btn_frame = ttk.Frame(main_container)
        btn_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
        ttk.Frame(btn_frame).pack(side="left", expand=True)
        
        ttk.Button(btn_frame, text="Cancelar", command=self._cancelar, width=15).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="✓ Guardar y Atender", command=self._guardar_historial, width=18).pack(side="left", padx=5)
        
        # Bind para limpiar al cerrar ventana
        self.window.protocol("WM_DELETE_WINDOW", self._cancelar)
    
    def _cancelar(self):
        """Cancela y cierra el diálogo"""
        # Unbind mousewheel antes de cerrar
        self.canvas.unbind_all("<MouseWheel>")
        self.window.destroy()
    
    def _agregar_receta(self):
        """Abre el diálogo para agregar una receta"""
        dialog = AgregarRecetaDialog(self.window)
        self.window.wait_window(dialog.window)
        
        if dialog.receta_data:
            self.recetas.append(dialog.receta_data)
            self._actualizar_lista_recetas()
    
    def _actualizar_lista_recetas(self):
        """Actualiza la lista visual de recetas"""
        # Limpiar
        for item in self.tree_recetas.get_children():
            self.tree_recetas.delete(item)
        
        # Repoblar
        for i, receta in enumerate(self.recetas, 1):
            medicamentos_str = ", ".join([d['medicamento_nombre'] for d in receta['detalles']])
            if len(medicamentos_str) > 50:
                medicamentos_str = medicamentos_str[:47] + "..."
            
            self.tree_recetas.insert("", "end", values=(
                i,
                receta['fecha_vencimiento'],
                medicamentos_str,
                "🗑️ Eliminar"
            ))
    
    def _on_receta_click(self, event):
        """Maneja clicks en la tabla de recetas"""
        try:
            item = self.tree_recetas.identify("item", event.x, event.y)
            if not item:
                return
            
            # Detectar si se clickeó en la columna de acciones
            col_num = 0
            col_x = 0
            
            for i, col in enumerate(["nro", "fecha_venc", "medicamentos", "acciones"]):
                col_width = self.tree_recetas.column(col, "width")
                if event.x < col_x + col_width:
                    col_num = i
                    break
                col_x += col_width
            
            # Si es la columna de acciones (columna 3)
            if col_num == 3:
                valores = self.tree_recetas.item(item)["values"]
                nro_receta = valores[0]
                
                # Eliminar receta
                respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar receta #{nro_receta}?")
                if respuesta:
                    del self.recetas[nro_receta - 1]
                    self._actualizar_lista_recetas()
        
        except Exception as e:
            print(f"[ERROR] Error en click: {str(e)}")
    
    def _guardar_historial(self):
        """Guarda el historial clínico y actualiza el estado del turno a 'Atendido'"""
        fecha_atencion = self.entry_fecha.get().strip()
        diagnostico = self.text_diagnostico.get("1.0", tk.END).strip()
        tratamiento = self.text_tratamiento.get("1.0", tk.END).strip()
        observaciones = self.text_observaciones.get("1.0", tk.END).strip()
        indicaciones = self.text_indicaciones.get("1.0", tk.END).strip()
        
        # Validaciones
        if not fecha_atencion:
            messagebox.showwarning("Advertencia", "La fecha de atención es obligatoria")
            return
        
        if not diagnostico:
            messagebox.showwarning("Advertencia", "El diagnóstico es obligatorio")
            return
        
        if not tratamiento:
            messagebox.showwarning("Advertencia", "El tratamiento es obligatorio")
            return
        
        # Validar formato de fecha
        try:
            fecha_obj = date.fromisoformat(fecha_atencion)
        except:
            messagebox.showwarning("Advertencia", "Fecha inválida (formato: YYYY-MM-DD)")
            return
        
        # Guardar en la BD
        db = Database()
        if not db.conectar("127.0.0.1:3306/hospital_db"):
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        
        try:
            # Obtener datos del turno
            query_turno = """
            SELECT t.id_paciente, t.id_turno
            FROM Turno t
            WHERE t.id_turno = %s
            """
            turno = db.obtener_registro(query_turno, (self.turno_data['id'],))
            
            if not turno:
                messagebox.showerror("Error", "No se encontró el turno")
                db.desconectar()
                return
            
            # Insertar historial clínico con las columnas correctas de la BD
            # Columnas reales: id_turno, id_paciente, diagnostico, tratamiento, notas, observaciones
            query_historial = """
            INSERT INTO Historial_clinico 
            (id_turno, id_paciente, diagnostico, tratamiento, notas, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            # Usar 'notas' para las indicaciones
            params_historial = (
                turno['id_turno'],
                turno['id_paciente'],
                diagnostico,
                tratamiento,
                indicaciones,  # -> columna 'notas'
                observaciones
            )
            
            resultado = db.ejecutar_consulta(query_historial, params_historial)
            
            if resultado is None or resultado == 0:
                messagebox.showerror("Error", "No se pudo guardar el historial clínico")
                db.desconectar()
                return
            
            # Obtener el ID del historial recién insertado
            id_historial = db.get_last_insert_id()
            
            if not id_historial:
                messagebox.showerror("Error", "No se pudo obtener el ID del historial")
                db.desconectar()
                return
            
            print(f"[DEBUG] Historial guardado con ID: {id_historial}")
            
            # Guardar recetas si existen
            if self.recetas:
                print(f"[DEBUG] Guardando {len(self.recetas)} receta(s)...")
                
                for idx, receta in enumerate(self.recetas, 1):
                    print(f"[DEBUG] Guardando receta #{idx}...")
                    
                    # Insertar receta
                    query_receta = """
                    INSERT INTO Receta (id_historial, fecha_emision, fecha_vencimiento, observaciones)
                    VALUES (%s, %s, %s, %s)
                    """
                    params_receta = (
                        id_historial,
                        fecha_obj,
                        receta['fecha_vencimiento'],
                        receta['observaciones']
                    )
                    
                    print(f"[DEBUG] Params receta: {params_receta}")
                    resultado_receta = db.ejecutar_consulta(query_receta, params_receta)
                    
                    if resultado_receta and resultado_receta > 0:
                        id_receta = db.get_last_insert_id()
                        print(f"[DEBUG] Receta guardada con ID: {id_receta}")
                        
                        if not id_receta:
                            print(f"[ERROR] No se pudo obtener ID de receta #{idx}")
                            continue
                        
                        # Insertar detalles de la receta
                        for det_idx, detalle in enumerate(receta['detalles'], 1):
                            print(f"[DEBUG] Guardando detalle {det_idx}/{len(receta['detalles'])}...")
                            
                            query_detalle = """
                            INSERT INTO Detalle_receta (id_receta, id_medicamento, dosis, indicaciones, cantidad)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                            params_detalle = (
                                id_receta,
                                detalle['id_medicamento'],
                                detalle['dosis'],
                                detalle['indicacion'],
                                detalle['cantidad']
                            )
                            
                            print(f"[DEBUG] Params detalle: {params_detalle}")
                            resultado_detalle = db.ejecutar_consulta(query_detalle, params_detalle)
                            
                            if resultado_detalle and resultado_detalle > 0:
                                print(f"[DEBUG] ✓ Detalle guardado")
                            else:
                                print(f"[ERROR] ✗ Error guardando detalle")
                    else:
                        print(f"[ERROR] Error al guardar receta #{idx}")
            
            # Actualizar estado del turno a "Atendido"
            query_turno_update = """
            UPDATE Turno 
            SET estado = 'Atendido'
            WHERE id_turno = %s
            """
            
            db.ejecutar_consulta(query_turno_update, (self.turno_data['id'],))
            
            db.desconectar()
            
            mensaje_exito = "✓ Turno atendido y historial clínico registrado exitosamente"
            if self.recetas:
                mensaje_exito += f"\n✓ Se guardaron {len(self.recetas)} receta(s) médica(s)"
            
            # Unbind mousewheel antes de cerrar
            self.canvas.unbind_all("<MouseWheel>")
            
            messagebox.showinfo("Éxito", mensaje_exito)
            
            # Preguntar si desea imprimir receta
            if self.recetas:
                respuesta = messagebox.askyesno(
                    "Imprimir Receta",
                    "¿Desea imprimir la receta médica?",
                    parent=self.window
                )
                
                if respuesta:
                    self._imprimir_receta(id_historial, fecha_obj)
            
            self.window.destroy()
        
        except Exception as e:
            db.desconectar()
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def _imprimir_receta(self, id_historial, fecha_emision):
        """Genera PDF de la receta asociada al historial clínico"""
        try:
            # Buscar la receta asociada al historial
            db = Database()
            if not db.conectar("127.0.0.1:3306/hospital_db"):
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
            
            query = "SELECT id_receta FROM Receta WHERE id_historial = %s LIMIT 1"
            resultado = db.obtener_registro(query, (id_historial,))
            db.desconectar()
            
            if not resultado or 'id_receta' not in resultado:
                messagebox.showwarning("Sin receta", "No se encontró receta para este historial")
                return
            
            id_receta = resultado['id_receta']
            
            # Importar controller de recetas
            from ..controllers.recetas_controller import RecetasController
            ctrl = RecetasController()
            
            # Elegir destino del PDF
            from tkinter import filedialog
            archivo = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=f"receta_{id_receta}_{fecha_emision}.pdf",
                filetypes=[("PDF", "*.pdf")]
            )
            
            if not archivo:
                return
            
            # Generar PDF
            ok = ctrl.generar_pdf(id_receta, archivo)
            if ok:
                messagebox.showinfo("Éxito", f"Receta #{id_receta} generada exitosamente:\n{archivo}")
            else:
                messagebox.showerror("Error", "Error al generar el PDF. Verifique que reportlab esté instalado.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al imprimir receta: {str(e)}")
