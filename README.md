# Range Minimum Query (RMQ) — Optimización de $O(n)$ a $O(1)$ con Sparse Table

Este repositorio contiene una solución y estudio comparativo del problema del **Rango de Consulta Mínima (Range Minimum Query - RMQ)**. El objetivo principal es demostrar empírica y visualmente cómo la transición de una búsqueda lineal ingenua $O(n)$ a una estructura precalculada **Sparse Table** permite resolver consultas en tiempo constante $O(1)$ tras una precomputación de $O(n \log n)$.

El proyecto incluye herramientas de benchmarking, una demostración interactiva en consola, un visualizador gráfico animado con Tkinter, y la documentación académica (LaTeX, Guión de Exposición, etc.).

---

## 🚀 Características del Proyecto

* **📊 Benchmark de Rendimiento (`rmq_benchmark.py`):** Evalúa arreglos masivos de hasta 100,000 elementos bajo 10,000 consultas concurrentes. Mide la diferencia en segundos y genera automáticamente una gráfica comparativa (`rmq_benchmark_plot.png`).
* **💻 Demo Interactiva en Consola (`rmq_benchmark.py --demo`):** Permite ingresar datos personalizados o generar arreglos aleatorios para probar consultas de rangos personalizadas en tiempo real.
* **🎨 Visualizador Gráfico (`rmq_gui.py`):** Interfaz moderna oscura (estilo *Catppuccin*) desarrollada en Tkinter que ilustra de manera animada cada 5 segundos cómo la matemática de Sparse Table une dos intervalos de potencias de 2 que se solapan para obtener el mínimo al instante.
* **📄 Documentación Académica (`Documentacion/`):** Contiene el informe técnico detallado, la presentación académica en LaTeX (`.tex`) y un guión diseñado para presentaciones de 10-15 minutos.

---

## 📁 Estructura del Repositorio

```text
├── Documentacion/
│   ├── RMQ Manual de uso.pdf    # Manual formal en formato PDF
├── rmq_benchmark.py             # Script de benchmarking & demo interactiva
├── rmq_benchmark_plot.png       # Gráfica generada por el benchmark
├── rmq_gui.py                   # Interfaz de usuario interactiva y animada
└── README.md                    # Este archivo de documentación
```

---

## 🛠️ Requisitos de Instalación

El proyecto está desarrollado completamente en **Python 3**. Requiere la instalación de `matplotlib` para la generación de gráficas y `tkinter` para el visualizador gráfico.

Para instalar las dependencias necesarias, ejecuta:

```bash
pip install matplotlib
```

> **Nota para usuarios de Linux (si aplica):** Si obtienes un error con Tkinter, puedes instalarlo usando tu gestor de paquetes (por ejemplo, `sudo apt-get install python3-tk`).

---

## 📖 Instrucciones de Uso

### 1. Ejecutar el Benchmark Masivo
Para realizar las pruebas de estrés con diferentes tamaños de arreglos y generar la gráfica comparativa:
```bash
python rmq_benchmark.py
```
Esto imprimirá una tabla con los tiempos de ejecución en la terminal y guardará la gráfica como `rmq_benchmark_plot.png` en la raíz del repositorio.

### 2. Ejecutar la Demostración Interactiva (CLI)
Para probar consultas con tus propios datos ingresados por consola:
```bash
python rmq_benchmark.py --demo
```
1. Ingresa una lista de números separados por espacio (o presiona *Enter* para generar 15 elementos aleatorios).
2. Introduce rangos en formato `L R` (por ejemplo, `2 8`) para ver el valor mínimo en ese segmento obtenido por la Sparse Table e ingenua de forma paralela.
3. Ingresa `q` para salir del bucle.

### 3. Iniciar el Visualizador Animado (GUI)
Para abrir la interfaz interactiva moderna y visualizar el solapamiento de intervalos en tiempo de ejecución:
```bash
python rmq_gui.py
```
*La GUI elegirá de forma autónoma rangos aleatorios cada 5 segundos y pintará de color cian el bloque precalculado de la izquierda, de magenta el bloque de la derecha y de verde brillante el mínimo final.*

---

## 📐 Fundamento Matemático

El problema RMQ consiste en encontrar el índice del elemento mínimo en un subarreglo $A[L..R]$. 

### Idempotencia
La clave para lograr consultas en tiempo $O(1)$ sin que afecte el solapamiento de rangos es la **idempotencia** del operador de mínimo:
$$\min(x, x) = x$$

Esto significa que si queremos consultar el rango $[L, R]$, y definimos $k = \lfloor \log_2(R - L + 1) \rfloor$ (la potencia de 2 más grande que cabe en el rango):
* El primer bloque cubre desde $L$ hasta $L + 2^k - 1$.
* El segundo bloque cubre desde $R - 2^k + 1$ hasta $R$.

Ambos bloques pueden solaparse, pero el mínimo total sigue siendo:
$$\text{RMQ}(L, R) = \min(\text{ST}[L][k], \text{ST}[R - 2^k + 1][k])$$

---

## 📈 Resultados Esperados

Al correr el benchmark, se observará que a medida que $n$ (el tamaño del arreglo) crece, el tiempo de la búsqueda ingenua $O(n)$ escala linealmente de manera ascendente. En contraste, la consulta a través de la Sparse Table se mantiene completamente plana, operando en tiempo constante $O(1)$.

¡Disfruta del proyecto y de la optimización algorítmica!
