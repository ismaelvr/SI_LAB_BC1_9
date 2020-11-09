import random
import numpy as np
from time import time
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import json

class Cell:
    
    # Opuestos
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'O', 'O': 'E'}
    visitado = False
    
    def __init__(self, x, y):

        self.valor=0
        self.x, self.y = x, y
        self.valor=1

        self.walls = {'N': False, 'E': False, 'S': False, 'O': False}
    def tiene_muros(self): 
        
        return all(self.walls.values())
    
    def crear_vecino(self, other, wall):
        
        self.walls[wall] = True
        other.walls[Cell.wall_pairs[wall]] = True

###############################################
class Cell_from_json:

    def __init__(self, x, y, walls):

        self.x, self.y = x, y

        self.walls = walls

        self.valor = 0

class Maze_from_json:
    
    def __init__(self, filename):
        
        f = open(filename, "r")
        contenido = f.read()
        datos_json = json.loads(contenido)
        valor=0
        #self.comprobar_json(datos_json)
        

        cells = datos_json.get("cells")

        self.ymax = datos_json['rows']
        self.xmax = datos_json['cols']

        self.maze_map = [[Cell_from_json(y,x, cells.get("({}, {})".format(y,x)).get("neighbors")) for y in range(self.ymax)] for x in range(self.xmax)]
        

    def comprobar_json(self, datos_json):
       

        if not len(datos_json) == 6:
            print("Archivo JSON no válido")
            return 0

        try:
            r = int(datos_json.get("rows"))
            c = int(datos_json.get("cols"))
            m = int(datos_json.get("max_n"))
        except:
            print("Archivo JSON no válido")
            return 0

        if r <= 0 or c <= 0:
            return 0

        if m != 4:
            print("Error. Únicamente debe haber 4 vecinos posibles")
            return 0

        elemento4 = datos_json.get("mov")
        elemento5 = datos_json.get("id_mov")

        comprobacion = [('N', (-1,0)),('E', (0,1)),('S', (1,0)),('O', (0,-1))]
        
        j = 0
        for coor, (e1,e2) in comprobacion:

            if e1 != elemento4[j][0]:
                print("Archivo JSON no válido")
            
            if e2 != elemento4[j][1]:
                print("Archivo JSON no válido")

            if coor != elemento5[j]:
                print("Archivo JSON no válido")
                return 0
                
            j = j + 1

        if elemento5[0] != 'N' or elemento5[1] != 'E' or elemento5[2] != 'S' or elemento5[3] != 'O':
            print("Archivo JSON no válido")
            return 0

    def getCelda(self, x, y):
  
        return self.maze_map[x][y]

    def write_svg(self, filename):
        """Write an SVG image of the maze to filename."""

        aspect_ratio = self.xmax / self.ymax
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = self.xmax*30
        width = int(height * aspect_ratio)
        if self.ymax/self.xmax >=2:
            width=width*int(self.ymax/self.xmax)
            height=height*int(self.ymax/self.xmax)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ymax, width / self.xmax
        

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
                    if not maze_from_json.getCelda(x,y).walls[2]:
                        x1, y1, x2, y2 = x*scx, (y+1)*scy, (x+1)*scx, (y+1)*scy
                        write_wall(f, x1, y1, x2, y2)
                    if not maze_from_json.getCelda(x,y).walls[1]:
                        x1, y1, x2, y2 = (x+1)*scx, y*scy, (x+1)*scx, (y+1)*scy
                        write_wall(f, x1, y1, x2, y2)
            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above. 
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height),file=f)
            print('</svg>', file=f)

#######################################

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
        #print(f"Casilla aleatoria : {n},{m}")
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

    def generar_json(self, maze):         
        json='{{\n\t"rows" : {},\n\t"cols" : {},\n\t"max_n" : 4,'.format(nx,ny)
        json=json+'\n\t"mov" : [[-1,0],[0,1],[1,0],[0,-1]],\n\t"id_mov" : ["N","E","S","O"],\n\t"cells" : {'
        for i in range(self.xmax):
            for j in range(self.ymax):
                json=json+'\n\t\t"( {}, {} )" : {{"value": {},"neighbors": {}}},'.format(i,j,self.maze_map[i][j].valor,list(self.maze_map[i][j].walls.values())).lower()
        json= json[:-1]
        json=json+'\n\t}\n}'
        with open("maze.json", 'w') as file:
            file.write(json)
            file.close()
    
    def encontrar_vecinos_validos(self, cell):

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

    def encontrar_vecinos(self, cell, camino):
        
        self.delta = [('O', (-1,0)),
                 ('E', (1,0)),
                 ('S', (0,1)),
                 ('N', (0,-1))]
        neighbours = []
        for direction, (dx,dy) in self.delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < nx) and (0 <= y2 < ny) and self.getCelda(x2, y2) not in camino:
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
     
        aspect_ratio = self.xmax / self.ymax
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = self.xmax*30
        width = int(height * aspect_ratio)
        if self.ymax/self.xmax >=2:
            width=width*int(self.ymax/self.xmax)
            height=height*int(self.ymax/self.xmax)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ymax, width / self.xmax
        

        def write_wall(f, x1, y1, x2, y2):
         
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
        while not self.destino_encontrado(celda_actual): 
            #El destino va a ser siempre el mismo, nosotro cambiamos la posicion inicial
            vecinos_validos = self.encontrar_vecinos_validos(celda_actual)
            
            if not vecinos_validos:
                #print(f"Ibamos a {celda_actual.x}, {celda_actual.y} pero no se puede")
                celda_actual.visitado = True
                celda_actual = visitados.pop()
                continue
            
            celda_actual.visitado = True
            #print(f'{celda_actual.x}, {celda_actual.y}')
            #print(vecinos_validos)
            direccion, siguiente_celda = random.choice(vecinos_validos)
            celda_actual.crear_vecino(siguiente_celda,direccion)
            visitados.append(celda_actual)
            #print(visitados)
            celda_actual = siguiente_celda
        celda_actual.visitado = True #Marcamos el destino como true
        
        
        #print(f"Hemos llegado al destino: {celda_actual.x}, {celda_actual.y}")
        #print("Ahora vamos a rellenar lo que falta")
        #maze.write_svg("maze_a_medias.svg")
        #Hemos encontrado el destino pero igual quedan casillas por visitar
        
        while self.quedan_celdas():
            n, m = self.casilla_aleatoria_no_visitada()
            celda_actual = self.getCelda(n, m)
            camino_secundario = []
            while not celda_actual.visitado or celda_actual in camino_secundario:  #arreglar

                vecinos = self.encontrar_vecinos(celda_actual, camino_secundario)
                #print(vecinos)
                celda_actual.visitado = True

                if not vecinos:
                    #print(f"Ibamos a {celda_actual.x}, {celda_actual.y} pero no se puede")
                    celda_actual.visitado = True
                    celda_temporal = camino_secundario.pop()  #Es raro pero funciona
                    camino_secundario.insert(0, celda_temporal)
                    camino_secundario.insert(0,celda_actual)
                    celda_actual = celda_temporal
                    continue
                
                direccion, siguiente_celda = random.choice(vecinos)
                
                if siguiente_celda in camino_secundario:
                    #celda_actual.visitado = True #Redundante
                    celda_actual = camino_secundario.pop()
                    
                    #print(f"Vecino ya en el camino: {siguiente_celda.x},{siguiente_celda.y}")
                    continue
        
                camino_secundario.append(celda_actual)
                celda_actual.crear_vecino(siguiente_celda,direccion)
                celda_actual.visitado = True
                celda_actual = siguiente_celda
                #print(f"Siguiente casilla: {celda_actual.x},{celda_actual.y} ")
            #print("Parece que se ha salido")
            
        #maze.write_svg("maze_terminado.svg")
        #print("Ya no hay mas celdas")

'''
def main():
    print("Elige: ")
    print("1. Crear laberinto aleatorio ")
    print("2. Cargar laberinto desde JSON ")

    eleccion = int(input())
    if (eleccion == 1):
        print("Introduzca el ancho del laberinto:")
        nx = int(input())
        print("Introduzca el alto del laberinto:")
        ny = int(input())

        start_time = time()
        maze = Maze(nx, ny)
        maze.crear_laberinto() #cambiar las paredes de abajo y derecha
        elapsed_time = time() - start_time
        print(f"La generación del laberinto ha tardado {elapsed_time} segundos")

        start_time = time()
        maze.generar_json(maze)
        elapsed_time = time() - start_time
        print(f"La generación del JSON ha tardado {elapsed_time} segundos")
    
        start_time = time()
        maze.write_svg("maze.svg")
        drawing = svg2rlg("maze.svg")
        renderPM.drawToFile(drawing, "maze.png", fmt="PNG")
        elapsed_time = time() - start_time
        print(f"La generación de la imagen ha tardado {elapsed_time} segundos")
    elif (eleccion == 2):
        print("Indica el nombre del archivo")
        filename = input()
        start_time = time()
        maze_from_json = Maze_from_json("ejemplosJson/"+filename+".json")  #PEDRO
        elapsed_time = time() - start_time
        print(f"La lectura del JSON y creación del laberinto ha tardado {elapsed_time} segundos")
        start_time = time()
        maze_from_json.write_svg("maze_from_json.svg")
        drawing = svg2rlg("maze_from_json.svg")
        renderPM.drawToFile(drawing, "maze_from_json.png", fmt = "PNG")
        elapsed_time = time() - start_time
        print(f"La generación del PNG ha tardado {elapsed_time} segundos")
    else:
        print("Eleccion incorrecta. Fin del programa")

def if __name__ == "__main__":
    main()
'''

    