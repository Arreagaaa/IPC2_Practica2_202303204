# -*- coding: utf-8 -*-
"""
Implementación de Cola Dinámica para el Sistema de Turnos Médicos
Basada en la plantilla proporcionada y adaptada para pacientes
"""

from models.nodo import Nodo

class ColaPacientes:
    """Cola dinámica para gestionar turnos de pacientes"""

    def __init__(self):
        self.primero = None  # Frente de la cola (próximo a atender)
        self.ultimo = None   # Final de la cola (último en llegar)

    def esta_vacia(self):
        """Verifica si la cola está vacía"""
        return self.primero is None

    def encolar(self, paciente):
        """
        Agrega un paciente al final de la cola

        Args:
            paciente (Paciente): Paciente a agregar
        """
        nuevo_nodo = Nodo(paciente)

        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.establecer_siguiente(nuevo_nodo)
            self.ultimo = nuevo_nodo

        self._actualizar_tiempos_espera()

    def desencolar(self):
        """
        Remueve y retorna el primer paciente de la cola

        Returns:
            Paciente: Paciente atendido o None si la cola está vacía
        """
        if self.esta_vacia():
            return None

        paciente_atendido = self.primero.obtener_info()
        self.primero = self.primero.obtener_siguiente()

        if self.primero is None:
            self.ultimo = None

        self._actualizar_tiempos_espera()

        return paciente_atendido

    def ver_primero(self):
        """Retorna el primer paciente sin removerlo de la cola"""
        if self.esta_vacia():
            return None
        return self.primero.obtener_info()

    def tamano(self):
        """Calcula el tamaño de la cola"""
        actual = self.primero
        contador = 0
        while actual is not None:
            contador += 1
            actual = actual.obtener_siguiente()
        return contador

    def buscar(self, nombre_paciente):
        """Busca un paciente por nombre"""
        actual = self.primero
        while actual is not None:
            if actual.obtener_info().es_igual_a_llave(nombre_paciente):
                return True
            actual = actual.obtener_siguiente()
        return False

    def obtener_posicion_paciente(self, nombre_paciente):
        """Obtiene la posición de un paciente en la cola"""
        actual = self.primero
        posicion = 1
        while actual is not None:
            if actual.obtener_info().es_igual_a_llave(nombre_paciente):
                return posicion
            actual = actual.obtener_siguiente()
            posicion += 1
        return -1

    def _actualizar_tiempos_espera(self):
        """Actualiza los tiempos de espera estimados para todos los pacientes"""
        actual = self.primero
        tiempo_acumulado = 0

        while actual is not None:
            paciente = actual.obtener_info()
            paciente.establecer_tiempo_espera_estimado(tiempo_acumulado)
            tiempo_acumulado += paciente.obtener_tiempo_atencion()
            actual = actual.obtener_siguiente()

    def obtener_tiempo_total_estimado(self):
        """Calcula el tiempo total estimado para atender a todos los pacientes"""
        actual = self.primero
        tiempo_total = 0
        while actual is not None:
            tiempo_total += actual.obtener_info().obtener_tiempo_atencion()
            actual = actual.obtener_siguiente()
        return tiempo_total

    def a_lista(self):
        """Convierte la cola a una lista para facilitar la visualización"""
        lista_pacientes = []
        actual = self.primero
        while actual is not None:
            lista_pacientes.append(actual.obtener_info())
            actual = actual.obtener_siguiente()
        return lista_pacientes

    def limpiar(self):
        """Limpia toda la cola"""
        self.primero = None
        self.ultimo = None