'''

Fuente: https://picoledelimao.github.io/blog/2015/12/06/solving-the-sliding-puzzle/

-Algoritmo A*
    cuando el menor peso es unico se usa la heuristica Manhattan
    cuando hay muchos pesos con el menor peso se usa la heuristica Machado
'''

import copy
import heapq

class Board:
    '''
    variable estatica que permite detener la ejecucion del metodo recursivo visit
    , se usa una variable estatica debido a que todos los tableros deben saber si
    ya se llego a una solucion dentro de la recursion
    '''
    is_complete = False

    def __init__(self, parent_board, configuration_board, target_board):
        self.dimension = len(configuration_board)

        #tablero antecesor
        self.parent_board = parent_board

        #ruta de las configuraciones previas realizadas hasta el momento
        self.path = []

        #configuracion del tablero y objetivo del tablero
        self.config = []
        self.target = []

        #diccionarios usados para el calculo de la distancia manhattan
        self.dict_config = {}
        self.dict_target = {}

        #peso del tablero actual
        self.weight = 0

        #tableros derivados o hijos
        self.children_boards = []

        #agrega la configuracion del tablero actual al path
        if self.parent_board != None:
            self.path = copy.deepcopy(self.parent_board.path)
            self.path.append(self.config)
        else:
            self.path.append(self.config)

        #asigna los valores de la configuracion inicial pasada por parametros a la configuracion del tablero actual
        for i in range(0, self.dimension):
            self.config.append([])
            for j in range(0, self.dimension):

                #se crea una matriz de dos dimensiones que representa la configuracion pasada en el constructor
                self.config[i].append(configuration_board[i][j])
                '''
                    se crea un diccionario que almacena las coordenadas de cada pieza 
                    de la configuracion pasada en el constructor
                '''
                self.dict_config.update({configuration_board[i][j]: (i, j)})

        #si no se define un tablero objetivo en el constructor se genera el tablero clasico
        if target_board == None:
            for i in range(0, self.dimension):
                self.target.append([])
                for j in range(0, self.dimension):
                    '''
                    se crea una matriz de dos dimensiones que representa el tablero objetivo
                    y se crea un diccionario que almacena las coordenadas de cada pieza del
                    tablero objetivo a generar
                    '''
                    if i == (self.dimension-1) and j == (self.dimension-1):
                        self.target[i].append(0)
                        self.dict_target.update({0: (i,j)})
                    else:
                        self.target[i].append(self.dimension * i + (j+1))
                        self.dict_target.update({(self.dimension * i + (j+1)): (i,j)})
        else:
            #se mapea el tablero objetivo pasado en el constructor
            for i in range(0, self.dimension):
                self.target.append([])
                for j in range(0, self.dimension):
                    '''
                    se crea una matriz de dos dimensiones que representa el tablero objetivo
                    y se crea un diccionario que almacena las coordenadas de cada pieza del
                    tablero objetivo pasado en el constructor
                    '''
                    self.target[i].append(target_board[i][j])
                    self.dict_target.update({target_board[i][j]: (i, j)})

        #se calcula el peso de la configuracion actual con el algoritmo Manhattan
        self.weight = self.manhattan_h()

    '''
        Se redefine este metodo para permitir que un objeto de tipo Board se pueda ordenar automaticamente
        de menor a mayor en una priority queue por medio del atributo peso
    '''
    def __lt__(self, other):
        return self.weight < other.weight

    #Imprime en consola un tablero
    def print_board(self, board, label=""):
        print(label)
        for r in board:
            print("|", end='')
            for e in r:
                if e < 10:
                    print(" ", e, end='')
                else:
                    print("", e, end='')
            print(" |")

    #funcion heuristica que cuenta cuantas piezas estan desacomodadas
    def misplaced_tiles_h(self):
        misplaced_tiles = 0
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                if self.config[i][j] != self.target[i][j]:
                    misplaced_tiles+=1
        return misplaced_tiles

    #funcion heuristica que calcula el peso de la configuracion actual en función de la posicion
    def manhattan_h(self):
        manhattan_distance = 0
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                manhattan_distance += (abs(self.dict_config.get(self.config[i][j])[0] - self.dict_target.get(self.config[i][j])[0])
                                       + abs(self.dict_config.get(self.config[i][j])[1] - self.dict_target.get(self.config[i][j])[1]))
        return manhattan_distance

    #obtiene la posicion de la pieza 0 de la configuracion actual
    def get_blank_position(self):
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                if self.config[i][j] == 0:
                    return (i, j)

    #Obtiene los movimientos validos de la pieza 0
    '''
        Ejemplo con tres dimensiones

        dimension 3

        f = fila
        c = columna

        f c

        0 0 abajo o derecha

        0 1 abajo o derecha o izquierda

        0 2 abajo o izquierda

        1 0 arriba o abajo o derecha

        1 1 arriba o abajo o derecha o izquierda

        1 2 arriba o abajo o izquierda

        2 0 arriba o derecha

        2 1 arriba o derecha o izquierda

        2 2 arriba o izquierda


        abajo: 00 01 02 10 11 12

        derecha: 00 01 10 11 20 21

        arriba: 10 11 12 20 21 22

        izquierda: 01 02 11 12 21 22


        if f < (dimension-1):
	        movimientos_validos.push(abajo)
        if c < (dimension-1):
	        movimientos_validos.push(derecha)
        if f > 0:
	        movimientos_validos.push(arriba)
        if c > 0:
	        movimientos_validos.push(izquierda)
    '''
    def get_blank_valid_movements(self):
        #diccionario usado como enumeracion para representar los movimientos validos de una pieza
        PIECE_MOVEMENT = {'UP': 'up', 'DOWN': 'down', 'LEFT' : 'left', 'RIGHT': 'right'}

        blank_position = self.get_blank_position()
        line = blank_position[0]
        column = blank_position[1]

        blank_valid_movements = []

        if line < self.dimension - 1:
            blank_valid_movements.append(PIECE_MOVEMENT.get("DOWN"))
        if line > 0:
            blank_valid_movements.append(PIECE_MOVEMENT.get("UP"))
        if column < self.dimension -1:
            blank_valid_movements.append(PIECE_MOVEMENT.get("RIGHT"))
        if column > 0:
            blank_valid_movements.append(PIECE_MOVEMENT.get("LEFT"))

        #lista de movimientos validos de la pieza cero dado el tablero actual que seran regresados
        return blank_valid_movements

    #intercambia las posiciones de dos piezas en un tablero
    def change_pieces(self, board, x1, y1, x2, y2):
        aux = board[x1][y1]
        board[x1][y1] = board[x2][y2]
        board[x2][y2] = aux

    #mueve la pieza 0 en un tablero
    def move_blank(self, board, piece_movement):
        blank_position = self.get_blank_position()
        line = blank_position[0]
        column = blank_position[1]

        if piece_movement == 'down':
            self.change_pieces(board, line, column, line+1, column)
        elif piece_movement == 'up':
            self.change_pieces(board, line, column, line-1, column)
        elif piece_movement == 'right':
            self.change_pieces(board, line, column, line, column+1)
        elif piece_movement == 'left':
            self.change_pieces(board, line, column, line, column-1)

    #Obtiene una lista de los tableros derivados de un tablero determinado
    def get_children_boards(self, board):
        blank_valid_movements = board.get_blank_valid_movements()
        number_of_valid_movements = len(blank_valid_movements)

        posible_configurations = []
        posible_children_boards = []

        for movement in range(0, number_of_valid_movements):
            #Se copia la configuracion actual en función de los movimientos validos
            posible_configurations.append(copy.deepcopy(board.config))

            #se ejecuta un movimiento posible
            board.move_blank(posible_configurations[movement], blank_valid_movements[movement])

        for configuration in range(0, len(posible_configurations)):
            insert_posible_configuration = True
            configuration_counter = 0
            '''
            Termina la comparación cuando se encuentra una coincidencia o se comparo
            al con todos los tableros excepto el último
            '''
            while insert_posible_configuration == True and configuration_counter < len(board.path) - 1:
                if posible_configurations[configuration] != board.path[configuration_counter]:
                    insert_posible_configuration = True
                else:
                    insert_posible_configuration = False
                configuration_counter+=1

            #si la configuracion obtenida no se encuentra en las configuraciones previas
            if insert_posible_configuration == True:
                #la configuracion se convierte en un nuevo board
                posible_children_boards.append(Board(board, posible_configurations[configuration], board.target))

        #se convierten los tableros posibles en una cola de prioridad
        heapq.heapify(posible_children_boards)

        #se vacia la cola de prioridad como una lista ordenada en el atributo next_boards del objeto board
        return heapq.nsmallest(len(posible_children_boards), posible_children_boards)

    def play(self):
        print(pow(self.dimension,2)-1, "Puzzle")
        print("**************************")
        self.visit(self)

    def visit(self, board):
        #si el peso del tablero actual es mayor a cero significa que no esta resuelto
        if board.weight > 0:
            #Se obtienen los tableros hijos del correspondiente tablero
            board.children_boards = self.get_children_boards(board)

            #si no hay tableros derivados, es decir un camino a seguir se retorna el metodo
            if not board.children_boards:
                return

            #se obtienen todos los pesos para saber si mas de uno coincide
            weigths = []
            for posible_board in board.children_boards:
                weigths.append(posible_board.weight)

            #se determina el numero de ocurrencias del menor peso
            ocurrences = weigths.count(board.children_boards[0].weight)

            next_board = None
            #si mas de un peso coincide
            if ocurrences > 1:
                children_boards_pq = []
                heapq.heapify(children_boards_pq)

                for i in range(0, ocurrences):
                    #obtener los hijos cada tablero empatado
                    board.children_boards[i].children_boards = self.get_children_boards(board.children_boards[i])

                    #si los tableros hijos tienen hijos a su vez
                    if board.children_boards[i].children_boards:
                        #se obtiene el hijo con el menor peso
                        minor_son_board = board.children_boards[i].children_boards.pop(0)

                        #el peso de la fila es un elemento propio de la heuristica Machado
                        row_weight = 0

                        #se compara cada fila para determinar si es igual a la del target, tal como lo indica la heuristica Machado
                        for row in range(0, len(minor_son_board.config)):
                            if minor_son_board.config[row] == minor_son_board.target[row]:
                                row_weight+=1

                        #Esta es una heuristica propia definida como la heuristica Machado
                        board.children_boards[i].weight = minor_son_board.weight + minor_son_board.misplaced_tiles_h() - row_weight

                        '''
                        Lo que hace la heuristica Machado es volver mas chico al peso de un tablero por cada fila ya acomodada
                        '''
                    else:
                        #si un tablero hijo no tiene hijos, al peso del tablero se le asigna el numero mas grande posible
                        board.children_boards[i].weight = float("inf")

                    heapq.heappush(children_boards_pq, board.children_boards[i])

                next_board_counter = 0

                '''
                se visita un nodo mientras haya elementos en la pila de prioridad que almacena los tableros hijos
                y mientras aun no se haya encontrado una solucion
                '''
                while next_board_counter < len(children_boards_pq) and self.is_complete != True:
                    next_board = heapq.heappop(children_boards_pq)
                    self.visit(next_board)
                    next_board_counter+=1
            else:
                #obtiene el primer elemento de la lista como si la lista fuera una cola
                next_board = board.children_boards.pop(0)
                self.visit(next_board)
        else:
            Board.is_complete = True
            movement_counter = 0

            for b in board.path:
                label = "Configuracion inicial"
                if movement_counter > 0:
                    label = "Movimiento " + str(movement_counter)

                self.print_board(b, label)
                movement_counter+=1

            print("Puzzle Completado, Resuelto en", len(board.path) - 1 , "pasos")

#b = Board(None, [[1,2,3],[0,4,6],[7,5,8]], None) #prueba 1
#b = Board(None, [[1, 5, 2], [4, 0, 3], [6, 7, 8]],[[1, 2, 3], [8, 0, 4], [7, 5, 6]]) #prueba 2 *

#b = Board(None, [[2, 8, 3], [1, 6, 4], [7, 0, 5]],[[2, 8, 3], [7, 1, 4], [0, 6, 5]]) #prueba 3
#b = Board(None, [[0,1,3],[4,2,5],[7,8,6]], None) #prueba 4
#b = Board(None, [[2, 8, 3], [1,6,4], [7,0,5]], [[1,2,3], [8,0,4], [7,6,5]]) #prueba 5

#b = Board(None, [[1,2,3,4], [5,6,0,8], [9,10,7,11], [13,14,15,12]], [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,0]]) # prueba 6
#b = Board(None, [[1,2,3,4], [5,6,0,8], [9,10,7,11], [13,14,15,12]], None) # prueba 6 sin target

#b = Board(None, [[2,8,3], [1,6,4], [7,0,5]], [[1,2,3], [8,0,4], [7,6,5]])# prueba 7

b.play()
