import tkinter.simpledialog
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from controllers.turnos import ControladorTurnos
from utils.graphviz_generator import GraphvizGenerator
import threading
import time
import os

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL no está instalado. Para instalarlo ejecute: pip install Pillow")


class ModernMedicalApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_style()
        self.controlador = ControladorTurnos()
        self.graphviz = GraphvizGenerator()

        self.current_image = None
        self.stats_image = None
        self.auto_refresh = tk.BooleanVar(value=True)

        self.create_widgets()
        self.setup_layout()
        self.update_display()

        self.auto_update_loop()

    def setup_window(self):
        self.root.title(
            "🏥 Sistema de Gestión de Turnos Médicos - Clínica Digital")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(True, True)

        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f'1200x800+{x}+{y}')

    def setup_style(self):
        self.style = ttk.Style()

        self.style.theme_use('clam')

        colors = {
            'primary': '#2c5aa0',
            'secondary': '#4a90e2',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'white': '#ffffff',
            'background': '#f8fafc'
        }

        self.style.configure('Primary.TButton',
                             background=colors['primary'],
                             foreground='white',
                             font=('Segoe UI', 10, 'bold'),
                             padding=(20, 10),
                             focuscolor='none')

        self.style.map('Primary.TButton',
                       background=[('active', colors['secondary'])])

        self.style.configure('Success.TButton',
                             background=colors['success'],
                             foreground='white',
                             font=('Segoe UI', 9, 'bold'),
                             padding=(15, 8))

        self.style.configure('Warning.TButton',
                             background=colors['warning'],
                             foreground='white',
                             font=('Segoe UI', 9, 'bold'),
                             padding=(15, 8))

        self.style.configure('Danger.TButton',
                             background=colors['danger'],
                             foreground='white',
                             font=('Segoe UI', 9, 'bold'),
                             padding=(15, 8))

        self.style.configure('Header.TLabel',
                             font=('Segoe UI', 16, 'bold'),
                             background='#f0f4f8',
                             foreground=colors['dark'])

        self.style.configure('Info.TLabel',
                             font=('Segoe UI', 11),
                             background='#f0f4f8',
                             foreground=colors['dark'])

        self.style.configure('Modern.TLabelframe',
                             background='white',
                             relief='solid',
                             borderwidth=1)

        self.style.configure('Modern.TLabelframe.Label',
                             font=('Segoe UI', 12, 'bold'),
                             background='white',
                             foreground=colors['primary'])

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg="#f0f4f8")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_header()

        self.create_left_panel()

        self.create_right_panel()

        self.create_bottom_panel()

    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg="#2c5aa0", height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame,
                               text="🏥 Sistema de Gestión de Turnos Médicos",
                               font=('Segoe UI', 20, 'bold'),
                               bg="#2c5aa0",
                               fg="white")
        title_label.pack(side="left", padx=20, pady=20)

        self.status_frame = tk.Frame(header_frame, bg="#2c5aa0")
        self.status_frame.pack(side="right", padx=20, pady=15)

        self.status_label = tk.Label(self.status_frame,
                                     text="🟢 Sistema Activo",
                                     font=('Segoe UI', 12),
                                     bg="#2c5aa0",
                                     fg="white")
        self.status_label.pack()

        self.time_label = tk.Label(self.status_frame,
                                   text="",
                                   font=('Segoe UI', 10),
                                   bg="#2c5aa0",
                                   fg="white")
        self.time_label.pack()
        self.update_time()

    def create_left_panel(self):
        left_frame = tk.Frame(self.main_frame, bg="#f0f4f8", width=400)
        left_frame.pack(side="left", fill="y", padx=(0, 20))
        left_frame.pack_propagate(False)

        registro_frame = ttk.LabelFrame(left_frame,
                                        text="📝 Registrar Nuevo Paciente",
                                        style="Modern.TLabelframe",
                                        padding=20)
        registro_frame.pack(fill="x", pady=(0, 20))

        tk.Label(registro_frame, text="Nombre completo:",
                 font=('Segoe UI', 10, 'bold'), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nombre = ttk.Entry(
            registro_frame, font=('Segoe UI', 10), width=25)
        self.entry_nombre.grid(row=0, column=1, pady=5, padx=(10, 0))

        tk.Label(registro_frame, text="Edad:",
                 font=('Segoe UI', 10, 'bold'), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_edad = ttk.Entry(
            registro_frame, font=('Segoe UI', 10), width=25)
        self.entry_edad.grid(row=1, column=1, pady=5, padx=(10, 0))

        tk.Label(registro_frame, text="Especialidad:",
                 font=('Segoe UI', 10, 'bold'), bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_especialidad = ttk.Combobox(registro_frame,
                                               values=self.controlador.obtener_especialidades_disponibles(),
                                               state="readonly",
                                               font=('Segoe UI', 10),
                                               width=22)
        self.combo_especialidad.grid(row=2, column=1, pady=5, padx=(10, 0))

        btn_registrar = ttk.Button(registro_frame,
                                   text="➕ Registrar Paciente",
                                   style="Success.TButton",
                                   command=self.registrar_paciente)
        btn_registrar.grid(row=3, columnspan=2, pady=15)

        gestion_frame = ttk.LabelFrame(left_frame,
                                       text="⚕️ Gestión de Turnos",
                                       style="Modern.TLabelframe",
                                       padding=20)
        gestion_frame.pack(fill="x", pady=(0, 20))

        btn_atender = ttk.Button(gestion_frame,
                                 text="👨‍⚕️ Atender Próximo Paciente",
                                 style="Primary.TButton",
                                 command=self.atender_paciente)
        btn_atender.pack(fill="x", pady=5)

        btn_siguiente = ttk.Button(gestion_frame,
                                   text="🔍 Ver Siguiente en Cola",
                                   style="Warning.TButton",
                                   command=self.ver_siguiente)
        btn_siguiente.pack(fill="x", pady=5)

        btn_buscar = ttk.Button(gestion_frame,
                                text="🔎 Buscar Paciente",
                                command=self.buscar_paciente)
        btn_buscar.pack(fill="x", pady=5)

        btn_limpiar = ttk.Button(gestion_frame,
                                 text="🧹 Limpiar Cola",
                                 style="Danger.TButton",
                                 command=self.limpiar_cola)
        btn_limpiar.pack(fill="x", pady=5)

        estado_frame = ttk.LabelFrame(left_frame,
                                      text="📊 Estado Actual",
                                      style="Modern.TLabelframe",
                                      padding=15)
        estado_frame.pack(fill="both", expand=True)

        self.info_text = scrolledtext.ScrolledText(estado_frame,
                                                   height=8,
                                                   font=('Consolas', 9),
                                                   wrap="word",
                                                   state="disabled")
        self.info_text.pack(fill="both", expand=True)

        self.auto_refresh_check = ttk.Checkbutton(estado_frame,
                                                  text="🔄 Actualización automática",
                                                  variable=self.auto_refresh)
        self.auto_refresh_check.pack(pady=(10, 0))

    def create_right_panel(self):
        right_frame = tk.Frame(self.main_frame, bg="#f0f4f8")
        right_frame.pack(side="right", fill="both", expand=True)

        viz_frame = ttk.LabelFrame(right_frame,
                                   text="📈 Visualización de Cola en Tiempo Real",
                                   style="Modern.TLabelframe",
                                   padding=15)
        viz_frame.pack(fill="both", expand=True, pady=(0, 10))

        canvas_frame = tk.Frame(viz_frame, bg="white", relief="sunken", bd=2)
        canvas_frame.pack(fill="both", expand=True)

        self.queue_canvas = tk.Label(canvas_frame,
                                     text="Cargando visualización...",
                                     bg="white",
                                     font=('Segoe UI', 12))
        self.queue_canvas.pack(expand=True, fill="both")

        btn_refresh = ttk.Button(viz_frame,
                                 text="🔄 Actualizar Visualización",
                                 command=self.update_visualization_manual)
        btn_refresh.pack(pady=5)

        stats_frame = ttk.LabelFrame(right_frame,
                                     text="📊 Estadísticas por Especialidad",
                                     style="Modern.TLabelframe",
                                     padding=15)
        stats_frame.pack(fill="x", pady=(10, 0))

        stats_canvas_frame = tk.Frame(
            stats_frame, bg="white", relief="sunken", bd=2, height=200)
        stats_canvas_frame.pack(fill="x", pady=5)
        stats_canvas_frame.pack_propagate(False)

        self.stats_canvas = tk.Label(stats_canvas_frame,
                                     text="Estadísticas se cargarán aquí...",
                                     bg="white",
                                     font=('Segoe UI', 10))
        self.stats_canvas.pack(expand=True)

        btn_stats = ttk.Button(stats_frame,
                               text="📈 Generar Estadísticas",
                               command=self.generar_estadisticas)
        btn_stats.pack(pady=5)

    def create_bottom_panel(self):
        bottom_frame = tk.Frame(self.main_frame, bg="#ecf0f1", height=60)
        bottom_frame.pack(fill="x", pady=(20, 0))
        bottom_frame.pack_propagate(False)

        self.system_info = tk.Label(bottom_frame,
                                    text="🔄 Sistema listo | Última actualización: --",
                                    font=('Segoe UI', 9),
                                    bg="#ecf0f1",
                                    fg="#2c3e50")
        self.system_info.pack(side="left", padx=20, pady=15)

        graphviz_status = "✅ Graphviz disponible" if self.graphviz.is_available(
        ) else "❌ Graphviz no disponible"
        self.graphviz_info = tk.Label(bottom_frame,
                                      text=graphviz_status,
                                      font=('Segoe UI', 9),
                                      bg="#ecf0f1",
                                      fg="#27ae60" if self.graphviz.is_available() else "#e74c3c")
        self.graphviz_info.pack(side="right", padx=20, pady=15)

    def setup_layout(self):
        pass

    def registrar_paciente(self):
        nombre = self.entry_nombre.get().strip()
        edad_str = self.entry_edad.get().strip()
        especialidad = self.combo_especialidad.get()

        if not nombre:
            messagebox.showerror(
                "❌ Error", "Por favor ingrese el nombre del paciente")
            return

        try:
            edad = int(edad_str)
        except ValueError:
            messagebox.showerror(
                "❌ Error", "La edad debe ser un número válido")
            return

        if not especialidad:
            messagebox.showerror(
                "❌ Error", "Por favor seleccione una especialidad")
            return

        success, mensaje = self.controlador.registrar_paciente(
            nombre, edad, especialidad)

        if success:
            messagebox.showinfo("✅ Éxito", mensaje)
            self.entry_nombre.delete(0, tk.END)
            self.entry_edad.delete(0, tk.END)
            self.combo_especialidad.set("")
            self.update_display()
        else:
            messagebox.showerror("❌ Error", mensaje)

    def atender_paciente(self):
        paciente, mensaje = self.controlador.atender_paciente()

        if paciente:
            messagebox.showinfo("✅ Paciente Atendido", mensaje)
        else:
            messagebox.showwarning("⚠️ Aviso", mensaje)

        self.update_display()

    def ver_siguiente(self):
        paciente, mensaje = self.controlador.ver_siguiente_paciente()

        if paciente:
            messagebox.showinfo("ℹ️ Próximo Paciente", mensaje)
        else:
            messagebox.showinfo("ℹ️ Información", mensaje)

    def buscar_paciente(self):
        nombre = tk.simpledialog.askstring("🔍 Buscar Paciente",
                                           "Ingrese el nombre del paciente:")

        if nombre:
            posicion, mensaje = self.controlador.obtener_posicion_paciente(
                nombre)
            if posicion != -1:
                messagebox.showinfo("✅ Paciente Encontrado", mensaje)
            else:
                messagebox.showwarning("⚠️ No Encontrado", mensaje)

    def limpiar_cola(self):
        if messagebox.askyesno("⚠️ Confirmación",
                               "¿Está seguro de que desea limpiar toda la cola?\n"
                               "Esta acción no se puede deshacer."):
            mensaje = self.controlador.limpiar_turnos()
            messagebox.showinfo("✅ Cola Limpiada", mensaje)
            self.update_display()

    def generar_estadisticas(self):
        stats = self.controlador.obtener_estadisticas_especialidad()

        if self.graphviz.is_available():
            success, filepath, mensaje = self.graphviz.generate_statistics_graph(
                stats)

            if success and os.path.exists(filepath) and PIL_AVAILABLE:
                try:
                    img = Image.open(filepath)
                    img = img.resize((400, 180), Image.Resampling.LANCZOS)
                    self.stats_image = ImageTk.PhotoImage(img)
                    self.stats_canvas.config(image=self.stats_image, text="")
                except Exception as e:
                    self.stats_canvas.config(
                        text=f"Error al cargar imagen: {str(e)}")
            else:
                stats_text = "Estadísticas por Especialidad:\n\n"
                for especialidad, cantidad in stats.items():
                    stats_text += f"{especialidad}: {cantidad} paciente(s)\n"
                self.stats_canvas.config(text=stats_text)
        else:
            stats_text = "Estadísticas por Especialidad:\n\n"
            for especialidad, cantidad in stats.items():
                stats_text += f"{especialidad}: {cantidad} paciente(s)\n"
            self.stats_canvas.config(text=stats_text)

    def update_visualization_manual(self):
        self.update_display()
        messagebox.showinfo(
            "✅ Actualizado", "Visualización actualizada correctamente")

    def update_display(self):
        self.update_queue_info()
        self.update_queue_visualization()
        self.update_system_status()

    def update_queue_info(self):
        estado = self.controlador.obtener_estado_cola()
        pacientes = self.controlador.obtener_lista_pacientes()

        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)

        info = f"🏥 ESTADO DE LA COLA\n"
        info += f"{'='*40}\n\n"
        info += f"📊 Total de pacientes en espera: {estado['total_pacientes']}\n"
        info += f"⏱️  Tiempo total estimado: {estado['tiempo_total_estimado']} minutos\n"
        info += f"👥 Pacientes atendidos hoy: {estado['pacientes_atendidos_hoy']}\n\n"

        if estado['esta_vacia']:
            info += "📋 La cola está vacía\n"
            info += "✨ No hay pacientes esperando\n"
        else:
            info += f"🔄 PRÓXIMO PACIENTE:\n"
            siguiente = estado['siguiente_paciente']
            if siguiente:
                info += f"   👤 {siguiente.nombre}\n"
                info += f"   🎂 {siguiente.edad} años\n"
                info += f"   ⚕️  {siguiente.especialidad}\n"
                info += f"   ⏲️  {siguiente.tiempo_atencion} min\n\n"

            info += f"📝 LISTA COMPLETA ({len(pacientes)} pacientes):\n"
            info += f"{'-'*40}\n"

            for i, paciente in enumerate(pacientes, 1):
                info += f"{i:2d}. {paciente.nombre} ({paciente.edad}a)\n"
                info += f"     {paciente.especialidad}\n"
                info += f"     Espera: {paciente.tiempo_espera_estimado} min"
                info += f" | Atención: {paciente.tiempo_atencion} min\n\n"

        self.info_text.insert(1.0, info)
        self.info_text.config(state="disabled")

        self.info_text.see(1.0)

    def update_queue_visualization(self):
        if not self.graphviz.is_available():
            self.queue_canvas.config(text="❌ Graphviz no disponible\n\n"
                                     "Para visualización gráfica,\n"
                                     "instale Graphviz:\n"
                                     "pip install graphviz")
            return

        pacientes = self.controlador.obtener_lista_pacientes()

        success, filepath, mensaje = self.graphviz.generate_queue_graph(
            pacientes)

        if success and os.path.exists(filepath):
            if PIL_AVAILABLE:
                try:
                    img = Image.open(filepath)
                    img.thumbnail((600, 400), Image.Resampling.LANCZOS)
                    self.current_image = ImageTk.PhotoImage(img)
                    self.queue_canvas.config(image=self.current_image, text="")
                except Exception as e:
                    self.queue_canvas.config(
                        text=f"❌ Error al cargar imagen:\n{str(e)}")
            else:
                simple_repr = self.graphviz.generate_simple_queue_representation(
                    pacientes)
                self.queue_canvas.config(text=simple_repr)
        else:
            self.queue_canvas.config(
                text=f"❌ Error en visualización:\n{mensaje}")

    def update_system_status(self):
        import datetime
        now = datetime.datetime.now()
        timestamp = now.strftime("%H:%M:%S")

        estado = self.controlador.obtener_estado_cola()
        status_text = f"🔄 Última actualización: {timestamp} | "
        status_text += f"Cola: {estado['total_pacientes']} pacientes | "
        status_text += f"Tiempo estimado: {estado['tiempo_total_estimado']} min"

        self.system_info.config(text=status_text)

    def update_time(self):
        import datetime
        now = datetime.datetime.now()
        time_str = now.strftime("%d/%m/%Y - %H:%M:%S")
        self.time_label.config(text=time_str)

        self.root.after(1000, self.update_time)

    def auto_update_loop(self):
        if self.auto_refresh.get():
            self.update_display()

        self.root.after(5000, self.auto_update_loop)


def main():
    root = tk.Tk()
    app = ModernMedicalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
