import maze.py
from sortedcontainers import SortedKeyList

class Frontera:

    def __init__(self):
        self._frontier = self.crea_frontera()

    def _crea_frontera(self):
            frontier = SortedKeyList(key=NodoArbol.get_f)
            return frontier

    def push(self, node):
        if isinstance(node, NodoArbol):
            self._frontier.add(node)
        else:
            print("Error. No es un nodo.")

    def pop(self):
        return self._frontier.pop(0)

    def es_vacia(self):
        if bool(self._frontier):
            return False
        return True

class Problema:

    def __init__(self,json):
        self.id_nodo=0
        self.frontera=Frontera()
        self.estadoInicial=str(json.get("INITIAL"))
        obj=str(json.get("OBJECTIVE"))
        maze = Maze_from_json(str(json.get("MAZE")))

        self.espacioEstados=EspacioEstados(obj,maze)

        
        nodoInicial=NodoArbol(self.id_nodo,0,self.estadoIncial,None,None,0,0,0)
        self.id_nodo=self.id_nodo+1
        self.frontera.push(nodoInicial)

    
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
        celda = self.maze.maze_map[id[1:2]][id[4:5]]
        return Estado(id,celda)

    def sucesores(self,estado):    
        suc = []
        if estado.vecinos[0]==True:
            suc.add(['N',"({}, {})".format(self.x,self.y+1),1])
        if estado.vecinos[1]==True:
            suc.add(['E',"({}, {})".format(self.x+1,self.y),1])
        if estado.vecinos[2]==True:
            suc.add(['S',"({}, {})".format(self.x,self.y-1),1])
        if estado.vecinos[3]==True:
            suc.add(['O',"({}, {})".format(self.x-1,self.y),1])
        return suc

    def objetivo(self,estado):
        if estado.id == self.obj:
            return True
        return False

class Estado:
    
     def __init__(self,id,celda):
         self.id=id
         self.valor=celda.valor
         self.vecinos=celda.walls

class NodoArbol():

    def __init__(self, id_nodo, costo, estado, padre, accion, p, h, valor):
        self.id_nodo = id_nodo
        self.padre = padre
        self.estado = estado
        self.coste = coste
        self.accion = accion
        self.profundidad = p
        self.h = h

    def get_h(self):
        return self.h

