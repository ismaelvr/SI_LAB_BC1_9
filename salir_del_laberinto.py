from maze import *
import operator
import json
import random

class Frontera:

    def __init__(self):
        self._frontier = self._crea_frontera()

    def _crea_frontera(self):
        return []

    def push(self, node):
        f,x,y=node.get_valor(),node.get_x(),node.get_y()
        self._frontier.append([node,f,x,y])

    def pop(self):
        self._frontier.sort(key= operator.itemgetter(1,2,3))
        aux=self._frontier.pop(0)
        return aux[0]

    def es_vacia(self):
        if bool(self._frontier):
            return False
        return True

class Problema:

    def __init__(self,json):
        self.id_nodo=0
        self.frontera=Frontera()
        try:
            estadoInicial=str(json.get("INITIAL"))
            obj=str(json.get("OBJETIVE"))
            maze = Maze_from_json(str(json.get("MAZE")))
            self.espacioEstados=EspacioEstados(maze,obj)
            estadoInicial= self.espacioEstados.crearEstado(estadoInicial)
        except:
            print("Error al abrir el json")
            exit(1)

        self.añadir_nodo(0,estadoInicial,None,None,0,0,0) 
        
        

    def añadir_nodo(self,coste,estado,padre,accion,p,h,valor):
        nodo=NodoArbol(self.id_nodo,coste,estado,padre,accion,p,h,valor)
        self.id_nodo=self.id_nodo+1
        self.frontera.push(nodo)

    def crear_aleatorio(self):
        aux,estado = self.espacioEstados.crear_aleatorio()
        self.añadir_nodo(0,estado,None,None,0,0,random.randrange(4))
        return aux

    
    def calcular_f(self):
        if self.solucion=="anchura":
            return 1
        elif self.solucion=="profundidad":
            return 1
        elif self.solucion=="costo uniforme":
            return 1
        elif self.solucion=="voraz":
            return 1
        else:
            return 1

class EspacioEstados:

    def __init__(self,maze,objetivo):        
        self.maze=maze
        self.obj=objetivo

    def crearEstado(self,id):
        aux= id[1:-1]
        aux = aux.split(',')
        x=int(aux[0])
        y=int(aux[1])
        celda = self.maze.maze_map[y][x]
        return Estado(id,celda,x,y)
    
    def crear_aleatorio(self):
        x = random.randrange(self.maze.xmax)
        y = random.randrange(self.maze.ymax)
        estado = self.crearEstado("({}, {})".format(x,y))
        suc = self.sucesores(estado)
        ret1="SUC(({}, {}))={}".format(x,y,suc)
        return ret1,estado

    def sucesores(self,estado):    
        suc = []
        if estado.vecinos[0]==True:
            suc.append(['N',"({}, {})".format(estado.x-1,estado.y),1])
        if estado.vecinos[1]==True:
            suc.append(['E',"({}, {})".format(estado.x,estado.y+1),1])
        if estado.vecinos[2]==True:
            suc.append(['S',"({}, {})".format(estado.x+1,estado.y),1])
        if estado.vecinos[3]==True:
            suc.append(['O',"({}, {})".format(estado.x,estado.y-1),1])
        return suc

    def objetivo(self,estado):
        if estado.id == self.obj:
            return True
        return False

class Estado:
    
     def __init__(self,id,celda,x,y):
         self.id=id
         self.valor=celda.valor
         self.vecinos=celda.walls
         self.x,self.y =x,y

class NodoArbol():

    def __init__(self, id_nodo, coste, estado, padre, accion, p, h, valor):
        self.id_nodo = id_nodo
        self.padre = padre
        self.estado = estado
        self.coste = coste
        self.accion = accion
        self.profundidad = p
        self.h = h
        self.valor = valor

    def get_valor(self):
        return self.valor
    def get_x(self):
        return self.estado.x
    def get_y(self):
        return self.estado.y


filename=input("Introduzca el nombre del archivo\n")
f = open(filename, "r")
contenido = f.read()
datos_json = json.loads(contenido)
problema = Problema(datos_json)

for i in range(100):
    print(problema.crear_aleatorio())

for i in range(101):
    nodo = problema.frontera.pop()
    print("id:{} estado:{} f:{}".format(nodo.id_nodo,nodo.estado.id,nodo.valor))

    