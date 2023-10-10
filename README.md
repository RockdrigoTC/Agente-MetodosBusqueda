# Metodos de busqueda

## Requisitos para ejecutar el programa "MetodosBusqueda.py"

### Opción 1: Instalar las Dependencias Necesarias (Python, numpy, tkinter)

**Windows:**
1. Ve al sitio web oficial de Python en [python.org](https://www.python.org/).
2. Descarga la última versión de Python para Windows.
3. Ejecuta el archivo de instalación descargado y sigue las instrucciones en pantalla. Asegúrate de marcar la casilla que dice "Add Python 3.X to PATH" durante la instalación, donde "3.X" es la versión de Python que estás instalando.
4. Abre una ventana de comandos (cmd) y verifica que Python se haya instalado correctamente ejecutando el siguiente comando:
```
python --version
```
5. Luego, instala las bibliotecas necesarias usando pip (el administrador de paquetes de Python). Ejecuta estos comandos en la ventana de comandos:
```
pip install numpy
```
6. No necesitas instalar tkinter por separado en Windows, ya que generalmente viene incluido en la instalación estándar de Python.

**Linux:**
1. La mayoría de las distribuciones de Linux ya incluyen Python. Abre una terminal y verifica si Python está instalado ejecutando:
```
python --version
```
2. Si Python no está instalado, puedes instalarlo usando el gestor de paquetes de tu distribución. Por ejemplo, en Ubuntu, puedes ejecutar:
```
sudo apt-get install python3
```
3. Luego, instala las bibliotecas necesarias con pip:
```
pip install numpy
```
4. Tkinter generalmente viene preinstalado en la mayoría de las distribuciones de Linux.

5. Una vez instaladas las dependencias, puedes ejecutar el programa "MetodosBusqueda.py" con el siguiente comando:
```
python MetodosBusqueda.py
```
### Opción 2: Utilizar el Entorno "metodos-busqueda"

1. Descomprime el `archivo metodos-busqueda.zip` en la raiz del proyecto.
2. Abre una ventana de comandos (cmd o terminal) en el directorio del proyecto.
3. Activa el entorno virtual ejecutando uno de los siguientes comandos, dependiendo de tu sistema:

**Windows:**
```
.\metodos-busqueda\Scripts\activate
```
**Linux:**
```
source metodos-busqueda/bin/activate
```
4. Una vez que el entorno esté activado, puedes ejecutar el programa "MetodosBusqueda.py" con el siguiente comando:
```
python MetodosBusqueda.py
```
5. Cuando hayas terminado de usar el programa, puedes desactivar el entorno virtual con el siguiente comando:
```
deactivate
```
¡Listo! Ahora puedes ejecutar el programa "MetodosBusqueda.py" en tu sistema, ya sea instalando las dependencias necesarias o utilizando el entorno virtual proporcionado. ¡Disfruta del programa!

## Instrucciones de Uso

**Crear un escenario:** Haz clic en el botón "Nuevo escenario" para generar un nuevo tablero con un tamaño especificado y una dificultad (Fácil, Medio o Difícil). Esto creará un tablero con obstáculos, una posición de inicio y una meta.

**Editar el tablero:** Si deseas editar el tablero manualmente, puedes hacerlo haciendo clic en el botón "Editar escenario". Esto te permitirá modificar las celdas del tablero, establecer obstáculos, la posición de inicio y la posición de la meta.

**Algoritmo de Búsqueda:** Selecciona un algoritmo de búsqueda (DFS, BFS, BestFirst o A*) desde el menú desplegable. Esto determinará qué algoritmo se utilizará para encontrar la ruta.

**Buscar Ruta:** Haz clic en el botón "Buscar" para que el programa ejecute el algoritmo de búsqueda seleccionado y encuentre una ruta desde la posición de inicio hasta la posición de meta.

**Visualización:** El programa mostrará el tablero en la ventana gráfica con la ruta encontrada resaltada en color. También se mostrará la longitud de la ruta y el tiempo de ejecución en la interfaz gráfica.

### Notas Adicionales

- La dificultad influye en la cantidad de obstáculos en el tablero. Cuanto mayor sea la dificultad, más obstáculos habrá.
- Se puede definir el tamaño del escenario con un numero entero N. El minimo y maximo del escenario es de 10 y 100 respectivamente.
- La posición de inicio y la posición de la meta se generan aleatoriamente, asegurando que estén separadas al menos por la mitad del tamaño del tablero.
- Puedes editar manualmente el tablero para establecer obstáculos, la posición de inicio y la posición de la meta. La "I" representa la posición de inicio y la "M" representa la posición de la meta los obstaculos son marcados con "#".
- Los algoritmos de búsqueda disponibles son Depth-First Search (DFS), Breadth-First Search (BFS), Best-First Search (BestF) y A*.
- Durante la búsqueda, el programa mostrará la trayectoria paso a paso y destacará la ruta más corta encontrada cuando termine la búsqueda.
- Si no se encuentra una ruta, se mostrará un mensaje indicando que no se encontró una ruta.
