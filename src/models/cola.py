from models.nodo import Nodo


class ColaPacientes:
    def __init__(self):
        self.primero = None  # Frente de la cola (próximo a atender)
        self.ultimo = None   # Final de la cola (último en llegar)

    def esta_vacia(self):
        return self.primero is None

    def encolar(self, paciente):
        nuevo_nodo = Nodo(paciente)

        if self.esta_vacia():
            self.primero = nuevo_nodo  # Primer paciente en la cola
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.establecer_siguiente(nuevo_nodo)  # Conecto al final
            self.ultimo = nuevo_nodo  # Actualizo el último nodo

        self._actualizar_tiempos_espera()

    def desencolar(self):
        if self.esta_vacia():
            return None

        paciente_atendido = self.primero.obtener_info()  # Guardar el paciente a atender
        self.primero = self.primero.obtener_siguiente()  # Mover el frente de la cola

        if self.primero is None:
            self.ultimo = None

        self._actualizar_tiempos_espera()

        return paciente_atendido

    def ver_primero(self):
        if self.esta_vacia():
            return None
        return self.primero.obtener_info()

    def tamano(self):
        actual = self.primero
        contador = 0
        while actual is not None:
            contador += 1
            actual = actual.obtener_siguiente()
        return contador

    def buscar(self, nombre_paciente):
        actual = self.primero
        while actual is not None:
            if actual.obtener_info().es_igual_a_llave(nombre_paciente):
                return True
            actual = actual.obtener_siguiente()
        return False

    def obtener_posicion_paciente(self, nombre_paciente):
        actual = self.primero
        posicion = 1
        while actual is not None:
            if actual.obtener_info().es_igual_a_llave(nombre_paciente):
                return posicion
            actual = actual.obtener_siguiente()
            posicion += 1
        return -1

    def _actualizar_tiempos_espera(self):
        actual = self.primero
        tiempo_acumulado = 0

        while actual is not None:
            paciente = actual.obtener_info()
            paciente.establecer_tiempo_espera_estimado(tiempo_acumulado)
            tiempo_acumulado += paciente.obtener_tiempo_atencion()
            actual = actual.obtener_siguiente()

    def obtener_tiempo_total_estimado(self):
        actual = self.primero
        tiempo_total = 0
        while actual is not None:
            tiempo_total += actual.obtener_info().obtener_tiempo_atencion()
            actual = actual.obtener_siguiente()
        return tiempo_total

    def a_lista(self):
        lista_pacientes = []
        actual = self.primero
        while actual is not None:
            lista_pacientes.append(actual.obtener_info())
            actual = actual.obtener_siguiente()
        return lista_pacientes

    def limpiar(self):
        self.primero = None
        self.ultimo = None
