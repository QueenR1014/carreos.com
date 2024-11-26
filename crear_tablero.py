from manim import *
import algoritmos as al
grid = NumberPlane(
    x_range=[1, 10, 1],
    y_range=[1, 10, 1],
    x_length=5,
    y_length=5,
    background_line_style={
        "stroke_color": WHITE,
        "stroke_width": 2,
        "stroke_opacity": 1,
    }
)
edges = Square(side_length=5, stroke_opacity=0.5, color=WHITE, stroke_width=2)
grid.shift(ORIGIN - grid.get_center())

#OBJETO TABLERO
tablero = VGroup(edges, grid)

x_o = 1
y_0 = 1
circles = VGroup()
circle_positions = {}
for i in range(10):
    for j in range(10):
        position = grid.c2p(i + x_o, j + y_0)
        circle = Dot(color=BLUE, radius=0.1).move_to(position)
        circles.add(circle)
        circle_positions[(i, j)] = circle

# Mostrar la cuadrícula

# Colocar barcos (nodos rojos)
size_ship4 = [(2, 3), (3, 3), (4, 3), (5, 3)]
size_ship2 = [(9, 1), (9, 2)]
size_ship3 = [(1, 7), (1, 8), (1, 9)]
size_ship5 = [(4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]

ship_positions = size_ship4 + size_ship2 + size_ship3 + size_ship5
ships = [size_ship2,size_ship3,size_ship4,size_ship5]
total_parts = len(ship_positions)

for ship in ships:
    Vship = VGroup()
    for coord in ship:
        circle = circle_positions[coord]
        Vship.add(circle)

#BSF
tablero_juego = al.crear_tablero(10)
def colocar_barcos(tablero, color_barco):
    if all(tablero.nodes[nodo]['color'] == 'azul' for nodo in ship_positions) and al.verificar_adyacencia(tablero, ship_positions):
            for nodo in ship_positions:
                x,y = nodo
                real_y = abs(y - 9)
                tablero.nodes[(x,real_y)]['color'] = color_barco
                tablero.nodes[(x,real_y)]['barco'] = True

colocar_barcos(tablero_juego,'rojo')
resultado = al.ataque(tablero_juego, 'BFS')
visitados_memoria = resultado[-1]
coord_memoria = resultado[-2]
#print(len(visitados_memoria),len(coord_memoria))
#print(f'coordenadas antes: {coord_memoria}')
#print(type(visitados_memoria))
for i in range(len(visitados_memoria)-1,0,-1):
        prev_list = visitados_memoria[i - 1]
        curr_list = visitados_memoria[i]
        #print(prev_list,curr_list)
        holder = []
        for nodo in curr_list:
            if nodo not in prev_list:
                holder.append(nodo)      
        visitados_memoria[i] = holder
#print(visitados_memoria)
count = 0
for instance in visitados_memoria:
    for nodo in instance:
         count += 1
#print(count)
for instancia in visitados_memoria:
    for i in range(len(instancia)):
        x,y = instancia[i]
        realy = abs(y-9)
        nodo = x, realy
        instancia[i] = nodo


for instancia in coord_memoria:
   for i in range(len(instancia)):
        x,y = instancia[i]
        realy = abs(y-9)
        nodo = x, realy
        instancia[i] = nodo

#print(visitados_memoria)
print(f'coordenadas encontradas: \n {coord_memoria}')
#print(tablero_juego.nodes)
#al.mostrar_tablero(tablero_juego)
"""for nodo in ship_positions:
    print(tablero.nodes[nodo]['color'])"""
                
for i in range(0,len(visitados_memoria)):
    instancia = visitados_memoria[i]
    encontrados = coord_memoria[i]
    if len(encontrados) == 0:
        #Solo se visitó vértice
        visitado = instancia[0]
        try:
            if visitado in encontrados[i+1]:
                print(f'visito {visitado} y encontré')
        except:
            print(f'visito {visitado} y no encontré')


    else:
        for visitado in instancia:
            if visitado in encontrados:
                print(f'visito {visitado} y encontré')
            else:
                print(f'visito {visitado} y no encontré')