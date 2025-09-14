# 🏥 Sistema de Gestión de Turnos Médicos

## 📋 Descripción del Proyecto

Sistema digitalizado para la gestión de turnos en una clínica médica que implementa una cola FIFO (First In, First Out) para administrar el orden de atención de los pacientes. La aplicación utiliza una interfaz gráfica moderna desarrollada en Tkinter y visualización de datos con Graphviz.

## 🎯 Competencias Desarrolladas

- ✅ Aplicación de estructuras de datos dinámicas en Python
- ✅ Implementación de colas para la gestión de turnos de atención
- ✅ Desarrollo de interfaces gráficas con Tkinter
- ✅ Visualización de estructuras de datos con Graphviz

## 🎯 Objetivos

### General
Aplicar el uso de estructuras de datos dinámicas en Python, implementando colas para gestionar los turnos de atención en una clínica médica con una interfaz gráfica interactiva.

### Específicos
- ✅ Usar estructuras de datos dinámicas para gestionar la cola de turnos de pacientes
- ✅ Implementar una interfaz gráfica con Tkinter para interactuar con el sistema de turnos
- ✅ Aplicar el concepto de cola (FIFO) para administrar el orden de atención
- ✅ Utilizar Graphviz para representar visualmente la estructura de la cola de pacientes

## ⚕️ Especialidades Médicas y Tiempos de Atención

| Especialidad | Tiempo Estimado |
|-------------|----------------|
| Medicina General | 10 minutos |
| Pediatría | 15 minutos |
| Ginecología | 20 minutos |
| Dermatología | 25 minutos |

## 🚀 Características del Sistema

### Funcionalidades Principales
- 📝 **Registro de pacientes** con nombre, edad y especialidad
- 👀 **Visualización en tiempo real** de la cola de turnos
- 👨‍⚕️ **Atención de pacientes** siguiendo orden FIFO
- ⏱️ **Cálculo automático** de tiempos de espera y atención
- 🔍 **Búsqueda de pacientes** en la cola
- 📊 **Estadísticas** por especialidad médica
- 🎨 **Visualización gráfica** con Graphviz
- 🧹 **Gestión completa** de la cola (limpiar, ver siguiente, etc.)

### Funciones Avanzadas
- 🔄 **Actualización automática** de la interfaz
- 📈 **Representación visual** de la estructura de datos
- 💾 **Historial** de pacientes atendidos
- ⚡ **Interfaz moderna** y responsiva
- 🛡️ **Validación robusta** de datos de entrada

## 📁 Estructura del Proyecto

```
IPC2_Practica2_202303204/
├── src/
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── controllers/
│   │   └── turnos.py          # Controlador de lógica de negocio
│   ├── models/
│   │   ├── cola.py            # Implementación de la estructura Cola
│   │   ├── nodo.py            # Clase Nodo para la lista enlazada
│   │   └── paciente.py        # Modelo de datos del Paciente
│   ├── views/
│   │   └── main_page.py       # Interfaz gráfica principal
│   ├── utils/
│   │   └── graphviz_generator.py # Generador de visualizaciones
│   └── graficas/              # Directorio para archivos generados
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación del proyecto
```

## 🛠️ Instalación y Configuración

### Requisitos Previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

1. **Instalar paquetes Python requeridos:**
```bash
pip install -r requirements.txt
```

2. **Instalar Graphviz (sistema):**

   **En Windows:**
   - Descargar desde: https://graphviz.org/download/
   - Agregar al PATH del sistema

   **En Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get install graphviz
   ```

   **En macOS:**
   ```bash
   brew install graphviz
   ```

## ▶️ Ejecución de la Aplicación

### Desde la línea de comandos:
```bash
cd src
python main.py
```

### Desde un IDE:
Ejecutar el archivo `src/main.py`

## 📖 Manual de Usuario

### 1. Registro de Pacientes
- Ingresar nombre completo del paciente
- Especificar edad (número válido entre 0-120)
- Seleccionar especialidad médica del dropdown
- Hacer clic en "➕ Registrar Paciente"

### 2. Gestión de Turnos
- **Atender Paciente**: Procesa al siguiente paciente en la cola
- **Ver Siguiente**: Muestra información del próximo paciente sin atenderlo
- **Buscar Paciente**: Localiza un paciente específico en la cola
- **Limpiar Cola**: Remueve todos los pacientes de la cola

### 3. Visualización
- **Panel de Estado**: Muestra información detallada de la cola actual
- **Visualización Graphviz**: Representación gráfica en tiempo real
- **Estadísticas**: Gráficos por especialidad médica
- **Actualización Automática**: Refresco cada 5 segundos

## 🏗️ Arquitectura del Sistema

### Patrón de Diseño: MVC (Model-View-Controller)

**Models** (`models/`):
- `Cola`: Implementación de estructura de datos cola con operaciones FIFO
- `Nodo`: Elemento individual de la lista enlazada
- `Paciente`: Entidad que representa a un paciente con sus atributos

**Views** (`views/`):
- `main_page.py`: Interfaz gráfica principal desarrollada en Tkinter

**Controllers** (`controllers/`):
- `turnos.py`: Lógica de negocio para la gestión de turnos

**Utils** (`utils/`):
- `graphviz_generator.py`: Utilidad para generar visualizaciones

## 🔧 Detalles Técnicos

### Estructura de Datos: Cola (Queue)
- **Implementación**: Lista enlazada simple
- **Operaciones principales**:
  - `encolar()`: Agrega paciente al final (O(1))
  - `desencolar()`: Remueve paciente del frente (O(1))
  - `ver_primero()`: Consulta sin remover (O(1))
  - `buscar()`: Búsqueda por nombre (O(n))

### Cálculo de Tiempos
- **Tiempo de espera**: Suma de tiempos de atención de pacientes anteriores
- **Tiempo total**: Tiempo de espera + tiempo de atención propia
- **Actualización**: Automática cuando se modifica la cola

### Validaciones Implementadas
- ✅ Nombres no vacíos y únicos en la cola
- ✅ Edades válidas (0-120 años)
- ✅ Especialidades dentro del catálogo disponible
- ✅ Prevención de duplicados en la cola

## 🎨 Interfaz de Usuario

### Diseño Visual
- **Tema**: Moderno con esquema de colores médicos
- **Tipografía**: Segoe UI para mejor legibilidad
- **Iconos**: Emojis para mayor claridad visual
- **Layout**: Distribución responsiva en paneles

### Componentes Principales
- **Panel de Registro**: Formulario para nuevos pacientes
- **Panel de Gestión**: Botones de control del sistema
- **Panel de Estado**: Información detallada de la cola
- **Panel de Visualización**: Gráficos de Graphviz
- **Panel de Estadísticas**: Métricas por especialidad

## 📊 Características de la Visualización

### Graphviz Integration
- **Cola de Turnos**: Representación visual de la estructura FIFO
- **Colores por Especialidad**: Diferenciación visual clara
- **Información Completa**: Todos los datos del paciente visibles
- **Leyenda**: Explicación de colores y símbolos
- **Actualización en Tiempo Real**: Sincronización automática

### Estadísticas
- **Gráficos de Barras**: Distribución por especialidad
- **Métricas en Tiempo Real**: Contadores dinámicos
- **Exportación**: Imágenes PNG para reportes

## 🧪 Testing y Validación

### Casos de Prueba Recomendados
1. **Registro de múltiples pacientes** con diferentes especialidades
2. **Atención secuencial** verificando orden FIFO
3. **Búsqueda de pacientes** existentes y no existentes
4. **Validación de entradas** incorrectas (nombres vacíos, edades inválidas)
5. **Gestión de cola vacía** (atender sin pacientes)
6. **Carga de trabajo** con muchos pacientes
7. **Limpieza de cola** y regeneración

## 📚 Conceptos Técnicos Aplicados

### Estructuras de Datos
- **Cola (Queue)**: FIFO para orden de atención
- **Lista Enlazada**: Implementación dinámica de la cola
- **Nodos**: Elementos individuales con enlaces

### Programación Orientada a Objetos
- **Encapsulamiento**: Datos y métodos en clases
- **Abstracción**: Interfaces claras entre componentes
- **Modularidad**: Separación de responsabilidades

### Interfaces Gráficas
- **Tkinter**: Framework nativo de Python
- **Event-driven**: Programación basada en eventos
- **Threading**: Actualización no bloqueante

## 🔮 Posibles Extensiones

### Funcionalidades Adicionales
- 💾 **Persistencia de datos** en base de datos
- 📧 **Notificaciones** por email/SMS
- 🕒 **Citas programadas** con fechas específicas
- 👥 **Sistema multiusuario** con roles
- 📱 **Aplicación móvil** complementaria
- 🏥 **Múltiples consultorios** simultáneos
- 📈 **Reportes avanzados** y analytics

## 👨‍💻 Información del Desarrollador

- **Carnet**: 202303204
- **Curso**: Introducción a la Programación y Computación 2
- **Universidad**: USAC
- **Práctica**: #2 - Sistema de Gestión de Turnos Médicos

## 📝 Notas de Implementación

### Optimizaciones Realizadas
- ✅ Actualización eficiente de tiempos de espera
- ✅ Manejo robusto de errores y excepciones
- ✅ Interfaz responsiva con threading no bloqueante
- ✅ Gestión inteligente de memoria con cleanup automático
- ✅ Validaciones comprensivas de entrada de datos

### Consideraciones de Rendimiento
- **Complejidad temporal**: Operaciones principales en O(1)
- **Uso de memoria**: Eficiente con cleanup automático
- **Actualización GUI**: No bloqueante con threading
- **Generación de gráficos**: Optimizada con cache

---

## 🎉 ¡Listo para usar!

El sistema está completamente funcional y cumple con todos los requisitos del enunciado. La aplicación proporciona una solución robusta, moderna y fácil de usar para la gestión digitalizada de turnos médicos.