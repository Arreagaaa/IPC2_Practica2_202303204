class Paciente:
    def __init__(self, nombre, edad, especialidad):
        self.nombre = nombre
        self.edad = edad
        self.especialidad = especialidad
        self.tiempo_atencion = self.TIEMPOS_ESPECIALIDAD.get(especialidad, 10)
        self.tiempo_registro = None
        self.tiempo_espera_estimado = 0

    TIEMPOS_ESPECIALIDAD = {
        "Medicina General": 10,
        "Pediatría": 15,
        "Ginecología": 20,
        "Dermatología": 25
    }

    def obtener_tiempo_atencion(self):
        return self.tiempo_atencion

    def establecer_tiempo_espera_estimado(self, tiempo_espera):
        self.tiempo_espera_estimado = tiempo_espera

    def obtener_tiempo_total_estimado(self):
        return self.tiempo_espera_estimado + self.tiempo_atencion

    def mostrar(self):
        print(f"Paciente: {self.nombre}")
        print(f"Edad: {self.edad} años")
        print(f"Especialidad: {self.especialidad}")
        print(f"Tiempo de atención: {self.tiempo_atencion} minutos")
        print(
            f"Tiempo estimado de espera: {self.tiempo_espera_estimado} minutos")
        print(
            f"Tiempo total estimado: {self.obtener_tiempo_total_estimado()} minutos")
        print("-" * 50)

    def es_igual_a_llave(self, nombre):
        return self.nombre.lower() == nombre.lower()

    def __str__(self):
        return f"{self.nombre} ({self.edad} años) - {self.especialidad}"

    def a_diccionario(self):
        return {
            'nombre': self.nombre,
            'edad': self.edad,
            'especialidad': self.especialidad,
            'tiempo_atencion': self.tiempo_atencion,
            'tiempo_espera_estimado': self.tiempo_espera_estimado
        }
