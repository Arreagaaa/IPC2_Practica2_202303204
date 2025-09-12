# -*- coding: utf-8 -*-
"""
Modelo de Paciente para el Sistema de Turnos Médicos
"""

class Paciente:
    """Clase que representa un paciente en el sistema de turnos"""

    # Tiempos de atención por especialidad (en minutos)
    TIEMPOS_ESPECIALIDAD = {
        "Medicina General": 10,
        "Pediatría": 15,
        "Ginecología": 20,
        "Dermatología": 25
    }

    def __init__(self, nombre, edad, especialidad):
        """
        Inicializa un paciente

        Args:
            nombre (str): Nombre del paciente
            edad (int): Edad del paciente
            especialidad (str): Especialidad médica requerida
        """
        self.nombre = nombre
        self.edad = edad
        self.especialidad = especialidad
        self.tiempo_atencion = self.TIEMPOS_ESPECIALIDAD.get(especialidad, 10)
        self.tiempo_registro = None
        self.tiempo_espera_estimado = 0

    def obtener_tiempo_atencion(self):
        """Retorna el tiempo de atención según la especialidad"""
        return self.tiempo_atencion

    def establecer_tiempo_espera_estimado(self, tiempo_espera):
        """Establece el tiempo estimado de espera"""
        self.tiempo_espera_estimado = tiempo_espera

    def obtener_tiempo_total_estimado(self):
        """Retorna el tiempo total estimado (espera + atención)"""
        return self.tiempo_espera_estimado + self.tiempo_atencion

    def mostrar(self):
        """Muestra la información del paciente"""
        print(f"Paciente: {self.nombre}")
        print(f"Edad: {self.edad} años")
        print(f"Especialidad: {self.especialidad}")
        print(f"Tiempo de atención: {self.tiempo_atencion} minutos")
        print(f"Tiempo estimado de espera: {self.tiempo_espera_estimado} minutos")
        print(f"Tiempo total estimado: {self.obtener_tiempo_total_estimado()} minutos")
        print("-" * 50)

    def es_igual_a_llave(self, nombre):
        """Compara si el nombre coincide con la llave buscada"""
        return self.nombre.lower() == nombre.lower()

    def __str__(self):
        """Representación en cadena del paciente"""
        return f"{self.nombre} ({self.edad} años) - {self.especialidad}"

    def a_diccionario(self):
        """Convierte el paciente a diccionario para serialización"""
        return {
            'nombre': self.nombre,
            'edad': self.edad,
            'especialidad': self.especialidad,
            'tiempo_atencion': self.tiempo_atencion,
            'tiempo_espera_estimado': self.tiempo_espera_estimado
        }