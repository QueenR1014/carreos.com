from manim import * 
import random
import heapq
from collections import deque
from crear_tablero import tablero, circles, circle_positions, ships, coord_memoria, visitados_memoria

class BS(Scene):
    def construct(self):
        # Mostrar la cuadrícula
        self.play(Create(tablero))
        self.wait(1)
        self.play(Create(circles))
        # Colocar barcos (nodos rojos)
        for ship in ships:
            Vship = VGroup()
            for coord in ship:
                circle = circle_positions[coord]
                Vship.add(circle)
            self.play(Vship.animate.set_color(RED))    
        self.wait(5)

        """# Añadir el contador visual
        counter = MathTex("Partes encontradas: 0", font_size=36)
        counter.to_corner(UL)
        self.add(counter)

        def update_counter(count):
            new_counter = MathTex(f"Partes encontradas: {count}", font_size=36)
            new_counter.to_corner(UL)
            self.play(Transform(counter, new_counter))

        # Mostrar las casillas exploradas
        def color_cell(node, color):
            self.play(circle_positions[node].animate.set_color(color))

        # Algoritmos de búsqueda
        def bfs_para_barcos(start_node):
            visited = set()
            queue = deque([start_node])
            parts_found = 0
            while queue and parts_found < total_parts:
                current_node = queue.popleft()
                for neighbor in get_neighbors(current_node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        if neighbor in ship_positions:
                            color_cell(neighbor, GREEN)
                            parts_found += 1
                            update_counter(parts_found)
                        else:
                            color_cell(neighbor, GRAY)
                        queue.append(neighbor)

        def dfs_para_barcos(start_node):
            visited = set()
            stack = [start_node]
            parts_found = 0
            while stack and parts_found < total_parts:
                current_node = stack.pop()
                for neighbor in get_neighbors(current_node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        if neighbor in ship_positions:
                            color_cell(neighbor, GREEN)
                            parts_found += 1
                            update_counter(parts_found)
                        else:
                            color_cell(neighbor, GRAY)
                        stack.append(neighbor)

        def dijkstra_para_barcos():
            visited = set()
            parts_found = 0
            probabilities = {pos: random.random() for pos in circle_positions.keys()}
            heap = [(-prob, node) for node, prob in probabilities.items()]
            heapq.heapify(heap)

            while heap and parts_found < total_parts:
                prob, current_node = heapq.heappop(heap)
                if current_node in visited:
                    continue
                visited.add(current_node)

                if current_node in ship_positions:
                    color_cell(current_node, GREEN)
                    parts_found += 1
                    update_counter(parts_found)
                else:
                    color_cell(current_node, GRAY)

        # Obtener vecinos válidos
        def get_neighbors(node):
            x, y = node
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            return [n for n in neighbors if n in circle_positions]

        # Resolver el problema con los algoritmos
        # Ejecutar BFS
        start_node = random.choice(ship_positions)
        self.play(Indicate(circle_positions[start_node]))
        bfs_para_barcos(start_node)
        self.wait(2)

        # Resetear el tablero para DFS
        for circle in circle_positions.values():
            self.play(circle.animate.set_color(BLUE))
        for circle in ship_positions:
            self.play(circle_positions[circle].animate.set_color(RED))
        update_counter(0)

        # Ejecutar DFS
        self.play(Indicate(circle_positions[start_node]))
        dfs_para_barcos(start_node)
        self.wait(2)

        # Resetear el tablero para Dijkstra
        for circle in circle_positions.values():
            self.play(circle.animate.set_color(BLUE))
        for circle in ship_positions:
            self.play(circle_positions[circle].animate.set_color(RED))
        update_counter(0)

        # Ejecutar Dijkstra
        dijkstra_para_barcos()
        self.wait(2)

        # Limpiar la escena
        self.play(FadeOut(tablero), FadeOut(circles), FadeOut(counter))
        self.wait(1)

"""

class BFS(Scene):
    def construct(self):
        self.add(tablero)
        for ship in ships:
            Vship = VGroup()
            for coord in ship:
                circle = circle_positions[coord]
                circle.set_color(RED)


        self.add(circles)
        self.wait(3)

        pointer = Circle(radius=0.3)
        for i in range(0,len(visitados_memoria)):
            instancia = visitados_memoria[i]
            encontrados = coord_memoria[i]
            if len(encontrados) == 0:
                #Solo se visitó vértice
                visitado = instancia[0]
                try:
                    if visitado in encontrados[i+1]:
                        print(f'visito {visitado} y encontré')
                        pointer.move_to(circle_positions[visitado].get_center())
                        pointer.set_color(GREEN)
                        self.add(pointer)
                        self.play(circle_positions[visitado].animate.set_color(GREEN))
                    else:
                        print(f'visito {visitado} y no encontré')
                        pointer.move_to(circle_positions[visitado].get_center())
                        pointer.set_color(RED)
                        self.add(pointer)
                        self.play(circle_positions[visitado].animate.set_color(YELLOW))
                except:
                    print(f'visito {visitado} y no encontré')
                    pointer.move_to(circle_positions[visitado].get_center())
                    pointer.set_color(RED)
                    self.add(pointer)
                    self.play(circle_positions[visitado].animate.set_color(YELLOW))
            else:
                for visitado in instancia:
                    if visitado in encontrados:
                        print(f'visito {visitado} y encontré')
                        pointer.move_to(circle_positions[visitado].get_center())
                        pointer.set_color(GREEN)
                        self.add(pointer)
                        self.play(circle_positions[visitado].animate.set_color(GREEN))
                    else:
                        print(f'visito {visitado} y no encontré')
                        pointer.move_to(circle_positions[visitado].get_center())
                        pointer.set_color(RED)
                        self.add(pointer)
                        self.play(circle_positions[visitado].animate.set_color(YELLOW))