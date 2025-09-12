import tkinter as tk
from tkinter import ttk, messagebox
from controllers.turnos import ControladorTurnos
from utils.graphviz_generator import GraphvizGenerator
from PIL import Image, ImageTk
import os


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 Sistema de Turnos Médicos")
        self.root.geometry("950x650")
        self.root.configure(bg="#e6f2ff")  # fondo azul claro

        self.controlador = ControladorTurnos()
        self.graphviz = GraphvizGenerator()

        # Aplicar estilo ttk
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10, "bold"), background="#007acc", foreground="white")
        style.configure("TLabel", font=("Arial", 11), background="#e6f2ff")
        style.configure("TLabelframe", font=("Arial", 12, "bold"), background="#cce6ff")

        # --- Registro ---
        frame_registro = ttk.LabelFrame(root, text="Registrar Paciente", padding=15)
        frame_registro.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_registro, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_nombre = ttk.Entry(frame_registro, width=25)
        self.entry_nombre.grid(row=0, column=1, padx=5)

        ttk.Label(frame_registro, text="Edad:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_edad = ttk.Entry(frame_registro, width=25)
        self.entry_edad.grid(row=1, column=1, padx=5)

        ttk.Label(frame_registro, text="Especialidad:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.combo_especialidad = ttk.Combobox(
            frame_registro, values=self.controlador.obtener_especialidades_disponibles(), state="readonly", width=22
        )
        self.combo_especialidad.grid(row=2, column=1, padx=5)

        ttk.Button(frame_registro, text="➕ Registrar", command=self.registrar_paciente).grid(row=3, columnspan=2, pady=8)

        # --- Cola ---
        frame_cola = ttk.LabelFrame(root, text="Gestión de Turnos", padding=15)
        frame_cola.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_cola, text="👨‍⚕️ Atender Paciente", command=self.atender_paciente).pack(side="left", padx=10)
        ttk.Button(frame_cola, text="🔎 Ver Siguiente", command=self.ver_siguiente).pack(side="left", padx=10)
        ttk.Button(frame_cola, text="🧹 Limpiar Cola", command=self.limpiar_cola).pack(side="left", padx=10)
        ttk.Button(frame_cola, text="📊 Ver Estadísticas", command=self.ver_estadisticas).pack(side="left", padx=10)

        # --- Info Cola ---
        self.label_info = ttk.Label(root, text="Cola vacía", font=("Arial", 13, "bold"))
        self.label_info.pack(pady=10)

        # --- Visualización Cola ---
        self.canvas = tk.Label(root, bg="#e6f2ff")
        self.canvas.pack(pady=5)

        # --- Visualización Estadísticas ---
        self.stats_canvas = tk.Label(root, bg="#e6f2ff")
        self.stats_canvas.pack(pady=5)

        self.actualizar_visualizacion()

    def registrar_paciente(self):
        nombre = self.entry_nombre.get()
        try:
            edad = int(self.entry_edad.get())
        except:
            messagebox.showerror("Error", "Edad inválida")
            return
        especialidad = self.combo_especialidad.get()

        ok, msg = self.controlador.registrar_paciente(nombre, edad, especialidad)
        messagebox.showinfo("Registro", msg)
        self.actualizar_visualizacion()

    def atender_paciente(self):
        paciente, msg = self.controlador.atender_paciente()
        messagebox.showinfo("Atención", msg)
        self.actualizar_visualizacion()

    def ver_siguiente(self):
        paciente, msg = self.controlador.ver_siguiente_paciente()
        messagebox.showinfo("Siguiente", msg)

    def limpiar_cola(self):
        msg = self.controlador.limpiar_turnos()
        messagebox.showinfo("Cola", msg)
        self.actualizar_visualizacion()

    def ver_estadisticas(self):
        stats = self.controlador.obtener_estadisticas_especialidad()
        ok, filepath, msg = self.graphviz.generate_statistics_graph(stats)
        if ok and os.path.exists(filepath):
            img = Image.open(filepath)
            img = img.resize((500, 300))
            self.stats_img = ImageTk.PhotoImage(img)
            self.stats_canvas.config(image=self.stats_img)

    def actualizar_visualizacion(self):
        pacientes = self.controlador.obtener_lista_pacientes()
        if not pacientes:
            self.label_info.config(text="Cola vacía")
        else:
            tiempo_total = self.controlador.obtener_estado_cola()["tiempo_total_estimado"]
            self.label_info.config(text=f"Pacientes en cola: {len(pacientes)} | Tiempo total estimado: {tiempo_total} min")

        ok, filepath, msg = self.graphviz.generate_queue_graph(pacientes)
        if ok and os.path.exists(filepath):
            img = Image.open(filepath)
            img = img.resize((600, 350))
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.config(image=self.tk_img)


def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
