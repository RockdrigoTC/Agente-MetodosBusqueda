import os
import numpy as np
import random
import time
import heapq
import tkinter as tk
import colorsys
from tkinter import messagebox
from tkinter import filedialog


# Función para crear un tablero de N x N con una dificultad especificada
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
        separacion = int(N / 1.4)
    elif dificultad == 2:
        num_obstaculos = int(0.4 * N * N)
        separacion = int(N / 1.25)
    
    # Establecer la posición de inicio y meta aleatoriamente asegurando que esten alejados al menos la mitad del tablero
    while True:
        inicio = (random.randint(0, N - 1), random.randint(0, N - 1))
        meta = (random.randint(0, N - 1), random.randint(0, N - 1))
        if distancia_manhattan(inicio, meta) > separacion:
            break

    tablero[inicio] = 2
    tablero[meta] = 3

    # Colocar obstáculos según la dificultad y asegurando que no esten en la posición de inicio y meta
    for i in range(num_obstaculos):
        fila = random.randint(0, N - 1)
        columna = random.randint(0, N - 1)
        if (fila, columna) != inicio and (fila, columna) != meta:
            tablero[fila][columna] = 1

    # Suavizar el tablero 
    for fila in range(N):
        for columna in range(N):
            vecinos = obtener_vecinos(tablero, (fila, columna))
            if len(vecinos) == 0 and tablero[fila][columna] == 0:
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

    # Si el nodo no esta en la primera columna, agregar el vecino de la izquierda
    if columna > 0 and tablero[fila][columna - 1] != 1:
        vecinos.append((fila, columna - 1))
    
    # Si el nodo no esta en la última columna, agregar el vecino de la derecha
    if columna < N - 1 and tablero[fila][columna + 1] != 1:
        vecinos.append((fila, columna + 1))

    # Si el nodo no esta en la última fila, agregar el vecino de abajo
    if fila < N - 1 and tablero[fila + 1][columna] != 1:
        vecinos.append((fila + 1, columna))
    
    #Invertir lista
    vecinos.reverse()

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
    global velocidad_var
    factor = velocidad_var.get()
    tiempo = 10 / factor / len(tablero)
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
                # Mostrar la trayectoria mas corta encontrada
                mostrar_tablero_en_canvas(tablero, inicio, meta, ruta_corta, True)
                return ruta_corta, time.perf_counter() - inicio_tiempo

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

                # Mostrar la trayectoria mas corta encontrada
                mostrar_tablero_en_canvas(tablero, inicio, meta, ruta_corta, True)
                return ruta_corta, time.perf_counter() - inicio_tiempo
                
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

                # Mostrar la trayectoria mas corta encontrada
                mostrar_tablero_en_canvas(tablero, inicio, meta, ruta_corta, True)
                return ruta_corta, time.perf_counter() - inicio_tiempo
            
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
    padres = {inicio: None}
    
    # Mientras la cola de prioridad no esté vacía
    while cola_prioridad:
        # Extraer el nodo con menor prioridad total
        _, nodo = heapq.heappop(cola_prioridad)
        
        # Si el nodo es la meta, reconstruir la trayectoria y retornarla
        if nodo == meta:
            trayectoria = [meta]
            while nodo in padres:
                nodo = padres[nodo]
                if nodo is not None:
                    trayectoria.append(nodo)
            trayectoria.reverse()
            # Mostrar la trayectoria mas corta encontrada
            mostrar_tablero_en_canvas(tablero, inicio, meta, trayectoria, True)
            return trayectoria, time.perf_counter() - inicio_tiempo
        
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
def generar_color_gradiente(posicion_actual, longitud_ruta, color_inicio=(0, 50, 230), color_final=(0, 128, 0)):
    # Calcula el valor intermedio de hue entre los dos colores
    hue_inicio = colorsys.rgb_to_hsv(color_inicio[0] / 255, color_inicio[1] / 255, color_inicio[2] / 255)[0]
    hue_final = colorsys.rgb_to_hsv(color_final[0] / 255, color_final[1] / 255, color_final[2] / 255)[0]
    hue_intermedio = hue_inicio + (hue_final - hue_inicio) * float(posicion_actual) / longitud_ruta
    
    # Convierte el hue intermedio de nuevo a RGB
    rgb = colorsys.hsv_to_rgb(hue_intermedio, 1, 1)
    
    # Convierte los valores RGB en una cadena hexadecimal
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

def mostrar_tablero_en_canvas_mapa(tablero, inicio, meta, ruta=None, exito=None):
    canvas.delete("all")
    canvas.delete("all")

    N = len(tablero)
    ancho_celda = 600 / N
    font = (int)(200 / N)
    borde = (int)(len(tablero)) / 10
    
    for fila in range(N):
        for columna in range(N):
            x1 = columna * ancho_celda
            y1 = fila * ancho_celda
            x2 = x1 + ancho_celda
            y2 = y1 + ancho_celda
            
            if (fila, columna) == inicio:
                canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="blue", width=borde)
                canvas.create_text(x1 + ancho_celda / 2, y1 + ancho_celda / 2, text="I", font=("Arial", font, "bold"))
            elif (fila, columna) == meta:
                canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="green", width=borde)
                canvas.create_text(x1 + ancho_celda / 2, y1 + ancho_celda / 2, text="M", font=("Arial", font, "bold"))
            elif tablero[fila][columna] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
            elif tablero[fila][columna] == 0:
                canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

    ventana.update()

# Función para mostrar el tablero y la ruta en el Canvas
def mostrar_tablero_en_canvas(tablero, inicio, meta, ruta=None, exito=None):
    global ultimo_pintado
    #canvas.delete("all")

    N = len(tablero)
    ancho_celda = 600 / N
    font = (int)(200 / N)
    gradiente_ruta = gradiente_ruta_var.get()
    flecha_ruta = flecha_ruta_var.get()


    fila, columna = ruta[-1]
    if len(ruta) > 2:
        fila2, columna2 = ruta[-2]
        x3 = columna2 * ancho_celda
        y3 = fila2 * ancho_celda
        x4 = x3 + ancho_celda
        y4 = y3 + ancho_celda
    x1 = columna * ancho_celda
    y1 = fila * ancho_celda
    x2 = x1 + ancho_celda
    y2 = y1 + ancho_celda
    if exito is None:
        if (fila, columna) != inicio and (fila, columna) != meta:
            canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black")
            ultimo_pintado = (fila, columna)
        if len(ruta) > 2:
            if (fila2, columna2) != inicio and (fila2, columna2) != meta:
                canvas.create_rectangle(x3, y3, x4, y4, fill="gray", outline="black")
    elif exito:
        # Ruta encontrada
        canvas.create_rectangle(ultimo_pintado[1]*ancho_celda, ultimo_pintado[0]*ancho_celda, 
                                ultimo_pintado[1]*ancho_celda+ancho_celda, ultimo_pintado[0]*ancho_celda+ancho_celda, 
                                fill="gray", outline="black")
        ancho_flecha = (int)(60 / N)
        if ancho_flecha < 1:
            ancho_flecha = 1
        for fila, columna in ruta:
            if (fila, columna) != inicio and (fila, columna) != meta:
                esperar(tablero)
                posicion_actual = ruta.index((fila, columna))
                if gradiente_ruta:
                    color = generar_color_gradiente(posicion_actual, len(ruta))
                else:
                    color = "green"
                x1 = columna * ancho_celda
                y1 = fila * ancho_celda
                x2 = x1 + ancho_celda
                y2 = y1 + ancho_celda
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                if flecha_ruta:
                    # Dibujar una flecha en la dirección de la ruta
                    if posicion_actual < len(ruta) - 1:
                        fila_siguiente, columna_siguiente = ruta[posicion_actual + 1]
                        x_mid = (x1 + x2) / 2
                        y_mid = (y1 + y2) / 2
                        if fila == fila_siguiente:
                            if columna < columna_siguiente:
                                # Dibuja una flecha hacia la derecha
                                canvas.create_polygon(x2, y_mid, x_mid, y1+ancho_celda/6, x_mid, y2-ancho_celda/6, fill="black", outline="black")
                                canvas.create_line(x2-ancho_celda/2, y_mid, x1, y_mid, fill="black", width=ancho_flecha)
                            else:
                                # Dibuja una flecha hacia la izquierda
                                canvas.create_polygon(x1, y_mid, x_mid, y1+ancho_celda/6, x_mid, y2-ancho_celda/6, fill="black", outline="black")
                                canvas.create_line(x1+ancho_celda/2, y_mid, x2, y_mid, fill="black", width=ancho_flecha)
                        elif columna == columna_siguiente:
                            if fila < fila_siguiente:
                                # Dibuja una flecha hacia abajo
                                canvas.create_polygon(x_mid, y2, x1+ancho_celda/6, y_mid, x2-ancho_celda/6, y_mid, fill="black", outline="black")
                                canvas.create_line(x_mid, y2-ancho_celda/2, x_mid, y1, fill="black", width=ancho_flecha)
                            else:
                                # Dibuja una flecha hacia arriba
                                canvas.create_polygon(x_mid, y1, x1+ancho_celda/6, y_mid, x2-ancho_celda/6, y_mid, fill="black", outline="black")
                                canvas.create_line(x_mid, y1+ancho_celda/2, x_mid, y2, fill="black", width=ancho_flecha)

            ventana.update()
    else:
        # Ruta no encontrada
        for fila, columna in ruta:
            if (fila, columna) != inicio and (fila, columna) != meta:
                x1 = columna * ancho_celda
                y1 = fila * ancho_celda
                x2 = x1 + ancho_celda
                y2 = y1 + ancho_celda
                canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")
    
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

    tamaño_tablero_entry.delete(0, tk.END)
    tamaño_tablero_entry.insert(0, str(tamaño_tablero))
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
    mostrar_tablero_en_canvas_mapa(tablero, inicio, meta)    

def abrir_ventana_edicion():
    global tablero, inicio, meta

    # Mostrar un mensaje si el tablero es demasiado grande
    if len(tablero) > 20:
        messagebox.showinfo("Editar Tablero", "El tablero es demasiado grande para editarlo.\nMáximo: 20x20", parent=ventana)
        return None

    # Crear una ventana para editar el tablero, al centro de la ventana principal
    ventana_edicion = tk.Toplevel(ventana)
    ventana_edicion.title("Edición de Escenario")
    ventana_edicion.resizable(False, False)
    ventana_edicion.grab_set()
    ventana_edicion.transient(ventana)
    ventana_edicion.geometry("+%d+%d" % (ventana.winfo_rootx() + 100, ventana.winfo_rooty()-50))

    # Función para cambiar el color de una celda en la ventana de edición
    def cambiar_color(fila, columna):
        global inicio, meta
        color = color_var.get()
        celdas[fila][columna].config(bg=color)
        if color == "white":
            copy_tablero[fila][columna] = 0  # Celda vacía
        elif color == "black":
            copy_tablero[fila][columna] = 1  # Celda obstáculo
        elif color == "blue":
            copy_tablero[fila][columna] = 2
            inicio = (fila, columna)
        elif color == "green":
            copy_tablero[fila][columna] = 3
            meta = (fila, columna)

    filas = tablero.shape[0]
    columnas = tablero.shape[1]
    celdas = []
    copy_tablero = np.copy(tablero)

    for fila in range(filas):
        fila_celdas = []
        for columna in range(columnas):
            if tablero[fila][columna] == 0:
                color = "white"
            elif tablero[fila][columna] == 1:
                color = "black"
            elif tablero[fila][columna] == 2:
                color = "blue"
            elif tablero[fila][columna] == 3:
                color = "green"
            boton = tk.Button(ventana_edicion, bg=color, width=2, height=1, command=lambda f=fila, c=columna: cambiar_color(f, c))
            boton.grid(row=fila, column=columna)
            fila_celdas.append(boton)
        celdas.append(fila_celdas)

    # Función para limpiar el tablero
    def limpiar_tablero():
        for fila in range(filas):
            for columna in range(columnas):
                celdas[fila][columna].config(bg="white")
                copy_tablero[fila][columna] = 0

    def guardar_escenario():
        global tablero, inicio, meta
        # Comprobar que hay un inicio y una meta
        if 2 not in copy_tablero or 3 not in copy_tablero:
            messagebox.showerror("Editar Tablero", "El escenario debe tener un inicio y una meta.", parent=ventana_edicion)
            return None
        # comprobar que no haya mas de un inicio o una meta
        if np.count_nonzero(copy_tablero == 2) > 1 or np.count_nonzero(copy_tablero == 3) > 1:
            messagebox.showerror("Editar Tablero", "El escenario debe tener un solo inicio y meta.", parent=ventana_edicion)
            return None
        tablero = np.copy(copy_tablero) 
        mostrar_tablero_en_canvas_mapa(tablero, inicio, meta)

        ventana_edicion.destroy()

    color_seleccionado = tk.StringVar()
    color_seleccionado.set("white")

    # Contenedor para los botones de color
    contenedor_selector_color = tk.Frame(ventana_edicion)
    contenedor_selector_color.grid(row=len(tablero) + 1, column=0, columnspan=len(tablero), pady=10)

    # Variable para rastrear la selección
    color_var = tk.StringVar()
    color_var.set("white")
    colores = ["blue", "green", "black", "white"]
    celda = ["Inicio", "Meta", "Obstáculo", "Vacío"]

    def guardar_color_seleccionado(color):
        color_var.set(color)

    for color in colores:
        radiobutton = tk.Radiobutton(
            contenedor_selector_color, 
            text=celda[colores.index(color)],
            variable=color_var, value=color,
            command=lambda color=color: guardar_color_seleccionado(color),
            borderwidth=2, relief="ridge", bg="gray", fg=color, selectcolor="gray", activeforeground=color, 
            font=("Arial", 10, "bold"))
        radiobutton.grid(row=0, column=colores.index(color), padx=10)

    # Contenedor para el botón de carga y guardado
    contenedor_botones = tk.Frame(ventana_edicion)
    contenedor_botones.grid(row=len(tablero) + 2, column=0, columnspan=len(tablero), pady=10)

    # Botón para limpiar el tablero
    limpiar_button = tk.Button(contenedor_botones, text="Limpiar", command=lambda: limpiar_tablero())
    limpiar_button.grid(row=0, column=1, padx=5)

    # Botón para guardar el tablero editado
    guardar_button = tk.Button(contenedor_botones, text="Terminar", command=guardar_escenario, font=("Arial", 9, "bold"))
    guardar_button.grid(row=0, column=0, padx=5)

    # Botón para guardar el tablero editado en un archivo txt
    guardar_txt_button = tk.Button(contenedor_botones, text="Guardar(txt)", command=lambda: guardar_tablero_en_txt(ventana_edicion, copy_tablero))
    guardar_txt_button.grid(row=0, column=2, padx=5)

    # Botón para cargar un tablero desde un archivo txt
    cargar_txt_button = tk.Button(contenedor_botones, text="Cargar(txt)", command=lambda: cargar_tablero_desde_txt(ventana_edicion))
    cargar_txt_button.grid(row=0, column=3, padx=5)

# Función para guardar el tablero editado en un archivo txt
def guardar_tablero_en_txt(ventana_edicion, copy_tablero):
    global tablero, tablero_edicion, inicio, meta

    if 2 not in copy_tablero or 3 not in copy_tablero:
            messagebox.showerror("Guardado de escenario", "El escenario debe tener un inicio y una meta.", parent=ventana_edicion)
            return None
    # comprobar que no haya mas de un inicio o una meta
    if np.count_nonzero(copy_tablero == 2) > 1 or np.count_nonzero(copy_tablero == 3) > 1:
        messagebox.showerror("Guardado de escenario", "El escenario debe tener un solo inicio y meta.", parent=ventana_edicion)
        return None
    
    
    # Guardar el tablero en un archivo txt en la carpeta "tableros"
    dir_path_tableros = dir_path+"/tableros"
    if not os.path.exists(dir_path_tableros):
        os.makedirs(dir_path_tableros)
    np.savetxt(f"{dir_path_tableros}/tablero_{len(tablero)}X{len(tablero)}-({inicio[1]},{inicio[0]})({meta[1]},{meta[0]}).txt", copy_tablero, fmt="%d")

    messagebox.showinfo("Guardado exitoso", "El escenario se guardó correctamente.", parent=ventana_edicion)

# Función para cargar un tablero desde un archivo txt
def cargar_tablero_desde_txt(ventana_edicion):
    global tablero, tablero_edicion, inicio, meta
    dir_path_tableros = dir_path+"/tableros"
    if not os.path.exists(dir_path_tableros):
        os.makedirs(dir_path_tableros)
    # ventana para seleccionar el archivo de tablero
    archivo_tablero = filedialog.askopenfilename(initialdir=dir_path_tableros, title="Seleccionar archivo de tablero", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    if archivo_tablero:
        # Si el archivo tiene caracteres no numericos, se muestra un mensaje de error
        try:
            # Obtener el tablero desde el archivo txt
            tablero = np.loadtxt(archivo_tablero).astype(int)
            # si inicio y meta no estan en el tablero, se muestra un mensaje de error
            if 2 not in tablero or 3 not in tablero:
                messagebox.showerror("Carga de escenario", "El archivo seleccionado no es un tablero válido  (no tiene inicio o meta).", parent=ventana_edicion)
                return None
            # si hay mas de un inicio o una meta, se muestra un mensaje de error
            if np.count_nonzero(tablero == 2) > 1 or np.count_nonzero(tablero == 3) > 1:
                messagebox.showerror("Carga de escenario", "El archivo seleccionado no es un tablero válido (tiene mas de un inicio o una meta).", parent=ventana_edicion)
                return None
            # si las filas y columnas del tablero no son iguales, se muestra un mensaje de error
            if tablero.shape[0] != tablero.shape[1]:
                messagebox.showerror("Carga de escenario", "El archivo seleccionado no es un tablero válido (no es cuadrado).", parent=ventana_edicion)
                return None
            inicio = np.where(tablero == 2)
            inicio = (inicio[0][0], inicio[1][0])
            meta = np.where(tablero == 3)
            meta = (meta[0][0], meta[1][0])
            # Donde hay valores diferentes de 0 y 1, se cambiaran por 0
            tablero[tablero > 3] = 0
            tablero[tablero < 0] = 0

            ventana_edicion.destroy()

            # Mostrar el tablero en el Canvas
            mostrar_tablero_en_canvas_mapa(tablero, inicio, meta)

        except ValueError:
            messagebox.showerror("Carga de escenario", "El archivo seleccionado no es un tablero válido (tiene caracteres no numéricos).", parent=ventana_edicion)
            return None

# Función para ejecutar los algoritmos de búsqueda
def buscar_ruta():
    global tablero, inicio, meta, trayectoria

    ruta_var.set("0")
    tiempo_var.set("0")
    resultados_var.set("")
    buscar_button.config(state="disabled")
    crear_escenario_button.config(state="disabled")
    editar_button.config(state="disabled")
    canvas.delete("all")
    mostrar_tablero_en_canvas_mapa(tablero, inicio, meta)


    # Obtener el algoritmo de búsqueda desde la interfaz gráfica
    algoritmo = algoritmo_var.get()

    # Ejecutar el algoritmo de búsqueda especificado
    if algoritmo == "DFS":
        trayectoria, tiempo_ejecucion = dfs(tablero, inicio, meta)
    elif algoritmo == "BFS":
        trayectoria, tiempo_ejecucion = bfs(tablero, inicio, meta)
    elif algoritmo == "BestF":
        trayectoria, tiempo_ejecucion = best_first_search(tablero, inicio, meta)
    elif algoritmo == "A*":
        trayectoria, tiempo_ejecucion = astar(tablero, inicio, meta)
    
    if trayectoria is None:
        resultados_var.set("No se encontró una ruta.")
        trayectoria = []

    print(f"\nAlgoritmo: {algoritmo}")
    print(f"Tiempo de ejecución: {round(tiempo_ejecucion, 4)} segundos")
    print(f"Longitud de la ruta: {len(trayectoria)} unidades")

    # Actualizar el tamaño de la ruta y el tiempo de ejecución en la interfaz gráfica
    ruta_var.set(str(len(trayectoria)))
    tiempo_var.set(str(round(tiempo_ejecucion, 4)))

    buscar_button.config(state="normal")
    crear_escenario_button.config(state="normal")
    editar_button.config(state="normal")

# Definir constantes para la dificultad
FACIL = 0
MEDIO = 1
DIFICIL = 2

# Variables globales
tablero = []
tablero_edicion = []
trayectoria = []
inicio = None
meta = None
ultimo_pintado = None

# Obtener la ubicacion
dir_path = os.path.dirname(os.path.realpath(__file__))

# Ventana principal de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Metodos de Búsqueda")
ancho_ventana = 820
alto_ventana = 610
x_ventana = ventana.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = ventana.winfo_screenheight() // 2 - alto_ventana // 2
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")
ventana.resizable(False, False)

# Canvas para mostrar el tablero
canvas = tk.Canvas(ventana, width=600, height=600)
canvas.grid(row=0, column=0, rowspan=30, padx=1, pady=1)

# Contenedor para el tamaño del tablero
tamaño_tablero_frame = tk.Frame(ventana)
tamaño_tablero_frame.grid(row=3, column=1, rowspan=1, columnspan=2, padx=1, pady=1)

# Campo de entrada para el tamaño del tablero
tamaño_tablero_label = tk.Label(tamaño_tablero_frame, text="Tamaño del tablero:", font=("Arial", 11, "normal"))
tamaño_tablero_label.grid(row=1, column=1, padx=1, pady=1)
tamaño_tablero_entry = tk.Entry(tamaño_tablero_frame, justify="center", width=5, font=("Arial", 11, "normal"))
tamaño_tablero_entry.grid(row=1, column=2, padx=1, pady=1)
tamaño_tablero_entry.insert(0, "20")

# Contenedor para las opciones de dificultad y algoritmo
opciones_frame = tk.Frame(ventana)
opciones_frame.grid(row=4, column=1, rowspan=1, columnspan=2, padx=1, pady=1)

# Opción para la dificultad
dificultad_label = tk.Label(opciones_frame, text="Dificultad:", font=("Arial", 11, "normal"))
dificultad_label.grid(row=1, column=1, padx=1, pady=1)
dificultad_var = tk.StringVar()
dificultad_var.set("Medio")
dificultad_optionmenu = tk.OptionMenu(opciones_frame, dificultad_var, "Fácil   ", "Medio", "Difícil ")
dificultad_optionmenu.grid(row=1, column=2, padx=1, pady=1)

# Opción para el algoritmo de búsqueda
algoritmo_label = tk.Label(opciones_frame, text="Algoritmo:", font=("Arial", 11, "normal"))
algoritmo_label.grid(row=2, column=1, padx=1, pady=1)
algoritmo_var = tk.StringVar()
algoritmo_var.set("DFS")
algoritmo_optionmenu = tk.OptionMenu(opciones_frame, algoritmo_var, "DFS", "BFS", "BestF", "A*")
algoritmo_optionmenu.grid(row=2, column=2, padx=1, pady=1)

# Contenedor para las opciones de la ruta
ruta_frame = tk.Frame(ventana)
ruta_frame.grid(row=7, column=1, rowspan=1, columnspan=2, padx=1, pady=1)

# Opciones de ruta
gradiente_ruta_label = tk.Label(ruta_frame, text="Gradiente en ruta:", font=("Arial", 11, "normal"))
gradiente_ruta_label.grid(row=1, column=1, padx=1, pady=1)
gradiente_ruta_var = tk.BooleanVar()
gradiente_ruta_var.set(True)
gradiente_ruta_checkbutton = tk.Checkbutton(ruta_frame, variable=gradiente_ruta_var)
gradiente_ruta_checkbutton.grid(row=1, column=2, padx=1, pady=1)

flecha_ruta_label = tk.Label(ruta_frame, text="Flechas en ruta:", font=("Arial", 11, "normal"))
flecha_ruta_label.grid(row=2, column=1, padx=1, pady=1)
flecha_ruta_var = tk.BooleanVar()
flecha_ruta_var.set(True)
flecha_ruta_checkbutton = tk.Checkbutton(ruta_frame, variable=flecha_ruta_var)
flecha_ruta_checkbutton.grid(row=2, column=2, padx=1, pady=1)

# Contenedor de configuracion de velocidad
velocidad_frame = tk.Frame(ventana)
velocidad_frame.grid(row=8, column=1, rowspan=1, columnspan=2, padx=1, pady=0)

# Opciones de velocidad
velocidad_label = tk.Label(velocidad_frame, text="Velocidad:", font=("Arial", 11, "normal"))
velocidad_label.grid(row=1, column=1, padx=1, pady=1)
velocidad_var = tk.IntVar()
velocidad_var.set(15)
velocidad_scale = tk.Scale(velocidad_frame, variable=velocidad_var, from_=1, to=100, orient=tk.HORIZONTAL, length=100,showvalue=False)
velocidad_scale.grid(row=1, column=2, padx=1, pady=1)

# Botón para crear un escenario
crear_escenario_button = tk.Button(ventana, text="Nuevo escenario", command=crear_escenario, font=("Arial", 11, "normal"))
crear_escenario_button.grid(row=11, column=1, columnspan=2, padx=1, pady=1)

# Botón para editar el tablero
editar_button = tk.Button(ventana, text="Editar escenario", command=abrir_ventana_edicion, font=("Arial", 11, "normal"))
editar_button.grid(row=12, column=1, columnspan=2, padx=1, pady=1)

# Botón para ejecutar el algoritmo de búsqueda
buscar_button = tk.Button(ventana, text="Buscar", command=buscar_ruta, font=("Arial", 11, "bold"))
buscar_button.grid(row=13, column=1, columnspan=2, padx=1, pady=1)

# Resultados
resultados_var = tk.StringVar()
resultados_var.set("")
resultados_label = tk.Label(ventana, textvariable=resultados_var, justify="left", font=("Arial", 10, "bold"))
resultados_label.grid(row=15, column=1, columnspan=2, padx=1, pady=1)

# Resultados tamaño de la ruta
ruta_label = tk.Label(ventana, text="Longitud de ruta:", font=("Arial", 10, "bold"))
ruta_label.grid(row=27, column=1, padx=1, pady=1)
ruta_var = tk.StringVar()
ruta_var.set("0")
ruta_entry = tk.Entry(ventana, state="readonly",justify="center", width=7, textvariable=ruta_var, font=("Arial", 11, "bold"))
ruta_entry.grid(row=27, column=2, padx=1, pady=1)

# Resultados tiempo de ejecución
tiempo_label = tk.Label(ventana, text="Tiempo de ejecución:", font=("Arial", 10, "bold"))
tiempo_label.grid(row=28, column=1, padx=1, pady=1)
tiempo_var = tk.StringVar()
tiempo_var.set("0")
tiempo_entry = tk.Entry(ventana, state="readonly",justify="center", width=7, textvariable=tiempo_var, font=("Arial", 11, "bold"))
tiempo_entry.grid(row=28, column=2, padx=1, pady=1)

# Crear un tablero inicial
crear_tablero(20, MEDIO)
mostrar_tablero_en_canvas_mapa(tablero, inicio, meta)

ventana.mainloop()

