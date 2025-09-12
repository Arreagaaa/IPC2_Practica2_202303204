import datetime
from models.cola import ColaPacientes
from models.paciente import Paciente


class ControladorTurnos:
    def __init__(self):
        self.cola = ColaPacientes()
        self.pacientes_atendidos = []  # Lista de pacientes ya atendidos
        self.total_pacientes_atendidos = 0

    def registrar_paciente(self, nombre, edad, especialidad):
        try:
            if not nombre or not nombre.strip():
                return False, "El nombre del paciente no puede estar vacío"

            if not isinstance(edad, int) or edad < 0 or edad > 120:
                return False, "La edad debe ser un número válido entre 0 y 120"

            if especialidad not in Paciente.TIEMPOS_ESPECIALIDAD:
                return False, f"Especialidad no válida. Opciones: {list(Paciente.TIEMPOS_ESPECIALIDAD.keys())}"

            if self.cola.buscar(nombre.strip()):
                return False, f"El paciente {nombre.strip()} ya está registrado en la cola"

            paciente = Paciente(nombre.strip(), edad, especialidad)
            paciente.tiempo_registro = datetime.datetime.now()
            self.cola.encolar(paciente)

            return True, f"Paciente {nombre.strip()} registrado exitosamente. Posición en cola: {self.cola.tamano()}"

        except Exception as e:
            return False, f"Error al registrar paciente: {str(e)}"

    def atender_paciente(self):
        try:
            if self.cola.esta_vacia():
                return None, "No hay pacientes en espera"

            paciente = self.cola.desencolar()
            paciente.tiempo_atencion_actual = datetime.datetime.now()

            self.pacientes_atendidos.append(paciente)
            self.total_pacientes_atendidos += 1

            mensaje = f"Atendiendo a: {paciente.nombre}\n"
            mensaje += f"Edad: {paciente.edad} años\n"
            mensaje += f"Especialidad: {paciente.especialidad}\n"
            mensaje += f"Tiempo de atención: {paciente.tiempo_atencion} minutos"

            return paciente, mensaje

        except Exception as e:
            return None, f"Error al atender paciente: {str(e)}"

    def ver_siguiente_paciente(self):
        siguiente_paciente = self.cola.ver_primero()
        if siguiente_paciente is None:
            return None, "No hay pacientes en espera"

        mensaje = f"Próximo paciente: {siguiente_paciente.nombre}\n"
        mensaje += f"Edad: {siguiente_paciente.edad} años\n"
        mensaje += f"Especialidad: {siguiente_paciente.especialidad}\n"
        mensaje += f"Tiempo estimado de atención: {siguiente_paciente.tiempo_atencion} minutos"

        return siguiente_paciente, mensaje

    def obtener_estado_cola(self):
        return {
            'total_pacientes': self.cola.tamano(),
            'esta_vacia': self.cola.esta_vacia(),
            'tiempo_total_estimado': self.cola.obtener_tiempo_total_estimado(),
            'pacientes_atendidos_hoy': self.total_pacientes_atendidos,
            'siguiente_paciente': self.cola.ver_primero()
        }

    def obtener_posicion_paciente(self, nombre_paciente):
        posicion = self.cola.obtener_posicion_paciente(nombre_paciente)
        if posicion == -1:
            return -1, f"El paciente {nombre_paciente} no está en la cola"

        return posicion, f"El paciente {nombre_paciente} está en la posición {posicion} de la cola"

    def obtener_lista_pacientes(self):
        return self.cola.a_lista()

    def limpiar_turnos(self):
        cantidad_pacientes = self.cola.tamano()
        self.cola.limpiar()
        return f"Cola limpiada. Se removieron {cantidad_pacientes} pacientes"

    def obtener_estadisticas_especialidad(self):
        estadisticas = {
            especialidad: 0 for especialidad in Paciente.TIEMPOS_ESPECIALIDAD.keys()}

        pacientes = self.obtener_lista_pacientes()
        for paciente in pacientes:
            estadisticas[paciente.especialidad] += 1

        return estadisticas

    def validar_especialidad(self, especialidad):
        return especialidad in Paciente.TIEMPOS_ESPECIALIDAD

    def obtener_especialidades_disponibles(self):
        return list(Paciente.TIEMPOS_ESPECIALIDAD.keys())
