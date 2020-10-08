# df_maze.py
import random
import matplotlib.pyplot as plt
import numpy as np
import json

class Cell:
    
    # Opuestos
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'O', 'O': 'E'}
    visitado = False

    def __init__(self, x, y):
      
        self.x, self.y = x, y

        self.walls = {'N': False, 'E': False, 'S': False, 'O': False}
 
    def tiene_muros(self):
        
        return all(self.walls.values())
    
    def crear_vecino(self, other, wall):
        
        self.walls[wall] = True
        other.walls[Cell.wall_pairs[wall]] = True

class Maze:
    
    def __init__(self, nx, ny):
        self.xmax = nx
        self.ymax = ny
        destx, desty = self.casilla_aleatoria(self.xmax, self.ymax)
        inix, iniy = self.casilla_aleatoria(self.xmax, self.ymax)
       
        while destx == inix or desty == iniy: #Así no coincide la casilla ni están excesivamente cerca (se puede mejorar) 
            destx, desty = self.casilla_aleatoria(self.xmax, self.ymax)
            inix, iniy = self.casilla_aleatoria(self.xmax, self.ymax)

        self.nx, self.ny = destx, desty
        self.ix, self.iy = inix, iniy
        print(f'Inicio: {self.ix},{self.iy}')
        print(f'Destino: {self.nx},{self.ny}')
        

        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def casilla_aleatoria(self, x,y):
        n = random.randrange(x)
        m = random.randrange(y)
        return n,m

    def casilla_aleatoria_no_visitada(self):
        n = random.randrange(self.xmax)
        m = random.randrange(self.ymax)
        while self.getCelda(n,m).visitado:
            n = random.randrange(self.xmax)
            m = random.randrange(self.ymax)
        print(n,m)
        return n,m

    def getCelda(self, x, y):
  
        return self.maze_map[x][y]

    def __str__(self):
        #Convertir en cadena 
        maze_rows = ['-' * nx*2]
        for y in range(ny):
            maze_row = ['|']
            for x in range(nx):
                if not self.maze_map[x][y].walls['E']:
                    maze_row.append(' |') #Ponemos pared al Este de la casilla
                    #print(x,y)
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(nx):
                if not self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')  #Ponemos pared al Sur de la casilla
                    #print(x,y)
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def guardar_txt(self, maze):
        with open("maze.txt", 'w') as file:
            file.write(str(maze))
            file.close()

    def generar_json(self, maze):

        with open("maze.json", 'w') as file:
            
            mazejson = {
                "rows": self.xmax,
                "columns": self.ymax    
                
            }
            json.dump(mazejson, file)
            file.close


    def encontrar_vecinos_validos(self, cell):
        """Return a list of unvisited neighbours to cell."""

        self.delta = [('O', (-1,0)),
                 ('E', (1,0)),
                 ('S', (0,1)),
                 ('N', (0,-1))]
        neighbours = []
        for direction, (dx,dy) in self.delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < nx) and (0 <= y2 < ny) and not maze.getCelda(x2,y2).visitado:
                neighbour = maze.getCelda(x2, y2)
                if not neighbour.tiene_muros():
                    neighbours.append((direction, neighbour))
        return neighbours

    def encontrar_vecinos(self, cell):
        """Return a list of unvisited neighbours to cell."""

        self.delta = [('O', (-1,0)),
                 ('E', (1,0)),
                 ('S', (0,1)),
                 ('N', (0,-1))]
        neighbours = []
        for direction, (dx,dy) in self.delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < nx) and (0 <= y2 < ny):
                neighbour = maze.getCelda(x2, y2)
                if not neighbour.tiene_muros():
                    neighbours.append((direction, neighbour))
        return neighbours

    def quedan_celdas(self):
        for i in range(self.xmax):
            for j in range(self.ymax):
                if not self.getCelda(i, j).visitado:
                    return True
        return False
    
    def destino_encontrado(self, celda_actual):
        if celda_actual.x == self.nx and celda_actual.y == self.ny:
            print("Destino encontrado")
            #self.encontrado = True
            return True
        return False
    
    def write_svg(self, filename):
        """Write an SVG image of the maze to filename."""

        aspect_ratio = self.xmax / self.ymax
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.xmax, width / self.ymax

        def write_wall(f, x1, y1, x2, y2):
            """Write a single wall to the SVG image file handle f."""

            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'
                                .format(x1, y1, x2, y2), file=f)

        # Write the SVG image file for maze
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                    .format(width+2*padding, height+2*padding,
                        -padding, -padding, width+2*padding, height+2*padding),
                  file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print(']]></style>\n</defs>', file=f)
            # Draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).
            for x in range(self.xmax):
                for y in range(self.ymax):
                    if not maze.getCelda(x,y).walls['S']:
                        x1, y1, x2, y2 = x*scx, (y+1)*scy, (x+1)*scx, (y+1)*scy
                        write_wall(f, x1, y1, x2, y2)
                    if not maze.getCelda(x,y).walls['E']:
                        x1, y1, x2, y2 = (x+1)*scx, y*scy, (x+1)*scx, (y+1)*scy
                        write_wall(f, x1, y1, x2, y2)
            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above. 
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height),file=f)
            print('</svg>', file=f)
    
    def crear_laberinto(self):
        #podemos hacer que cuando llegue al destino, recorra la array de visitados y ahí marque todos a true
        celda_actual = self.getCelda(self.ix, self.iy)
        visitados = []
        #celda_actual.visitado = True

        #Primero encontramos el destino
        with open("depuracion.txt", 'w') as f:
            while not self.destino_encontrado(celda_actual): 
                #El destino va a ser siempre el mismo, nosotro cambiamos la posicion inicial
                vecinos_validos = self.encontrar_vecinos_validos(celda_actual)
                
                if not vecinos_validos:
                    print(f"Ibamos a {celda_actual.x}, {celda_actual.y} pero no se puede")
                    celda_actual.visitado = True
                    celda_actual = visitados.pop()
                    continue
                
                celda_actual.visitado = True
                print(f'{celda_actual.x}, {celda_actual.y}')
                #print(vecinos_validos)
                direccion, siguiente_celda = random.choice(vecinos_validos)
                celda_actual.crear_vecino(siguiente_celda,direccion)
                visitados.append(celda_actual)
                f.write(str(celda_actual.x))
                f.write(",")
                f.write(str(celda_actual.y))
                f.write("\n")
                #print(visitados)
                celda_actual = siguiente_celda
        
        print(f"Hemos llegado al destino: {celda_actual.x}, {celda_actual.y}")
        print("Obviemos los siguiente")
        maze.write_svg("maze_a_medias.svg")
        #Hemos encontrado el destino pero igual quedan casillas por visitar
        
        while self.quedan_celdas():
            n, m = self.casilla_aleatoria_no_visitada()
            celda_actual = self.getCelda(n, m)
            
            while not celda_actual.visitado: #arreglar
                vecinos = self.encontrar_vecinos(celda_actual)
                #print(vecinos)
                celda_actual.visitado = True
                direccion, siguiente_celda = random.choice(vecinos)
                celda_actual.crear_vecino(siguiente_celda,direccion)
                celda_actual = siguiente_celda
            maze.write_svg("maze_terminado.svg")
        print("Ya no hay mas celdas")
              
# Tamaño laberinto
nx, ny = 10,10

maze = Maze(nx, ny)
maze.crear_laberinto() #cambiar las paredes de abajo y derecha
maze.guardar_txt(maze)
maze.generar_json(maze)
#maze.draw()
print(maze)
