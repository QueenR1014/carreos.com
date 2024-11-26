import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import deque
import heapq
import time
import csv
# =======================
# Configuración del tablero
# =======================
def guardar_csv(nombre_archivo, datos, campos):
    """Guardar los datos en un archivo CSV."""
    with open(nombre_archivo, mode='a', newline='') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos)
        if archivo.tell() == 0:  # Si el archivo está vacío, escribe los encabezados.
            writer.writeheader()
        for dato in datos:
            writer.writerow(dato)

def crear_tablero(tamaño=10):
    tablero = nx.grid_2d_graph(tamaño, tamaño)
    nx.set_node_attributes(tablero, (0,0), 'pos')
    nx.set_node_attributes(tablero, 'azul', 'color')  # Color inicial de las casillas
    nx.set_node_attributes(tablero, None, 'barco')   # Indica si el nodo contiene un barco
    nx.set_node_attributes(tablero, 0.0, 'probabilidad')  # Probabilidad inicial de 0
    for node in tablero.nodes:
        tablero.nodes[node]['pos'] = node
    return tablero

def mostrar_tablero(tablero):
    color_map = {
        'azul': 'blue',
        'rojo': 'red',
        'verde': 'green',
        'gris': 'gray',
        'amarillo': 'yellow',
        'naranja': 'orange',
        'morado': 'purple',
        'cian': 'cyan'
    }
    colores = [color_map[tablero.nodes[nodo]['color']] for nodo in tablero.nodes()]
    pos = {(x, y): (x, -y) for x, y in tablero.nodes()}
    plt.clf()
    nx.draw(tablero, pos, node_color=colores, with_labels=False, node_size=500, edge_color='gray')
    plt.show()

def reiniciar_colores(tablero):
    for nodo in tablero.nodes():
        if tablero.nodes[nodo]['barco']:
            tablero.nodes[nodo]['color'] = 'rojo'
        else:
            tablero.nodes[nodo]['color'] = 'azul'

# =======================
# Colocación de barcos con restricciones
# =======================
def verificar_adyacencia(tablero, nodos):
    for nodo in nodos:
        vecinos = list(tablero.neighbors(nodo))
        for vecino in vecinos:
            if tablero.nodes[vecino]['barco']:
                return False
    return True

def colocar_barco_optimo(tablero, tamaño, color_barco):
    while True:
        orientacion = random.choice(['horizontal', 'vertical'])
        x, y = random.randint(0, 9), random.randint(0, 9)

        if orientacion == 'horizontal' and x + tamaño <= 10:
            nodos = [(x + i, y) for i in range(tamaño)]
        elif orientacion == 'vertical' and y + tamaño <= 10:
            nodos = [(x, y + i) for i in range(tamaño)]
        else:
            continue

        if all(tablero.nodes[nodo]['color'] == 'azul' for nodo in nodos) and verificar_adyacencia(tablero, nodos):
            for nodo in nodos:
                tablero.nodes[nodo]['color'] = color_barco
                tablero.nodes[nodo]['barco'] = True
            break

# =======================
# Actualización de probabilidades
# =======================
def actualizar_probabilidades(tablero, disparo, impacto):
    """
    Actualiza las probabilidades de los nodos adyacentes según el resultado del disparo.
    """
    for vecino in tablero.neighbors(disparo):
        if impacto:
            tablero.nodes[vecino]['probabilidad'] += 0.3  # Incrementar si hay impacto
        else:
            tablero.nodes[vecino]['probabilidad'] -= 0.1  # Reducir si no hay impacto
        # Limitar la probabilidad entre 0 y 1
        tablero.nodes[vecino]['probabilidad'] = max(0.0, min(1.0, tablero.nodes[vecino]['probabilidad']))

def dijkstra_para_barcos(tablero, visitados, casillas_pendientes, partes_encontradas, total_partes_barcos):
    """
    Dijkstra para seleccionar el siguiente nodo a explorar basado en probabilidades dinámicas.
    """
    while partes_encontradas < total_partes_barcos:  # Solo sigue mientras no haya encontrado todas las partes
        probabilidades = nx.get_node_attributes(tablero, 'probabilidad')
        heap = [(-prob, nodo) for nodo, prob in probabilidades.items() if nodo not in visitados]  # Prioridad inversa
        heapq.heapify(heap)

        if not heap:  # Si no hay nodos restantes con probabilidades positivas
            break

        prob, nodo_actual = heapq.heappop(heap)
        prob = -prob  # Revertir el signo para obtener la probabilidad positiva
        print(f"Dijkstra explora: {nodo_actual} con probabilidad {prob:.2f}")

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)

            if tablero.nodes[nodo_actual]['barco']:
                tablero.nodes[nodo_actual]['color'] = 'verde'
                casillas_pendientes.append(nodo_actual)
                actualizar_probabilidades(tablero, nodo_actual, impacto=True)
                partes_encontradas += 1
            else:
                tablero.nodes[nodo_actual]['color'] = 'gris'
                actualizar_probabilidades(tablero, nodo_actual, impacto=False)

            #mostrar_tablero(tablero)

    return partes_encontradas

def dfs_para_barcos(tablero, inicio, visitados, casillas_pendientes, partes_encontradas, total_partes_barcos):
    pila = [inicio]
    while pila and partes_encontradas < total_partes_barcos:
        nodo_actual = pila.pop()
        print(f"DFS explora: {nodo_actual}")
        for vecino in tablero.neighbors(nodo_actual):
            if vecino not in visitados:
                visitados.add(vecino)
                if tablero.nodes[vecino]['barco']:
                    tablero.nodes[vecino]['color'] = 'verde'
                    casillas_pendientes.append(vecino)
                    partes_encontradas += 1
                else:
                    tablero.nodes[vecino]['color'] = 'gris'
                mostrar_tablero(tablero)
    return partes_encontradas
# =======================
# Algoritmo principal
# =======================
def ataque(tablero, estrategia):
    
    visitados = set()
    casillas_pendientes = deque()
    total_partes_barcos = sum(1 for nodo in tablero.nodes if tablero.nodes[nodo]['barco'])
    partes_encontradas = 0
    coord_memoria = []
    visitados_memoria = []
    disparos = 0
    inicio_tiempo = time.time()

    #plt.figure()
    #contador test
    count = 0
    while partes_encontradas < total_partes_barcos:
        
        coord_encontradas = []
        if casillas_pendientes:
            inicio = casillas_pendientes.popleft()
            if estrategia == 'BFS':
                partes_encontradas, coord_encontradas = bfs_para_barcos(tablero, inicio, visitados, casillas_pendientes, partes_encontradas,coord_encontradas, total_partes_barcos)
            elif estrategia == 'DFS':
                partes_encontradas = dfs_para_barcos(tablero, inicio, visitados, casillas_pendientes, partes_encontradas, total_partes_barcos)
            elif estrategia == 'Dijkstra':
                partes_encontradas = dijkstra_para_barcos(tablero, visitados, casillas_pendientes, partes_encontradas, total_partes_barcos)
            
        else:
            disparo = disparo_aleatorio(tablero, visitados)
            if disparo:
                disparos += 1
                visitados.add(disparo)
                impacto = tablero.nodes[disparo]['barco']
                actualizar_probabilidades(tablero, disparo, impacto)
                if impacto:
                    tablero.nodes[disparo]['color'] = 'verde'
                    casillas_pendientes.append(disparo)
                    partes_encontradas += 1
                else:
                    tablero.nodes[disparo]['color'] = 'gris'
                #mostrar_tablero(tablero)
        count += 1
        coord_memoria.append(coord_encontradas)
        visitados_memoria.append(list(visitados))

    print(f"solución en {count} pasos")
    tiempo_total = time.time() - inicio_tiempo
    #plt.show()
    # Guardar en CSV en cada iteración
    #coord_data = [{'x': coord[0], 'y': coord[1]} for coord in coord_encontradas]
    #visitados_data = [{'x': coord[0], 'y': coord[1]} for coord in visitados]
    
    #guardar_csv('coordenadas_encontradas.csv', coord_data, campos_coord)
    #guardar_csv('visitados.csv', visitados_data, campos_visitados)
    print(f'VÉRTICES VISITADOS TOTAL: {len(visitados)}')
    return disparos, tiempo_total, partes_encontradas / disparos, coord_memoria, visitados_memoria

def disparo_aleatorio(tablero, visitados):
    posibles = [nodo for nodo in tablero.nodes if nodo not in visitados]
    return random.choice(posibles) if posibles else None


def bfs_para_barcos(tablero, inicio, visitados, casillas_pendientes, partes_encontradas,coordenadas_memoria,total_partes_barcos):
    cola = deque([inicio])
    while cola and partes_encontradas < total_partes_barcos:
        nodo_actual = cola.popleft()
        print(f"BFS explora: {nodo_actual}")
        for vecino in tablero.neighbors(nodo_actual):
            if vecino not in visitados:
                visitados.add(vecino)
                
                if tablero.nodes[vecino]['barco']:
                    coordenadas_memoria.append(tablero.nodes[vecino]['pos'])
                    tablero.nodes[vecino]['color'] = 'verde'
                    casillas_pendientes.append(vecino)
                    partes_encontradas += 1
                else:
                    tablero.nodes[vecino]['color'] = 'gris'
                #mostrar_tablero(tablero)
    return partes_encontradas, coordenadas_memoria
# =======================
# Ejecución del programa
# =======================
# Crear tablero y colocar barcos
tablero = crear_tablero()
colores_barcos = ['amarillo', 'naranja', 'morado', 'cian']
tamaños_barcos = [5, 4, 3, 2]
for tamaño, color in zip(tamaños_barcos, colores_barcos):
    colocar_barco_optimo(tablero, tamaño, color)

# Inicializar probabilidades
reiniciar_colores(tablero)

# Ejecutar estrategia Dijkstra
print("\nEstrategia Dijkstra:")
#disparos, tiempo_total, precision = ataque(tablero, 'BFS')

# Resultados
"""print("\nResultados:")
print(f"Disparos totales: {disparos}")
print(f"Tiempo total: {tiempo_total:.2f} segundos")
print(f"Precisión: {precision * 100:.2f}%")"""
