from maze import *
import operator
import json
import random
import math

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

    def __init__(self,json,estrategia):
        self.__poda = {}
        self.id_nodo=0
        self.frontera=Frontera()
        self.prof_max=1000000
        self.solucion=False
        self.estrategia=estrategia
        try:
            estadoInicial=str(json.get("INITIAL"))
            obj=str(json.get("OBJETIVE"))
            maze = Maze_from_json(str(json.get("MAZE")))
            self.espacioEstados=EspacioEstados(maze,obj)
            estadoInicial= self.espacioEstados.crearEstado(estadoInicial)
        except:
            print("Error al abrir el json")
            exit(1)

        self.añadir_nodo(estadoInicial,None,None,0)
        solucion = self.solucinar 
        if self.solucion:
            print("SI hay solucion")
        else:
            print("NO hay solucion")
    
    def solucinar(self):
        while not self.solucion and  not self.frontera.es_vacia():
            nodo_actual = self.frontera.pop()
            if self.espacioEstados.objetivo(nodo_actual.estado):
                self.solucion = True
            else:
                sucesores = self.espacioEstados.sucesores(nodo_actual)
                for i in sucesores: 
                    estado = self.espacioEstados.crearEstado(i[1])
                    self.añadir_nodo(estado,i[0],nodo_actual,nodo_actual.p)
                    
        return nodo_actual

    def calcular_valor(self,nodo):

        if self.estrategia == "Anchura":
            nodo.valor = nodo.padre.p + 1

        if self.estrategia == "Costo uniforme":
            nodo.valor = nodo.padre.coste + nodo.coste

        if self.estrategia == "Profundidad":
            #falta hacer profundidad acotada
            nodo.valor = -(nodo.padre.p + 1)
            
        if self.estrategia == "Voraz":
            nodo.h = self.espacioEstados.calcular_h(nodo.estado)
            nodo.valor = nodo.h

        if self.estrategia == "A*":
            nodo.h = self.espacioEstados.calcular_h(nodo.estado)
            valor = nodo.padre.coste + nodo.coste
            nodo.valor = nodo.h + valor
    
    def poda(self, estado, valor):
        '''
        hace la poda del arbol
        '''
        if not estado in self.__poda:
            self.__poda[estado] = valor
            return True
        if self.__poda.get(estado) > valor:
            self.__poda.pop(estado)
            self.__poda[estado] = valor
            return True
        return False    

    def añadir_nodo(self,estado,accion,padre,p):
        coste = self.espacioEstados.calcular_coste(estado)
        nodo=NodoArbol(self.id_nodo,coste,estado,padre,accion,p+1,0,0)
        nodo.valor=self.calcular_valor(nodo)
        nodo.accion="[{}][{},{}]"
        self.id_nodo=self.id_nodo+1
        if poda(estado,nodo.valor):
            self.frontera.push(nodo)
    
    def crear_aleatorio(self):
        aux,estado = self.espacioEstados.crear_aleatorio()
        self.añadir_nodo(0,estado,None,None,0,0,random.randrange(4))
        return aux

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

    def calcular_h(self,estado):
        aux= self.obj[1:-1]
        aux = aux.split(',')
        x=int(aux[0])
        y=int(aux[1])
        sol = abs(estado.x-x)+ abs(estado.y-y)
        print("h: {} estado: {},{}\n".format(sol,x,y))
        return sol

    def calcular_coste(self,estado):
        cell =self.maze.maze_map[estado.y][estado.x]
        return cell.valor + 1

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
    


def main():
    filename=input("Introduzca el nombre del archivo\n")
    f = open(filename, "r")
    contenido = f.read()
    datos_json = json.loads(contenido)
    problema = Problema(datos_json,"A*")

    for i in range(100):
        print(problema.crear_aleatorio())

    for i in range(101):
        nodo = problema.frontera.pop()
        print("id:{} estado:{} f:{}".format(nodo.id_nodo,nodo.estado.id,nodo.valor))

if __name__ == "__main__":
    main()