class Nodo:
    def __init__(self, info):
        self.info = info
        self.siguiente = None

    def obtener_info(self):
        return self.info

    def obtener_siguiente(self):
        return self.siguiente

    def establecer_siguiente(self, nuevo_siguiente):
        self.siguiente = nuevo_siguiente
