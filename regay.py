import pygame 
import random
import time

# =======================
# Configuración del tablero
# =======================
def crear_tablero(tamaño=10):
    tablero = [[{'color': 'azul', 'barco': False} for _ in range(tamaño)] for _ in range(tamaño)]
    return tablero

def colocar_barco_optimo(tablero, tamaño):
    while True:
        orientacion = random.choice(['horizontal', 'vertical'])
        x, y = random.randint(0, len(tablero) - 1), random.randint(0, len(tablero) - 1)

        if orientacion == 'horizontal' and x + tamaño <= len(tablero):
            nodos = [(x + i, y) for i in range(tamaño)]
        elif orientacion == 'vertical' and y + tamaño <= len(tablero):
            nodos = [(x, y + i) for i in range(tamaño)]
        else:
            continue

        if all(tablero[nodo[1]][nodo[0]]['color'] == 'azul' for nodo in nodos):
            for nodo in nodos:
                tablero[nodo[1]][nodo[0]]['color'] = 'rojo'
                tablero[nodo[1]][nodo[0]]['barco'] = True
            break

# =======================
# Dibujar tablero en Pygame
# =======================
def dibujar_tablero(screen, tablero, tamaño_celda):
    colores = {
        'azul': (0, 0, 255),
        'rojo': (255, 0, 0),
        'verde': (0, 255, 0),
        'gris': (200, 200, 200)
    }
    for y, fila in enumerate(tablero):
        for x, celda in enumerate(fila):
            color = colores[celda['color']]
            pygame.draw.rect(screen, color, (x * tamaño_celda, y * tamaño_celda, tamaño_celda, tamaño_celda))
            pygame.draw.rect(screen, (0, 0, 0), (x * tamaño_celda, y * tamaño_celda, tamaño_celda, tamaño_celda), 1)

# =======================
# Simulación de ataque
# =======================
def ataque(tablero, estrategia):
    visitados = set()
    frontera = [(0, 0)]
    pasos = []
    barcos_encontrados = 0
    total_barcos = sum(1 for fila in tablero for celda in fila if celda['barco'])

    while barcos_encontrados < total_barcos and frontera:
        nodo = frontera.pop(0) if estrategia == 'BFS' else frontera.pop()
        if nodo in visitados:
            continue

        x, y = nodo
        visitados.add(nodo)
        pasos.append(nodo)

        if tablero[y][x]['barco']:
            tablero[y][x]['color'] = 'verde'
            barcos_encontrados += 1
        else:
            tablero[y][x]['color'] = 'gris'

        vecinos = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                   if 0 <= x + dx < len(tablero) and 0 <= y + dy < len(tablero)]
        frontera.extend([v for v in vecinos if v not in visitados])

        yield pasos  # Generar pasos para la animación

# =======================
# Animar en Pygame
# =======================
def animar_ataque(tablero, pasos, tamaño_celda=50):
    pygame.init()
    tamaño = len(tablero) * tamaño_celda
    screen = pygame.display.set_mode((tamaño, tamaño))
    pygame.display.set_caption("Simulación de Ataque")

    for paso in pasos:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((255, 255, 255))
        dibujar_tablero(screen, tablero, tamaño_celda)
        pygame.display.flip()
        time.sleep(0.5)  # Pausa entre pasos

    time.sleep(2)  # Espera antes de cerrar la ventana
    pygame.quit()

# =======================
# Ejecución del programa
# =======================
if __name__ == "__main__":
    tamaño_tablero = 10
    tablero = crear_tablero(tamaño_tablero)
    tamaños_barcos = [5, 4, 3, 2]

    for tamaño in tamaños_barcos:
        colocar_barco_optimo(tablero, tamaño)

    print("Iniciando animación con BFS...")
    pasos_bfs = list(ataque(tablero, 'BFS'))
    animar_ataque(tablero, pasos_bfs)

