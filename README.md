# Metodos de busqueda

## Requisitos para ejecutar el programa "MetodosBusqueda.py"

### Instalar las Dependencias Necesarias (Python, numpy, tkinter)

**Windows:**
1. Ve al sitio web oficial de Python en [python.org](https://www.python.org/).
2. Descarga la última versión de Python para Windows.
3. Ejecuta el archivo de instalación descargado y sigue las instrucciones en pantalla. Asegúrate de marcar la casilla que dice "Add Python 3.X to PATH" durante la instalación, donde "3.X" es la versión de Python que estás instalando.
4. Abre una ventana de comandos (cmd) y verifica que Python se haya instalado correctamente ejecutando el siguiente comando:
```
python --version
```
5. Luego, instala las bibliotecas necesarias usando pip (el administrador de paquetes de Python). Ejecuta este comandos en la cmd:
```
pip install numpy
```
- Nota: No necesitas instalar tkinter por separado en Windows, ya que generalmente viene incluido en la instalación estándar de Python.

**Linux:**
1. La mayoría de las distribuciones de Linux ya incluyen Python. Abre una terminal y verifica si Python está instalado ejecutando:
```
python --version
```
2. Si Python no está instalado, puedes instalarlo usando el gestor de paquetes de tu distribución. Por ejemplo, en Ubuntu, puedes ejecutar:
- Debian
  ```
  sudo apt install python3
  ```
- Fedora
  ```
  sudo dnf install python3
  ```
- Arch
  ```
  sudo pacman -S python
  ```
3. Luego, instala Numpy con pip:
```
pip install numpy
```
4. Para instalar Tkinter ejecuta el siguiente comando en la terminal:
- Debian
  ```
  sudo apt install python3-tk
  ```
- Fedora
  ```
  sudo dnf install python3-tkinter
  ```
- Arch
  ```
  sudo pacman -S tk
  ```

6. Una vez instaladas las dependencias, puedes ejecutar el programa "MetodosBusqueda.py" con el siguiente comando:
```
python MetodosBusqueda.py
```

## Uso

**Crear un escenario:** Haz clic en el botón "Nuevo escenario" para generar un nuevo tablero con un tamaño especificado y una dificultad (Fácil, Medio o Difícil). Esto creará un tablero con obstáculos, una posición de inicio y una meta.

**Editar el tablero:** Si deseas editar el tablero manualmente, puedes hacerlo haciendo clic en el botón "Editar escenario". Esto te permitirá modificar las celdas del tablero, establecer obstáculos, la posición de inicio y la posición de la meta.

- Establecer obstáculos: Coloca el simbolo "#" en la celda que deseas marcar como obstáculo.
- Establecer la posición de inicio: Coloca el simbolo "I" en la celda que deseas marcar como posición de inicio.
- Establecer la posición de la meta: Coloca el simbolo "M" en la celda que deseas marcar como posición de la meta.
- Guardar cambios: Haz clic en el botón "Aceptar" para guardar los cambios realizados en el tablero.
- Guardar archivo de tablero: Haz clic en el botón "Guardar" para guardar el tablero en un archivo de texto.
- Cargar archivo de tablero: Haz clic en el botón "Cargar" para cargar un tablero desde un archivo de texto.

**Algoritmo de Búsqueda:** Selecciona un algoritmo de búsqueda (DFS, BFS, BestFirst o A*) desde el menú desplegable. Esto determinará qué algoritmo se utilizará para encontrar la ruta.

**Buscar Ruta:** Haz clic en el botón "Buscar" para que el programa ejecute el algoritmo de búsqueda seleccionado y encuentre una ruta desde la posición de inicio hasta la posición de meta.

**Visualización:** Durante la búsqueda, el programa mostrará los nodos explorados y destacará la ruta más corta encontrada cuando termine la búsqueda. De igual forma, se mostrará el tiempo de ejecución y la longitud de la ruta encontrada.

- Opciones de vizualizacion de ruta: Se cuentan con las opciones de "Gradiente en ruta" y "Flecha en ruta", que permiten vizualizar la ruta encontrada de forma más clara.

### Notas Adicionales

- La dificultad influye en la cantidad de obstáculos en el tablero. Cuanto mayor sea la dificultad, más obstáculos habrá.
- Se puede definir el tamaño del escenario con un numero entero N. El minimo y maximo del escenario es de 10 y 100 respectivamente.
- La posición de inicio y la posición de la meta se generan aleatoriamente, asegurando que estén separadas al menos por la mitad del tamaño del tablero.
