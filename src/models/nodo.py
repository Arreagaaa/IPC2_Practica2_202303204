# -*- coding: utf-8 -*-
"""
Modelo Nodo para la estructura de la Cola de Pacientes
"""

class Nodo:
    """Clase que representa un nodo en la cola"""

    def __init__(self, info):
        self.info = info
        self.siguiente = None

    def obtener_info(self):
        """Obtiene la información del nodo"""
        return self.info

    def obtener_siguiente(self):
        """Obtiene el siguiente nodo"""
        return self.siguiente

    def establecer_siguiente(self, nuevo_siguiente):
        """Establece el siguiente nodo"""
        self.siguiente = nuevo_siguiente