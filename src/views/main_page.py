# -*- coding: utf-8 -*-
"""
Interfaz gráfica principal para el Sistema de Turnos Médicos
Implementada con Tkinter
"""

from controllers.turnos import ControladorTurnos
from utils.graphviz_generator import generar_grafica_cola
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import sys

# Agregar el directorio raíz al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MainWindow:
    """Ventana principal del sistema de turnos médicos"""

    def __init__(self):
        self.controller = ControladorTurnos()

        # Configuración de la ventana principal
        self.root = tk.Tk()
        self.root.title("Sistema de Turnos Médicos - Clínica San Carlos")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)

        # Variables de Tkinter
        self.patient_name = tk.StringVar()
        self.patient_age = tk.StringVar()
        self.selected_specialty = tk.StringVar()

        # Configurar estilo
        self.setup_styles()

        # Crear interfaz
        self.create_widgets()

        # Actualizar información inicial
        self.refresh_queue_display()

    def setup_styles(self):
        """Configura los estilos de la aplicación"""
        self.root.configure(bg='#f0f0f0')

        # Estilo para ttk
        style = ttk.Style()
        style.theme_use('clam')

    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""

        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = tk.Label(
            main_frame, text="Sistema de Turnos Médicos", bg='#f0f0f0', font=("Helvetica", 16))
        title_label.pack(pady=10)

        # Frame para datos del paciente
        patient_frame = tk.LabelFrame(
            main_frame, text="Datos del Paciente", bg='#f0f0f0')
        patient_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(patient_frame, text="Nombre:", bg='#f0f0f0').grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Entry(patient_frame, textvariable=self.patient_name).grid(
            row=0, column=1, padx=5, pady=5)

        tk.Label(patient_frame, text="Edad:", bg='#f0f0f0').grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Entry(patient_frame, textvariable=self.patient_age).grid(
            row=1, column=1, padx=5, pady=5)

        # Especialidad
        tk.Label(patient_frame, text="Especialidad:", bg='#f0f0f0').grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)
        specialty_combobox = ttk.Combobox(
            patient_frame, textvariable=self.selected_specialty, state="readonly")
        specialty_combobox['values'] = (
            "Medicina General", "Pediatría", "Ginecología", "Dermatología")
        specialty_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Frame para botones
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        register_button = tk.Button(
            button_frame, text="Registrar Paciente", command=self.register_patient)
        register_button.pack(side=tk.LEFT, padx=5, pady=5)

        attend_button = tk.Button(
            button_frame, text="Atender Paciente", command=self.attend_patient)
        attend_button.pack(side=tk.LEFT, padx=5, pady=5)

        next_button = tk.Button(
            button_frame, text="Ver Siguiente Paciente", command=self.show_next_patient)
        next_button.pack(side=tk.LEFT, padx=5, pady=5)

        search_button = tk.Button(
            button_frame, text="Buscar Paciente", command=self.search_patient)
        search_button.pack(side=tk.LEFT, padx=5, pady=5)

        list_button = tk.Button(
            button_frame, text="Ver Lista de Pacientes", command=self.show_patient_list)
        list_button.pack(side=tk.LEFT, padx=5, pady=5)

        graph_button = tk.Button(
            button_frame, text="Generar Gráfica de Cola", command=self.generate_queue_graph)
        graph_button.pack(side=tk.LEFT, padx=5, pady=5)

        clear_button = tk.Button(
            button_frame, text="Limpiar Turnos", command=self.clear_turns)
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        exit_button = tk.Button(
            button_frame, text="Salir", command=self.root.quit)
        exit_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame para mostrar la cola de pacientes
        self.queue_frame = tk.LabelFrame(
            main_frame, text="Cola de Pacientes", bg='#f0f0f0')
        self.queue_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Texto con desplazamiento para mostrar la cola
        self.queue_text = scrolledtext.ScrolledText(
            self.queue_frame, state='disabled', wrap=tk.WORD, bg='#ffffff')
        self.queue_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Cargar imagen
        self.load_image()

    def load_image(self):
        """Carga y muestra una imagen en la interfaz"""
        try:
            image_path = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), "assets", "logo.png")
            image = Image.open(image_path)
            image = image.resize((200, 100), Image.ANTIALIAS)
            self.logo_image = ImageTk.PhotoImage(image)

            label = tk.Label(self.root, image=self.logo_image, bg='#f0f0f0')
            label.image = self.logo_image  # Guardar referencia de la imagen
            label.pack(pady=10)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def register_patient(self):
        """Registra un nuevo paciente en el sistema"""
        name = self.patient_name.get()
        age = self.patient_age.get()
        specialty = self.selected_specialty.get()

        if not name or not age or not specialty:
            messagebox.showwarning(
                "Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            age = int(age)
            self.controller.registrar_paciente(name, age, specialty)
            messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
            self.clear_patient_fields()
            self.refresh_queue_display()
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero.")

    def attend_patient(self):
        """Atiende al siguiente paciente en la cola"""
        patient = self.controller.atender_paciente()
        if patient:
            messagebox.showinfo("Paciente Atendido",
                                f"Paciente atendido: {patient.nombre}")
        else:
            messagebox.showinfo("Información", "No hay pacientes en la cola.")
        self.refresh_queue_display()

    def show_next_patient(self):
        """Muestra información del siguiente paciente sin atenderlo"""
        patient = self.controller.ver_siguiente_paciente()
        if patient:
            messagebox.showinfo("Siguiente Paciente",
                                f"Siguiente paciente: {patient.nombre}")
        else:
            messagebox.showinfo("Información", "No hay pacientes en la cola.")

    def search_patient(self):
        """Busca un paciente por nombre y muestra su posición en la cola"""
        name = self.patient_name.get()
        if not name:
            messagebox.showwarning(
                "Advertencia", "Ingrese el nombre del paciente a buscar.")
            return

        found = self.controller.buscar_paciente(name)
        if found:
            position = self.controller.obtener_posicion_paciente(name)
            messagebox.showinfo(
                "Paciente Encontrado", f"Paciente encontrado en la posición {position} de la cola.")
        else:
            messagebox.showinfo(
                "No Encontrado", "Paciente no encontrado en la cola.")

    def show_patient_list(self):
        """Muestra la lista de pacientes en la cola"""
        patients = self.controller.obtener_lista_pacientes()
        if patients:
            patient_list = "\n".join(
                [f"{p.nombre} - {p.edad} años - {p.especialidad}" for p in patients])
            messagebox.showinfo("Lista de Pacientes",
                                f"Pacientes en la cola:\n{patient_list}")
        else:
            messagebox.showinfo("Lista de Pacientes",
                                "No hay pacientes en la cola.")

    def generate_queue_graph(self):
        """Genera una gráfica de la cola de pacientes"""
        try:
            generar_grafica_cola(self.controller.cola)
            messagebox.showinfo("Gráfica Generada",
                                "Gráfica de la cola generada exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar la gráfica: {e}")

    def clear_turns(self):
        """Limpia la cola de turnos"""
        self.controller.limpiar_turnos()
        messagebox.showinfo(
            "Cola Limpiada", "Cola de turnos limpiada correctamente.")
        self.refresh_queue_display()

    def clear_patient_fields(self):
        """Limpia los campos de entrada de paciente"""
        self.patient_name.set("")
        self.patient_age.set("")
        self.selected_specialty.set("")

    def refresh_queue_display(self):
        """Actualiza la visualización de la cola de pacientes"""
        self.queue_text.configure(state='normal')
        self.queue_text.delete(1.0, tk.END)

        patients = self.controller.obtener_lista_pacientes()
        if patients:
            for patient in patients:
                self.queue_text.insert(
                    tk.END, f"{patient.nombre} - {patient.edad} años - {patient.especialidad}\n")
        else:
            self.queue_text.insert(tk.END, "No hay pacientes en la cola.")

        self.queue_text.configure(state='disabled')

    def run(self):
        """Inicia el bucle principal de la aplicación"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()

from controllers.turnos import ControladorTurnos
from utils.graphviz_generator import generar_grafica_cola

def mostrar_menu():
    print("=== Sistema de Turnos Médicos ===")
    print("1. Registrar paciente")
    print("2. Atender paciente")
    print("3. Ver siguiente paciente")
    print("4. Buscar paciente")
    print("5. Ver lista de pacientes")
    print("6. Generar gráfica de la cola")
    print("7. Limpiar turnos")
    print("8. Salir")

def main():
    controlador = ControladorTurnos()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del paciente: ")
            edad = int(input("Edad: "))
            print("Especialidades disponibles:")
            print("- Medicina General")
            print("- Pediatría")
            print("- Ginecología")
            print("- Dermatología")
            especialidad = input("Especialidad: ")
            controlador.registrar_paciente(nombre, edad, especialidad)
            print("Paciente registrado correctamente.\n")

        elif opcion == "2":
            paciente = controlador.atender_paciente()
            if paciente:
                print(f"Paciente atendido: {paciente}")
            else:
                print("No hay pacientes en la cola.\n")

        elif opcion == "3":
            paciente = controlador.ver_siguiente_paciente()
            if paciente:
                print(f"Siguiente paciente: {paciente}")
            else:
                print("No hay pacientes en la cola.\n")

        elif opcion == "4":
            nombre = input("Nombre del paciente a buscar: ")
            encontrado = controlador.buscar_paciente(nombre)
            if encontrado:
                posicion = controlador.obtener_posicion_paciente(nombre)
                print(f"Paciente encontrado en la posición {posicion} de la cola.\n")
            else:
                print("Paciente no encontrado.\n")

        elif opcion == "5":
            lista = controlador.obtener_lista_pacientes()
            if lista:
                print("\nPacientes en la cola:")
                for paciente in lista:
                    paciente.mostrar()
            else:
                print("No hay pacientes en la cola.\n")

        elif opcion == "6":
            generar_grafica_cola(controlador.cola)
            print("Gráfica generada.\n")

        elif opcion == "7":
            controlador.limpiar_turnos()
            print("Cola de turnos limpiada.\n")

        elif opcion == "8":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intente de nuevo.\n")

# Make sure to export the main function
__all__ = ['main']
