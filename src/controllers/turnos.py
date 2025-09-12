# -*- coding: utf-8 -*-
"""
Controlador para el Sistema de Turnos Médicos
Maneja la lógica de negocio entre la interfaz y los modelos
"""

import datetime
from models.cola import ColaPacientes
from models.paciente import Paciente


class ControladorTurnos:
    """Controlador para la gestión de turnos de pacientes"""

    def __init__(self):
        self.cola = ColaPacientes()
        self.pacientes_atendidos = []  # Lista de pacientes ya atendidos
        self.total_pacientes_atendidos = 0

    def registrar_paciente(self, nombre, edad, especialidad):
        """
        Registra un nuevo paciente en la cola

        Args:
            nombre (str): Nombre del paciente
            edad (int): Edad del paciente
            especialidad (str): Especialidad médica

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Validaciones
            if not nombre or not nombre.strip():
                return False, "El nombre del paciente no puede estar vacío"

            if not isinstance(edad, int) or edad < 0 or edad > 120:
                return False, "La edad debe ser un número válido entre 0 y 120"

            if especialidad not in Paciente.TIEMPOS_ESPECIALIDAD:
                return False, f"Especialidad no válida. Opciones: {list(Paciente.TIEMPOS_ESPECIALIDAD.keys())}"

            # Verificar si el paciente ya está en la cola
            if self.cola.buscar(nombre.strip()):
                return False, f"El paciente {nombre.strip()} ya está registrado en la cola"

            # Crear y registrar el paciente
            paciente = Paciente(nombre.strip(), edad, especialidad)
            paciente.tiempo_registro = datetime.datetime.now()
            self.cola.encolar(paciente)

            return True, f"Paciente {nombre.strip()} registrado exitosamente. Posición en cola: {self.cola.tamano()}"

        except Exception as e:
            return False, f"Error al registrar paciente: {str(e)}"

    def atender_paciente(self):
        """
        Atiende al próximo paciente en la cola

        Returns:
            tuple: (patient: Patient or None, message: str)
        """
        try:
            if self.cola.esta_vacia():
                return None, "No hay pacientes en espera"

            # Obtener y atender al próximo paciente
            paciente = self.cola.desencolar()
            paciente.tiempo_atencion_actual = datetime.datetime.now()

            # Agregar a la lista de pacientes atendidos
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
        """
        Obtiene información del próximo paciente sin atenderlo

        Returns:
            tuple: (patient: Patient or None, message: str)
        """
        siguiente_paciente = self.cola.ver_primero()
        if siguiente_paciente is None:
            return None, "No hay pacientes en espera"

        mensaje = f"Próximo paciente: {siguiente_paciente.nombre}\n"
        mensaje += f"Edad: {siguiente_paciente.edad} años\n"
        mensaje += f"Especialidad: {siguiente_paciente.especialidad}\n"
        mensaje += f"Tiempo estimado de atención: {siguiente_paciente.tiempo_atencion} minutos"

        return siguiente_paciente, mensaje

    def obtener_estado_cola(self):
        """
        Obtiene el estado actual de la cola

        Returns:
            dict: Información del estado de la cola
        """
        return {
            'total_pacientes': self.cola.tamano(),
            'esta_vacia': self.cola.esta_vacia(),
            'tiempo_total_estimado': self.cola.obtener_tiempo_total_estimado(),
            'pacientes_atendidos_hoy': self.total_pacientes_atendidos,
            'siguiente_paciente': self.cola.ver_primero()
        }

    def obtener_posicion_paciente(self, nombre_paciente):
        """
        Obtiene la posición de un paciente en la cola

        Args:
            nombre_paciente (str): Nombre del paciente

        Returns:
            tuple: (position: int, message: str)
        """
        posicion = self.cola.obtener_posicion_paciente(nombre_paciente)
        if posicion == -1:
            return -1, f"El paciente {nombre_paciente} no está en la cola"

        return posicion, f"El paciente {nombre_paciente} está en la posición {posicion} de la cola"

    def obtener_lista_pacientes(self):
        """
        Obtiene la lista completa de pacientes en la cola

        Returns:
            list: Lista de pacientes
        """
        return self.cola.a_lista()

    def limpiar_turnos(self):
        """
        Limpia toda la cola de pacientes

        Returns:
            str: Mensaje de confirmación
        """
        cantidad_pacientes = self.cola.tamano()
        self.cola.limpiar()
        return f"Cola limpiada. Se removieron {cantidad_pacientes} pacientes"

    def obtener_estadisticas_especialidad(self):
        """
        Obtiene estadísticas por especialidad

        Returns:
            dict: Estadísticas por especialidad
        """
        estadisticas = {
            especialidad: 0 for especialidad in Paciente.TIEMPOS_ESPECIALIDAD.keys()}

        pacientes = self.obtener_lista_pacientes()
        for paciente in pacientes:
            estadisticas[paciente.especialidad] += 1

        return estadisticas

    def validar_especialidad(self, especialidad):
        """
        Valida si una especialidad es válida

        Args:
            especialidad (str): Especialidad a validar

        Returns:
            bool: True si es válida
        """
        return especialidad in Paciente.TIEMPOS_ESPECIALIDAD

    def obtener_especialidades_disponibles(self):
        """
        Obtiene la lista de especialidades disponibles

        Returns:
            list: Lista de especialidades
        """
        return list(Paciente.TIEMPOS_ESPECIALIDAD.keys())
