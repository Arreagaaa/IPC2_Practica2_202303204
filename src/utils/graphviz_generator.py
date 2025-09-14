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
    def __init__(self):
        self.available = GRAPHVIZ_AVAILABLE
        self.output_dir = tempfile.gettempdir()

    def is_available(self):
        return self.available

    def generate_queue_graph(self, patients_list, filename='queue_visualization'):
        if not self.available:
            return False, "", "Graphviz no está disponible"

        try:
            dot = graphviz.Digraph(comment='Cola de Pacientes')
            dot.attr(rankdir='TB')
            dot.attr('node', shape='box', style='filled')
            dot.attr('graph', bgcolor='white')

            if not patients_list:
                dot.node('empty', 'COLA VACÍA\\n\\nNo hay pacientes\\nen espera',
                         fillcolor='lightgray', fontcolor='black')
                dot.node('info', 'Estado: Sin pacientes\\nTiempo total: 0 min',
                         shape='note', fillcolor='lightyellow')
            else:
                header_text = f'SISTEMA DE TURNOS MÉDICOS\\n'
                header_text += f'Pacientes en cola: {len(patients_list)}\\n'
                header_text += f'Tiempo total estimado: {sum(p.obtener_tiempo_atencion() for p in patients_list)} min'

                dot.node('header', header_text, shape='box', fillcolor='lightblue',
                         fontsize='12', fontcolor='black')

                for i, patient in enumerate(patients_list):
                    node_id = f'patient_{i}'

                    colors = {
                        'Medicina General': 'lightgreen',
                        'Pediatría': 'lightcoral',
                        'Ginecología': 'lightpink',
                        'Dermatología': 'lightyellow'
                    }
                    color = colors.get(patient.especialidad, 'lightgray')

                    label = f'Posición: {i+1}\\n'
                    label += f'Nombre: {patient.nombre}\\n'
                    label += f'Edad: {patient.edad} años\\n'
                    label += f'Especialidad: {patient.especialidad}\\n'
                    label += f'Tiempo atención: {patient.tiempo_atencion} min\\n'
                    label += f'Tiempo espera: {patient.tiempo_espera_estimado} min\\n'
                    label += f'Tiempo total: {patient.obtener_tiempo_total_estimado()} min'

                    dot.node(node_id, label, fillcolor=color, fontsize='10')

                    if i == 0:
                        dot.edge('header', node_id, label='PRÓXIMO')
                    else:
                        dot.edge(f'patient_{i-1}', node_id, style='dashed')

            filepath = os.path.join(self.output_dir, filename)
            dot.render(filepath, format='png', cleanup=True)
            png_filepath = f"{filepath}.png"

            return True, png_filepath, f"Gráfico generado exitosamente en: {png_filepath}"

        except Exception as e:
            return False, "", f"Error al generar gráfico: {str(e)}"

    def generate_statistics_graph(self, specialty_stats, filename='specialty_stats'):

        if not self.available:
            return False, "", "Graphviz no está disponible"

        try:
            dot = graphviz.Digraph(comment='Estadísticas por Especialidad')
            dot.attr(rankdir='TB')
            dot.attr('node', shape='box', style='filled')

            dot.node('title', 'ESTADÍSTICAS POR ESPECIALIDAD',
                     shape='box', fillcolor='lightblue', fontsize='14')

            for specialty, count in specialty_stats.items():
                node_id = specialty.lower().replace(' ', '_').replace('í', 'i').replace('ó', 'o')
                label = f'{specialty}\\nPacientes: {count}'

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

            filepath = os.path.join(self.output_dir, filename)
            dot.render(filepath, format='png', cleanup=True)
            png_filepath = f"{filepath}.png"

            return True, png_filepath, f"Gráfico de estadísticas generado en: {png_filepath}"

        except Exception as e:
            return False, "", f"Error al generar gráfico de estadísticas: {str(e)}"

    def generate_simple_queue_representation(self, patients_list):
        if not patients_list:
            return "COLA VACÍA: [ ]"

        representation = "COLA DE TURNOS: "
        representation += "[ "
        for i, patient in enumerate(patients_list):
            if i > 0:
                representation += " -> "
            representation += f"{patient.nombre}({patient.especialidad})"
        representation += " ]"
        representation += f"\nTotal: {len(patients_list)} pacientes"
        representation += f" | Tiempo total: {sum(p.obtener_tiempo_atencion() for p in patients_list)} min"

        return representation

    def set_output_directory(self, directory):
        if os.path.exists(directory) and os.path.isdir(directory):
            self.output_dir = directory
            return True
        return False
