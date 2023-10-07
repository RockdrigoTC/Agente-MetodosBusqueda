import numpy as np
import random
import time
import heapq
import tkinter as tk

# Definir constantes para la dificultad
FACIL = 0
MEDIO = 1
DIFICIL = 2

tablero = None
tablero_edicion = None
inicio = None
meta = None

# Función para crear un tablero de N x N con obstáculos
def crear_tablero(N, dificultad):
    global tablero, tablero_edicion, inicio, meta
    tablero = np.zeros((N, N), dtype=int)
    
    num_obstaculos = 0

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

    # Si el nodo no esta en la primera columna, agregar el vecino de la izquierda
    if columna > 0 and tablero[fila][columna - 1] != 1:
        vecinos.append((fila, columna - 1))

    # Si el nodo no esta en la última fila, agregar el vecino de abajo
    if fila < N - 1 and tablero[fila + 1][columna] != 1:
        vecinos.append((fila + 1, columna))
    
    return vecinos


def obtener_vecinosDFS(tablero, nodo):
    # Obtener el tamaño del tablero
    N = len(tablero)
    
    # Obtener la fila y columna del nodo
    fila, columna = nodo
    
    # Crear una lista para almacenar los vecinos
    vecinos = []
    
    # Si el nodo no esta en la primera fila, agregar el vecino de arriba
    if fila > 0 and tablero[fila - 1][columna] != 1:
        vecinos.append(((fila - 1, columna), 0))
    
    # Si el nodo no esta en la última columna, agregar el vecino de la derecha
    if columna < N - 1 and tablero[fila][columna + 1] != 1:
        vecinos.append(((fila, columna + 1), 1))

    # Si el nodo no esta en la primera columna, agregar el vecino de la izquierda
    if columna > 0 and tablero[fila][columna - 1] != 1:
        vecinos.append(((fila, columna - 1), 2))

    # Si el nodo no esta en la última fila, agregar el vecino de abajo
    if fila < N - 1 and tablero[fila + 1][columna] != 1:
        vecinos.append(((fila + 1, columna), 3))
    
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
    
    # Agregar el nodo inicial a la pila
    pila.append(inicio)
    
    # Mientras la pila no este vacia
    while len(pila) > 0:
        # Extraer el nodo de la pila
        nodo = pila.pop()
        
        # Si el nodo no ha sido visitado
        if nodo not in visitados:
            # Marcar el nodo como visitado
            visitados[nodo] = True
            
            # Si el nodo es la meta, retornar la trayectoria
            if nodo == meta:
                mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()), True)
                return list(visitados.keys()), time.perf_counter() - inicio_tiempo
            
            # Obtener los vecinos del nodo
            vecinos = obtener_vecinos(tablero, nodo)
            
            # Agregar los vecinos a la pila
            pila.extend(vecinos)

            esperar(tablero)
            mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()))
    
    # Si no se encontró una trayectoria, retornar None
    mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()), False)
    return None, time.perf_counter() - inicio_tiempo


# Algoritmo de Depth-First Search (DFS). Siempre visita al vecino de la derecha recursivamente, después al de abajo, luego al de la izquierda y por último al de arriba, como si recorriera un arnol en preorden
def dfs2(tablero, inicio, meta):

    # Iniciar el tiempo de ejecución
    inicio_tiempo = time.perf_counter()

    # Obtener el tamaño del tablero
    N = len(tablero)

    # Pila para almacenar los nodos
    pila = []

    # Diccionario para almacenar los nodos visitados
    visitados = {}

    # Agregar el nodo inicial a la pila
    pila.append(inicio)

    # Definir el orden de prioridad para las direcciones
    direcciones_prioridad = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Izquierda, abajo, derecha, arriba

    # Mientras la pila no esté vacía
    while pila:
        # Obtener el nodo actual de la pila
        nodo_actual = pila[-1]

        # Si el nodo actual es la meta, retornar la trayectoria
        if nodo_actual == meta:
            trayectoria = list(pila)
            return trayectoria, time.perf_counter() - inicio_tiempo

        # Si el nodo actual no ha sido visitado
        if nodo_actual not in visitados:
            # Marcar el nodo actual como visitado
            visitados[nodo_actual] = True

            # Encontrar la próxima dirección prioritaria para explorar
            siguiente_direccion = None
            for direccion in direcciones_prioridad:
                vecino = (nodo_actual[0] + direccion[0], nodo_actual[1] + direccion[1])
                if (
                    0 <= vecino[0] < N
                    and 0 <= vecino[1] < N
                    and tablero[vecino[0]][vecino[1]] == 0
                    and vecino not in visitados
                ):
                    siguiente_direccion = direccion
                    break

            if siguiente_direccion:
                # Agregar el siguiente vecino a la pila
                siguiente_nodo = (nodo_actual[0] + siguiente_direccion[0], nodo_actual[1] + siguiente_direccion[1])
                pila.append(siguiente_nodo)
            else:
                # Si no hay vecinos en la dirección prioritaria, retroceder
                pila.pop()
        else:
            # Si el nodo actual ya ha sido visitado, retroceder
            pila.pop()

        esperar(tablero)
        mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()))

    # Si no se encontró una trayectoria, retornar None
    mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()), False)
    return None, time.perf_counter() - inicio_tiempo



# Función de Best-First Search (BFS)
def best_first_search(tablero, inicio, meta):

    # Iniciar el tiempo de ejecución
    inicio_tiempo = time.perf_counter()

    # Cola de prioridad para almacenar los nodos
    cola_prioridad = []
    
    # Diccionario para almacenar los nodos visitados
    visitados = {}
    
    # Agregar el nodo inicial a la cola de prioridad
    cola_prioridad.append((inicio, distancia_manhattan(inicio, meta)))
    
    # Mientras la cola de prioridad no esté vacía
    while len(cola_prioridad) > 0:
        # Extraer el nodo de la cola de prioridad
        nodo, _ = cola_prioridad.pop(0)
        
        # Si el nodo no ha sido visitado
        if nodo not in visitados:
            # Marcar el nodo como visitado
            visitados[nodo] = True
            
            # Si el nodo es la meta, retornar la trayectoria
            if nodo == meta:
                mostrar_tablero_en_canvas(tablero, inicio, meta, list(visitados.keys()), True)
                return list(visitados.keys()), time.perf_counter() - inicio_tiempo
            
            # Obtener los vecinos del nodo
            vecinos = obtener_vecinos(tablero, nodo)
            
            # Agregar los vecinos a la cola de prioridad
            for vecino in vecinos:
                distancia_hasta_meta = distancia_manhattan(vecino, meta)
                cola_prioridad.append((vecino, distancia_hasta_meta))
            
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


# Función para mostrar el tablero y la ruta en el lienzo (Canvas)
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
                canvas.create_rectangle(x1, y1, x2, y2, fill="orange", outline="black")
            elif tablero[fila][columna] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
            elif ruta and (fila, columna) in ruta:
                if exito is None:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")
                elif exito:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")
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
    if dificultad == "Fácil":
        dificultad = FACIL
    elif dificultad == "Medio": 
        dificultad = MEDIO
    elif dificultad == "Difícil":
        dificultad = DIFICIL

    # Crear un tablero con el tamaño y dificultad especificados
    tablero, inicio, meta = crear_tablero(tamaño_tablero, dificultad)
    
    # Mostrar el tablero en el Canvas
    mostrar_tablero_en_canvas(tablero, inicio, meta)    


# Función para editar el tablero
def editar_tablero():
    global tablero, tablero_edicion, inicio, meta

    if tablero_edicion is None:
        tablero_edicion = np.ndarray((10, 10), dtype=str)
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
    # Obtener el algoritmo de búsqueda desde la interfaz gráfica
    algoritmo = algoritmo_var.get()

    # Ejecutar el algoritmo de búsqueda especificado
    if algoritmo == "DFS":
        trayectoria, tiempo_ejecucion = dfs2(tablero, inicio, meta)
    elif algoritmo == "BFS":
        trayectoria, tiempo_ejecucion = best_first_search(tablero, inicio, meta)
    elif algoritmo == "A*":
        trayectoria, tiempo_ejecucion = astar(tablero, inicio, meta)
    
    print(f"Algoritmo: {algoritmo}")
    print(f"Tiempo de ejecución: {tiempo_ejecucion} segundos")


# Ventana principal de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Algoritmos de Búsqueda")

# Campo de entrada para el tamaño del tablero
tamaño_tablero_label = tk.Label(ventana, text="Tamaño del tablero:")
tamaño_tablero_label.pack()
tamaño_tablero_entry = tk.Entry(ventana, justify="center", width=5)
tamaño_tablero_entry.pack()
tamaño_tablero_entry.insert(0, "10")

# Opción para la dificultad
dificultad_label = tk.Label(ventana, text="Dificultad:")
dificultad_label.pack()
dificultad_var = tk.StringVar()
dificultad_var.set("Fácil")
dificultad_optionmenu = tk.OptionMenu(ventana, dificultad_var, "Fácil", "Medio", "Difícil")
dificultad_optionmenu.pack()

# Botón para crear un escenario
ejecutar_button = tk.Button(ventana, text="Nuevo escenario", command=crear_escenario)
ejecutar_button.pack()

# Botón para editar el tablero
editar_button = tk.Button(ventana, text="Editar escenario", command=editar_tablero)
editar_button.pack()

# Opción para el algoritmo de búsqueda
algoritmo_label = tk.Label(ventana, text="Algoritmo:")
algoritmo_label.pack()
algoritmo_var = tk.StringVar()
algoritmo_var.set("DFS")
algoritmo_optionmenu = tk.OptionMenu(ventana, algoritmo_var, "DFS", "BFS", "A*")
algoritmo_optionmenu.pack()

# Botón para ejecutar el algoritmo de búsqueda. fuente por defecto en negrita en negrita
buscar_button = tk.Button(ventana, text="Buscar", command=buscar_ruta, font=("Arial", 11, "bold"))
buscar_button.pack()

# Canvas para mostrar el tablero
canvas = tk.Canvas(ventana, width=500, height=500)
canvas.pack()

# Crear un tablero inicial
crear_tablero(10, FACIL)
mostrar_tablero_en_canvas(tablero, inicio, meta)

# Iniciar la interfaz gráfica
ventana.mainloop()
