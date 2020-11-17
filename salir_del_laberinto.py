from maze import *
import operator
import json
import random
import math

class Stack:
    '''
    crea una pila
    '''
    def __init__(self):
        '''
        inicia la pila
        '''
        self.items = []

    def is_empty(self):
        '''
        comprueba si esta vacia
        '''
        return self.items == []

    def push(self, item):
        '''
        push
        '''
        self.items.append(item)

    def pop(self):
        '''
        pop
        '''
        return self.items.pop()

    def peek(self):
        '''
        peek
        '''
        return self.items[len(self.items)-1]

    def size(self):
        '''
        size
        '''
        return len(self.items)

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
        solucion = self.solucinar()

        if self.solucion:
            print("SI hay solucion")
            self.escribir_solucion(solucion)
        else:
            print("NO hay solucion")

    def escribir_solucion(self,solucion):
        fichero = open("sol_{}x{}_{}.txt".format(self.espacioEstados.maze.xmax,self.espacioEstados.maze.ymax,self.estrategia), 'w')
        fichero.write(str("[id][cost,state,father_id,action,depth,h,value]\n"))
        pila = Stack()
        while solucion.padre is not None:
            aux="[{}][{},{},{},{},{},{},{}]\n".format(solucion.id_nodo,solucion.coste,solucion.estado.id,solucion.padre.id_nodo,solucion.accion,solucion.p,solucion.h,solucion.valor)
            pila.push(aux)
            solucion=solucion.padre
        aux="[{}][{},{},None,{},{},{},{}]\n".format(solucion.id_nodo,solucion.coste,solucion.estado.id,solucion.accion,solucion.p,solucion.h,solucion.valor)
        pila.push(aux)
        while not pila.is_empty():
            fichero.write(str(pila.pop()))
        fichero.close()
 
    def solucinar(self):
        nodo_actual = None
        while not self.solucion and  not self.frontera.es_vacia():
            nodo_actual = self.frontera.pop()
            if self.espacioEstados.objetivo(nodo_actual.estado):
                self.solucion = True
            else:
                sucesores = self.espacioEstados.sucesores(nodo_actual.estado)
                for i in sucesores: 
                    estado = self.espacioEstados.crearEstado(i[1])
                    self.añadir_nodo(estado,i[0],nodo_actual,nodo_actual.p)
                    
        return nodo_actual

    def calcular_valor(self,nodo,coste_padre):

        if self.estrategia == "BREATH":
            if nodo.padre is not None:
                nodo.valor = nodo.padre.p + 1
            else:
                nodo.valor=1

        if self.estrategia == "UNIFORM":
            nodo.valor = nodo.coste

        if self.estrategia == "DEPTH":
            #falta hacer profundidad acotada
            if nodo.padre is not None:
                nodo.valor = -(nodo.padre.p + 1)
            else:
                nodo.valor= -1
            
        if self.estrategia == "GREEDY":
            nodo.h = self.espacioEstados.calcular_h(nodo.estado)
            nodo.valor = nodo.h

        if self.estrategia == "A":
            nodo.h = self.espacioEstados.calcular_h(nodo.estado)
            nodo.valor = nodo.h + nodo.coste
    
    def poda(self, estado, valor):
        '''
        hace la poda del arbol
        '''
        if not estado.id in self.__poda:
            self.__poda[estado.id] = valor
            return True
        if self.__poda.get(estado.id) > valor:
            self.__poda.pop(estado.id)
            self.__poda[estado.id] = valor
            return True
        return False    

    def añadir_nodo(self,estado,accion,padre,p):
        coste = self.espacioEstados.calcular_coste(estado)
        if padre is not None:
            nodo=NodoArbol(self.id_nodo,coste+padre.coste,estado,padre,accion,p+1,0,0)
        else:
            nodo=NodoArbol(self.id_nodo,coste,estado,padre,accion,p+1,0,0)
        if padre is None:
            self.calcular_valor(nodo,0)
        else:
            self.calcular_valor(nodo,padre.coste)
        self.id_nodo=self.id_nodo+1
        if self.poda(estado,nodo.valor):
            self.frontera.push(nodo)
    
    def crear_aleatorio(self):
        aux,estado = self.espacioEstados.crear_aleatorio()
        self.añadir_nodo(estado,None,None,0)
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
        #print("h: {} estado: {},{}\n".format(sol,estado.x,estado.y))
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
        self.p = p
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
    eleccion=int(input("Elige:\n1.Anchura\n2.Profundidad acotada\n3.Coste Uniforme\n4.Voraz\n5.A*\n"))
    if eleccion == 1:
        estrategia="BREATH"
    elif eleccion == 2:
        estrategia="DEPTH"
    elif eleccion == 3:
        estrategia="UNIFORM"
    elif eleccion == 4:
        estrategia="GREEDY"
    elif eleccion == 5:
        estrategia="A"
    else:
        print("Eleccion erronea")
        exit(1)
    contenido = f.read()
    datos_json = json.loads(contenido)
    problema = Problema(datos_json,estrategia)


if __name__ == "__main__":
    main()