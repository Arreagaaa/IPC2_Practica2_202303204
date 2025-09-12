# -*- coding: utf-8 -*-
"""
Generador de visualizaciones con Graphviz para el Sistema de Turnos Médicos
"""

try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Graphviz no está instalado. Para instalarlo ejecute: pip install graphviz")

import os
import tempfile
from models.cola import ColaPacientes


class GraphvizGenerator:
    """Generador de gráficos para visualizar la cola de pacientes"""

    def __init__(self):
        self.available = GRAPHVIZ_AVAILABLE
        self.output_dir = tempfile.gettempdir()

    def is_available(self):
        """Verifica si Graphviz está disponible"""
        return self.available

    def generate_queue_graph(self, patients_list, filename='queue_visualization'):
        """
        Genera un gráfico de la cola de pacientes

        Args:
            patients_list (list): Lista de pacientes en la cola
            filename (str): Nombre del archivo de salida

        Returns:
            tuple: (success: bool, filepath: str, message: str)
        """
        if not self.available:
            return False, "", "Graphviz no está disponible"

        try:
            # Crear el gráfico
            dot = graphviz.Digraph(comment='Cola de Pacientes')
            dot.attr(rankdir='TB')  # Top to Bottom
            dot.attr('node', shape='box', style='filled')
            dot.attr('graph', bgcolor='white')

            if not patients_list:
                # Cola vacía
                dot.node('empty', 'COLA VACÍA\n\nNo hay pacientes\nen espera',
                         fillcolor='lightgray', fontcolor='black')

                # Información adicional
                dot.node('info', 'Estado: Sin pacientes\nTiempo total: 0 min',
                         shape='note', fillcolor='lightyellow')

            else:
                # Nodo de cabecera
                header_text = f'SISTEMA DE TURNOS MÉDICOS\\n'
                header_text += f'Pacientes en cola: {len(patients_list)}\\n'
                header_text += f'Tiempo total estimado: {sum(p.get_attention_time() for p in patients_list)} min'

                dot.node('header', header_text,
                         shape='box', fillcolor='lightblue', fontsize='12', fontcolor='black')

                # Crear nodos para cada paciente
                for i, patient in enumerate(patients_list):
                    node_id = f'patient_{i}'

                    # Determinar color según especialidad
                    colors = {
                        'Medicina General': 'lightgreen',
                        'Pediatría': 'lightcoral',
                        'Ginecología': 'lightpink',
                        'Dermatología': 'lightyellow'
                    }
                    color = colors.get(patient.specialty, 'lightgray')

                    # Contenido del nodo
                    label = f'Posición: {i+1}\\n'
                    label += f'Nombre: {patient.name}\\n'
                    label += f'Edad: {patient.age} años\\n'
                    label += f'Especialidad: {patient.specialty}\\n'
                    label += f'Tiempo atención: {patient.attention_time} min\\n'
                    label += f'Tiempo espera: {patient.estimated_wait_time} min\\n'
                    label += f'Tiempo total: {patient.get_total_estimated_time()} min'

                    dot.node(node_id, label, fillcolor=color, fontsize='10')

                    # Conectar nodos
                    if i == 0:
                        dot.edge('header', node_id, label='PRÓXIMO')
                    else:
                        dot.edge(f'patient_{i-1}', node_id, style='dashed')

                # Leyenda de colores
                with dot.subgraph(name='cluster_legend') as legend:
                    legend.attr(label='Leyenda de Especialidades',
                                fontsize='10')
                    legend.attr(style='dotted')
                    legend.node('leg_mg', 'Medicina General',
                                fillcolor='lightgreen', fontsize='8')
                    legend.node('leg_ped', 'Pediatría',
                                fillcolor='lightcoral', fontsize='8')
                    legend.node('leg_gin', 'Ginecología',
                                fillcolor='lightpink', fontsize='8')
                    legend.node('leg_der', 'Dermatología',
                                fillcolor='lightyellow', fontsize='8')

            # Guardar el archivo
            filepath = os.path.join(self.output_dir, filename)
            dot.render(filepath, format='png', cleanup=True)

            png_filepath = f"{filepath}.png"
            return True, png_filepath, f"Gráfico generado exitosamente en: {png_filepath}"

        except Exception as e:
            return False, "", f"Error al generar gráfico: {str(e)}"

    def generate_statistics_graph(self, specialty_stats, filename='specialty_stats'):
        """
        Genera un gráfico de barras con estadísticas por especialidad

        Args:
            specialty_stats (dict): Estadísticas por especialidad
            filename (str): Nombre del archivo

        Returns:
            tuple: (success: bool, filepath: str, message: str)
        """
        if not self.available:
            return False, "", "Graphviz no está disponible"

        try:
            dot = graphviz.Digraph(comment='Estadísticas por Especialidad')
            dot.attr(rankdir='TB')
            dot.attr('node', shape='box', style='filled')

            # Título
            dot.node('title', 'ESTADÍSTICAS POR ESPECIALIDAD',
                     shape='box', fillcolor='lightblue', fontsize='14')

            # Crear nodos para cada especialidad
            for specialty, count in specialty_stats.items():
                node_id = specialty.lower().replace(' ', '_')
                label = f'{specialty}\\nPacientes: {count}'

                # Color basado en la cantidad
                if count == 0:
                    color = 'lightgray'
                elif count <= 2:
                    color = 'lightgreen'
                elif count <= 4:
                    color = 'lightyellow'
                else:
                    color = 'lightcoral'

                dot.node(node_id, label, fillcolor=color)
                dot.edge('title', node_id, style='dotted')

            # Guardar archivo
            filepath = os.path.join(self.output_dir, filename)
            dot.render(filepath, format='png', cleanup=True)

            png_filepath = f"{filepath}.png"
            return True, png_filepath, f"Gráfico de estadísticas generado en: {png_filepath}"

        except Exception as e:
            return False, "", f"Error al generar gráfico de estadísticas: {str(e)}"

    def generate_simple_queue_representation(self, patients_list):
        """
        Genera una representación textual simple de la cola

        Args:
            patients_list (list): Lista de pacientes

        Returns:
            str: Representación textual de la cola
        """
        if not patients_list:
            return "COLA VACÍA: [ ]"

        representation = "COLA DE TURNOS: "
        representation += "[ "

        for i, patient in enumerate(patients_list):
            if i > 0:
                representation += " -> "
            representation += f"{patient.name}({patient.specialty})"

        representation += " ]"
        representation += f"\nTotal: {len(patients_list)} pacientes"
        representation += f" | Tiempo total: {sum(p.get_attention_time() for p in patients_list)} min"

        return representation

    def set_output_directory(self, directory):
        """
        Establece el directorio de salida para los gráficos

        Args:
            directory (str): Ruta del directorio
        """
        if os.path.exists(directory) and os.path.isdir(directory):
            self.output_dir = directory
            return True
        return False


def generar_grafica_cola(cola: ColaPacientes, nombre_archivo="cola_pacientes"):
    """
    Genera una gráfica de la cola de pacientes usando Graphviz
    """
    try:
        from graphviz import Digraph
    except ImportError:
        print("Graphviz no está instalado.")
        return

    dot = Digraph(comment="Cola de Pacientes")
    actual = cola.primero
    indice = 0

    while actual is not None:
        paciente = actual.obtener_info()
        etiqueta = f"{paciente.nombre}\n{paciente.especialidad}\n{paciente.tiempo_espera_estimado} min"
        dot.node(str(indice), etiqueta)
        if actual.obtener_siguiente() is not None:
            dot.edge(str(indice), str(indice + 1))
        actual = actual.obtener_siguiente()
        indice += 1

    dot.render(f"{nombre_archivo}.gv", view=False)
    print(f"Gráfica generada: {nombre_archivo}.gv.pdf")
