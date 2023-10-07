import numpy as np
import random
import time
import heapq
import tkinter as tk
import colorsys

# Definir constantes para la dificultad
FACIL = 0
MEDIO = 1
DIFICIL = 2

tablero = None
tablero_edicion = None
trayectoria = None
inicio = None
meta = None

# Función para crear un tablero de N x N con obstáculos
def crear_tablero(N, dificultad):
    global tablero, tablero_edicion, inicio, meta
    tablero = np.zeros((N, N), dtype=int)
    
    num_obstaculos = 0
    separacion = int(N / 2)

    # Generar dificultad de obstáculos
    if dificultad == 0:
        num_obstaculos = int(0.1 * N * N)
        separacion = int(N / 2)
    elif dificultad == 1:
        num_obstaculos = int(0.2 * N * N)
        separacion = int(N / 1.5)
    elif dificultad == 2:
        num_obstaculos = int(0.4 * N * N)
        separacion = int(N / 1.25)
    
    # Establecer la posición de inicio y meta aleatoriamente asegurando que esten alejados al menos la mitad del tablero
    inicio = (random.randint(0, N - 1), random.randint(0, N - 1))   
    meta = (random.randint(0, N - 1), random.randint(0, N - 1))
    while distancia_manhattan(inicio, meta) < separacion:
        inicio = (random.randint(0, N - 1), random.randint(0, N - 1))
        meta = (random.randint(0, N - 1), random.randint(0, N - 1))

    # Colocar obstáculos según la dificultad y asegurando que no esten en la posición de inicio y meta
    for i in range(num_obstaculos):
        fila = random.randint(0, N - 1)
        columna = random.randint(0, N - 1)
        if (fila, columna) != inicio and (fila, columna) != meta:
            tablero[fila][columna] = 1

    tablero_edicion = np.copy(tablero)
    return tablero, inicio, meta


# Función para visualizar el tablero en la consola
def mostrar_tablero(tablero, inicio, meta, trayectoria=None):
    N = len(tablero)
    
    # Crear una copia del tablero para visualizar la trayectoria
    if trayectoria is not None:
        tablero = np.copy(tablero)
        for fila, columna in trayectoria:
            tablero[fila][columna] = 2
    
    # Visualizar el tablero
    for fila in range(N):
        for columna in range(N):
            if (fila, columna) == inicio:
                print("I", end=" ")
            elif (fila, columna) == meta:
                print("M", end=" ")
            elif tablero[fila][columna] == 1:
                print("#", end=" ")
            elif tablero[fila][columna] == 2:
                print("*", end=" ")
            else:
                print("-", end=" ")
        print()
    print()


# Función para obtener los vecinos de un nodo
def obtener_vecinos(tablero, nodo):
    # Obtener el tamaño del tablero
    N = len(tablero)
    
    # Obtener la fila y columna del nodo
    fila, columna = nodo
    
    # Crear una lista para almacenar los vecinos
    vecinos = []
    
    # Si el nodo no esta en la primera fila, agregar el vecino de arriba
    if fila > 0 and tablero[fila - 1][columna] != 1:
        vecinos.append((fila - 1, columna))
    
    # Si el nodo no esta en la última columna, agregar el vecino de la derecha
    if columna < N - 1 and tablero[fila][columna + 1] != 1:
        vecinos.append((fila, columna + 1))

    # Si el nodo no esta en la última fila, agregar el vecino de abajo
    if fila < N - 1 and tablero[fila + 1][columna] != 1:
        vecinos.append((fila + 1, columna))
    
    # Si el nodo no esta en la primera columna, agregar el vecino de la izquierda
    if columna > 0 and tablero[fila][columna - 1] != 1:
        vecinos.append((fila, columna - 1))
    
    return vecinos


# función para obtener la distancia Manhattan entre dos nodos
def distancia_manhattan(nodo1, nodo2):
    # Obtener la fila y columna de cada nodo
    fila1, columna1 = nodo1
    fila2, columna2 = nodo2
    
    # Calcular la distancia Manhattan
    distancia = abs(fila1 - fila2) + abs(columna1 - columna2)
    
    return distancia


# Función para esperar un tiempo proporcional al tamaño del tablero
def esperar(tablero):
    tiempo = 1 / len(tablero)
    time.sleep(tiempo)


# Algoritmo de Depth-First Search (DFS)
def dfs(tablero, inicio, meta):
    # Iniciar el tiempo de ejecución
    inicio_tiempo = time.perf_counter()

    # Pila para almacenar los nodos
    pila = []

    # Diccionario para almacenar los nodos visitados
    visitados = {}

    # Agregar el nodo inicial a la pila junto con una ruta vacía
    pila.append((inicio, []))

    # Ruta más corta encontrada
    ruta_corta = []

    # Mientras la pila no esté vacía
    while len(pila) > 0:
        # Extraer el nodo y la ruta de la pila
        nodo, ruta_actual = pila.pop()

        # Si el nodo no ha sido visitado
        if nodo not in visitados:
            # Marcar el nodo como visitado
            visitados[nodo] = True

            # Agregar el nodo a la ruta actual
            ruta_actual.append(nodo)

            # Si el nodo es la meta, actualizar la ruta más corta encontrada
            if nodo == meta:
                if not ruta_corta or len(ruta_actual) < len(ruta_corta):
                    ruta_corta = list(ruta_actual)
                fin_tiempo = time.perf_counter() - inicio_tiempo
                # Mostrar la trayectoria mas corta encontrada
                ruta = []
                for nodo in ruta_corta:
                    esperar(tablero)
                    ruta.append(nodo)
                    mostrar_tablero_en_canvas(tablero, inicio, meta, ruta, True)
                return ruta_corta, fin_tiempo

            # Obtener los vecinos del nodo
            vecinos = obtener_vecinos(tablero, nodo)

            # Agregar los vecinos a la pila junto con la ruta actual
            for vecino in vecinos:
                pila.append((vecino, list(ruta_actual)))

            esperar(tablero)
            mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()))

    # Si no se encontró una trayectoria, retornar None
    mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()), False)
    return None, time.perf_counter() - inicio_tiempo


# Algoritmo de Breadth-First Search (BFS)
def bfs(tablero, inicio, meta):
    # Iniciar el tiempo de ejecución
    inicio_tiempo = time.perf_counter()

    # Cola para almacenar los nodos junto con sus rutas
    cola = []
    
    # Diccionario para almacenar los nodos visitados y sus rutas
    visitados = {}
    
    # Agregar el nodo inicial a la cola junto con una ruta vacía
    cola.append((inicio, []))
    
    # Ruta más corta encontrada
    ruta_corta = []

    # Mientras la cola no esté vacía
    while len(cola) > 0:
        # Extraer el nodo y la ruta de la cola
        nodo, ruta_actual = cola.pop(0)
        
        # Si el nodo no ha sido visitado
        if nodo not in visitados:
            # Marcar el nodo como visitado
            visitados[nodo] = True
            
            # Agregar el nodo a la ruta actual
            ruta_actual.append(nodo)

            # Si el nodo es la meta, actualizar la ruta más corta encontrada
            if nodo == meta:
                if not ruta_corta or len(ruta_actual) < len(ruta_corta):
                    ruta_corta = list(ruta_actual)

                fin_tiempo = time.perf_counter() - inicio_tiempo
                # Mostrar la trayectoria mas corta encontrada
                ruta = []
                for nodo in ruta_corta:
                    esperar(tablero)
                    ruta.append(nodo)
                    mostrar_tablero_en_canvas(tablero, inicio, meta, ruta, True)
                return ruta_corta, fin_tiempo
                
            # Obtener los vecinos del nodo
            vecinos = obtener_vecinos(tablero, nodo)
            
            # Agregar los vecinos a la cola junto con la ruta actual
            for vecino in vecinos:
                cola.append((vecino, list(ruta_actual)))

            esperar(tablero)
            mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()))
    
    # No hay trayectoria
    mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()), False)
    return None, time.perf_counter() - inicio_tiempo


# Función de Best-First Search (BFS)
def best_first_search(tablero, inicio, meta):

    # Iniciar el tiempo de ejecución
    inicio_tiempo = time.perf_counter()

    # Cola de prioridad para almacenar los nodos
    cola_prioridad = []
    
    # Diccionario para almacenar los nodos visitados y sus rutas
    visitados = {}
    
    # Agregar el nodo inicial a la cola de prioridad junto con una ruta vacía
    cola_prioridad.append((inicio, distancia_manhattan(inicio, meta), []))
    
    # Ruta más corta encontrada
    ruta_corta = []

    # Mientras la cola de prioridad no esté vacía
    while len(cola_prioridad) > 0:
        # Extraer el nodo, la distancia y la ruta de la cola de prioridad
        nodo, _, ruta_actual = cola_prioridad.pop(0)
        
        # Si el nodo no ha sido visitado
        if nodo not in visitados:
            # Marcar el nodo como visitado
            visitados[nodo] = True
            
            # Agregar el nodo a la ruta actual
            ruta_actual.append(nodo)

            # Si el nodo es la meta, actualizar la ruta más corta encontrada
            if nodo == meta:
                if not ruta_corta or len(ruta_actual) < len(ruta_corta):
                    ruta_corta = list(ruta_actual)
                fin_tiempo = time.perf_counter() - inicio_tiempo
                # Mostrar la trayectoria mas corta encontrada
                ruta = []
                for nodo in ruta_corta:
                    esperar(tablero)
                    ruta.append(nodo)
                    mostrar_tablero_en_canvas(tablero, inicio, meta, ruta, True)
                return ruta_corta, fin_tiempo
            
            # Obtener los vecinos del nodo
            vecinos = obtener_vecinos(tablero, nodo)
            
            # Agregar los vecinos a la cola de prioridad junto con la ruta actual
            for vecino in vecinos:
                distancia_hasta_meta = distancia_manhattan(vecino, meta)
                cola_prioridad.append((vecino, distancia_hasta_meta, list(ruta_actual)))
            
            # Ordenar la cola de prioridad
            cola_prioridad.sort(key=lambda x: x[1])

            esperar(tablero)
            mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()))
    
    # No hay trayectoria
    mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()), False)
    return None, time.perf_counter() - inicio_tiempo


# Función de búsqueda A*
def astar(tablero, inicio, meta):

    # Iniciar el tiempo de ejecución
    inicio_tiempo = time.perf_counter()

    # Cola de prioridad para almacenar los nodos con prioridad total
    cola_prioridad = [(0, inicio)]  # (Prioridad, Nodo)
    
    # Diccionario para almacenar los costos acumulativos
    costos_acumulativos = {inicio: 0}
    
    # Diccionario para almacenar el padre de cada nodo
    padres = {}
    
    # Mientras la cola de prioridad no esté vacía
    while cola_prioridad:
        # Extraer el nodo con menor prioridad total
        _, nodo = heapq.heappop(cola_prioridad)
        
        # Si el nodo es la meta, reconstruir la trayectoria y retornarla
        if nodo == meta:
            trayectoria = [meta]
            while nodo in padres:
                nodo = padres[nodo]
                trayectoria.append(nodo)
            trayectoria.reverse()
            fin_tiempo = time.perf_counter() - inicio_tiempo
            
            # Mostrar la trayectoria en el Canvas paso a paso
            ruta = []
            for nodo in trayectoria:
                esperar(tablero)
                ruta.append(nodo)
                mostrar_tablero_en_canvas(tablero, inicio, meta, ruta, True)

            return trayectoria, fin_tiempo
        
        # Obtener los vecinos del nodo
        vecinos = obtener_vecinos(tablero, nodo)
        
        # Explorar los vecinos
        for vecino in vecinos:
            # Calcular el nuevo costo acumulativo desde el nodo inicial
            nuevo_costo = costos_acumulativos[nodo] + 1
            
            # Si el vecino no ha sido visitado o tiene un costo acumulativo menor
            if vecino not in costos_acumulativos or nuevo_costo < costos_acumulativos[vecino]:
                # Actualizar el costo acumulativo
                costos_acumulativos[vecino] = nuevo_costo
                
                # Calcular la prioridad total
                prioridad_total = nuevo_costo + distancia_manhattan(vecino, meta)
                
                # Agregar el vecino a la cola de prioridad
                heapq.heappush(cola_prioridad, (prioridad_total, vecino))
                
                # Establecer el nodo actual como el padre del vecino
                padres[vecino] = nodo

            esperar(tablero)
            mostrar_tablero_en_canvas(tablero, inicio, meta, list(padres.keys()))

    # No hay una trayectoria
    mostrar_tablero_en_canvas(tablero, inicio, meta, list(padres.keys()), False)
    return None, time.perf_counter() - inicio_tiempo


# Función para generar un gradiente entre dos colores
def generar_color_gradiente(posicion_actual, longitud_ruta, color_inicio=(0, 50, 230), color_final=(0, 255, 0)):
    # Calcula el valor intermedio de hue entre los dos colores
    hue_inicio = colorsys.rgb_to_hsv(color_inicio[0] / 255, color_inicio[1] / 255, color_inicio[2] / 255)[0]
    hue_final = colorsys.rgb_to_hsv(color_final[0] / 255, color_final[1] / 255, color_final[2] / 255)[0]
    hue_intermedio = hue_inicio + (hue_final - hue_inicio) * float(posicion_actual) / longitud_ruta
    
    # Convierte el hue intermedio de nuevo a RGB
    rgb = colorsys.hsv_to_rgb(hue_intermedio, 1, 1)
    
    # Convierte los valores RGB en una cadena hexadecimal
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))


# Función para mostrar el tablero y la ruta en el Canvas
def mostrar_tablero_en_canvas(tablero, inicio, meta, ruta=None, exito=None):
    canvas.delete("all")

    N = len(tablero)
    ancho_celda = 500 / N
    
    for fila in range(N):
        for columna in range(N):
            x1 = columna * ancho_celda
            y1 = fila * ancho_celda
            x2 = x1 + ancho_celda
            y2 = y1 + ancho_celda
            
            if (fila, columna) == inicio:
                canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black")
            elif (fila, columna) == meta:
                canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")
            elif tablero[fila][columna] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
            elif ruta and (fila, columna) in ruta:
                if exito is None:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")
                elif exito:
                    posicion_actual = ruta.index((fila, columna))
                    color = generar_color_gradiente(posicion_actual, len(ruta))
                    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

    ventana.update()


# Función para crear un escenario
def crear_escenario():
    global tablero, inicio, meta
    # Obtener el tamaño del tablero y la dificultad desde la interfaz gráfica
    tamaño_tablero_entry_value = tamaño_tablero_entry.get()
    if tamaño_tablero_entry_value.isdigit():
        tamaño_tablero = int(tamaño_tablero_entry_value)
        if 10 <= tamaño_tablero <= 100:
            pass
        else:
            tamaño_tablero = min(max(tamaño_tablero, 10), 100)
    else:
        tamaño_tablero = 10

    dificultad = dificultad_var.get()
    if dificultad.startswith("Fácil"):
        dificultad = FACIL
    elif dificultad.startswith("Medio"): 
        dificultad = MEDIO
    elif dificultad.startswith("Difícil"):
        dificultad = DIFICIL

    # Crear un tablero con el tamaño y dificultad especificados
    tablero, inicio, meta = crear_tablero(tamaño_tablero, dificultad)
    
    # Mostrar el tablero en el Canvas
    mostrar_tablero_en_canvas(tablero, inicio, meta)    


# Función para editar el tablero
def editar_tablero():
    global tablero, tablero_edicion, inicio, meta

    if tablero_edicion is None:
        tablero_edicion = np.ndarray((20, 20), dtype=str)
        tablero_edicion.fill("0")

    tablero_edicion = tablero_edicion.astype(str)
    tablero_edicion[tablero_edicion == "0"] = ""
    tablero_edicion[tablero_edicion == "1"] = "#"

    if inicio is not None:
        tablero_edicion[inicio] = "I"
    if meta is not None:
        tablero_edicion[meta] = "M"

    # Crear una ventana para editar el tablero
    ventana_edicion = tk.Toplevel(ventana)
    ventana_edicion.title("Editar Tablero")
    ventana_edicion.resizable(False, False)

    # Función para validar la entrada y limitarla a un solo carácter
    def validar_entrada(cadena):
        if len(cadena) > 1:
            return False
        return True

    validar_entrada_fn = ventana_edicion.register(validar_entrada)

    # Cargar el tablero en la ventana de edición
    for fila in range(len(tablero_edicion)):
        for columna in range(len(tablero_edicion)):
            celda = tk.Entry(ventana_edicion, width=3, validate="key", validatecommand=(validar_entrada_fn, "%P"))
            celda.grid(row=fila, column=columna)
            celda.insert(0, tablero_edicion[fila][columna])
            celda.config(justify="center")

    # Botón para guardar el tablero editado
    guardar_button = tk.Button(ventana_edicion, text="Guardar", command=lambda: guardar_tablero(ventana_edicion))
    guardar_button.grid(row=len(tablero_edicion) + 1, column=1, columnspan=len(tablero_edicion))


# Función para guardar el tablero editado
def guardar_tablero(ventana_edicion):
    global tablero, tablero_edicion, inicio, meta

    # Obtener el tablero editado desde la ventana de edición
    for fila in range(len(tablero_edicion)):
        for columna in range(len(tablero_edicion)):
            celda = ventana_edicion.grid_slaves(row=fila, column=columna)[0]
            valor_celda = celda.get()
            if not valor_celda:
                valor_celda = "0"
            elif valor_celda == "#":
                valor_celda = "1"
            elif valor_celda == "I":
                valor_celda = "2"
            elif valor_celda == "M":
                valor_celda = "3"
            else:
                valor_celda = "0"
            tablero_edicion[fila][columna] = valor_celda

    # Convertir el tablero editado a una matriz de enteros
    tablero_edicion = tablero_edicion.astype(int)

    # Asignar la posición de inicio y meta
    if 2 in tablero_edicion:
        inicio = np.where(tablero_edicion == 2)
        inicio = (inicio[0][0], inicio[1][0])
    if 3 in tablero_edicion:
        meta = np.where(tablero_edicion == 3)
        meta = (meta[0][0], meta[1][0])

    # Eliminar los obstáculos en la posición de inicio y meta
    tablero_edicion[tablero_edicion == 2] = 0
    tablero_edicion[tablero_edicion == 3] = 0

    # Actualizar el tablero
    tablero = np.copy(tablero_edicion)

    # Mostrar el tablero en el Canvas
    mostrar_tablero_en_canvas(tablero, inicio, meta)
    
    # Cerrar la ventana de edición
    ventana_edicion.destroy()


# Función para ejecutar los algoritmos de búsqueda
def buscar_ruta():
    global tablero, inicio, meta, trayectoria

    ruta_var.set("0")
    tiempo_var.set("0")
    buscar_button.config(state="disabled")

    # Obtener el algoritmo de búsqueda desde la interfaz gráfica
    algoritmo = algoritmo_var.get()

    # Ejecutar el algoritmo de búsqueda especificado
    if algoritmo == "DFS":
        trayectoria, tiempo_ejecucion = dfs(tablero, inicio, meta)
    elif algoritmo == "BFS":
        trayectoria, tiempo_ejecucion = bfs(tablero, inicio, meta)
    elif algoritmo == "Best":
        trayectoria, tiempo_ejecucion = best_first_search(tablero, inicio, meta)
    elif algoritmo == "A*":
        trayectoria, tiempo_ejecucion = astar(tablero, inicio, meta)
    
    print(f"Algoritmo: {algoritmo}")
    print(f"Tiempo de ejecución: {tiempo_ejecucion} segundos")
    print(f"Tamaño de la ruta: {len(trayectoria)}")

    # Actualizar el tamaño de la ruta y el tiempo de ejecución en la interfaz gráfica
    ruta_var.set(str(len(trayectoria)))
    tiempo_var.set(str(round(tiempo_ejecucion, 4)))

    buscar_button.config(state="normal")


# Ventana principal de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Algoritmos de Búsqueda")
ventana.resizable(False, False)
ventana.geometry("710x510")

# Canvas para mostrar el tablero
canvas = tk.Canvas(ventana, width=500, height=500)
canvas.grid(row=0, column=0, rowspan=30, padx=1, pady=1)

# Campo de entrada para el tamaño del tablero
tamaño_tablero_label = tk.Label(ventana, text="Tamaño del tablero:")
tamaño_tablero_label.grid(row=3, column=1, padx=1, pady=1)
tamaño_tablero_entry = tk.Entry(ventana, justify="center", width=5)
tamaño_tablero_entry.grid(row=3, column=2, padx=1, pady=1)
tamaño_tablero_entry.insert(0, "20")

# Opción para la dificultad
dificultad_label = tk.Label(ventana, text="Dificultad:")
dificultad_label.grid(row=4, column=1, padx=1, pady=1)
dificultad_var = tk.StringVar()
dificultad_var.set("Medio")
dificultad_optionmenu = tk.OptionMenu(ventana, dificultad_var, "Fácil   ", "Medio", "Difícil ")
dificultad_optionmenu.grid(row=4, column=2, padx=1, pady=1)

# Botón para crear un escenario
ejecutar_button = tk.Button(ventana, text="Nuevo escenario", command=crear_escenario)
ejecutar_button.grid(row=5, column=1, columnspan=2, padx=1, pady=1)

# Botón para editar el tablero
editar_button = tk.Button(ventana, text="Editar escenario", command=editar_tablero)
editar_button.grid(row=6, column=1, columnspan=2, padx=1, pady=1)

# Opción para el algoritmo de búsqueda
algoritmo_label = tk.Label(ventana, text="Algoritmo:")
algoritmo_label.grid(row=7, column=1, padx=1, pady=1)
algoritmo_var = tk.StringVar()
algoritmo_var.set("DFS")
algoritmo_optionmenu = tk.OptionMenu(ventana, algoritmo_var, "DFS", "BFS", "Best", "A*")
algoritmo_optionmenu.grid(row=7, column=2, padx=1, pady=1)

# Botón para ejecutar el algoritmo de búsqueda. fuente por defecto en negrita en negrita
buscar_button = tk.Button(ventana, text="Buscar", command=buscar_ruta, font=("Arial", 11, "bold"))
buscar_button.grid(row=8, column=1, columnspan=2, padx=1, pady=1)

# Resultados tamaño de la ruta
ruta_label = tk.Label(ventana, text="Longitud de ruta:")
ruta_label.grid(row=27, column=1, padx=1, pady=1)
ruta_var = tk.StringVar()
ruta_var.set("0")
ruta_entry = tk.Entry(ventana, state="readonly",justify="center", width=6, textvariable=ruta_var)
ruta_entry.grid(row=27, column=2, padx=1, pady=1)

# Resultados tiempo de ejecución
tiempo_label = tk.Label(ventana, text="Tiempo de ejecución:")
tiempo_label.grid(row=28, column=1, padx=1, pady=1)
tiempo_var = tk.StringVar()
tiempo_var.set("0")
tiempo_entry = tk.Entry(ventana, state="readonly",justify="center", width=6, textvariable=tiempo_var)
tiempo_entry.grid(row=28, column=2, padx=1, pady=1)

# Crear un tablero inicial
crear_tablero(20, MEDIO)
mostrar_tablero_en_canvas(tablero, inicio, meta)

ventana.mainloop()
