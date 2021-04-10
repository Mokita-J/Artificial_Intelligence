# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 11:
# 92532 Mónica Jin
# 93681 Afonso Carvalho

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search, InstrumentedProblem
import sys, time


class RRState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

    def __eq__(self, other):
        if type(other) is type(self):
            return self.board == other.board
        return False

    def __hash__(self):
        return hash(self.board)

class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """
    goal = None

    def __init__(self, size, R_pos, B_pos, Y_pos, G_pos, barriers):
        self.robots = {"R": R_pos, "B": B_pos, "Y": Y_pos, "G": G_pos}
        self.barriers = barriers
        self.size = size

    def __eq__(self, other):
        if type(other) is type(self):
            return self.robots == other.robots and self.size == other.size
        return False

    def __hash__(self):
        return hash((self.robots["R"], self.robots["B"], self.robots["Y"], self.robots["G"], self.size))

    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """
        return self.robots[robot]

    def possible_actions(self, robot: str):
        actions = []
        (x, y) = self.robot_position(robot)
        if y != self.size: #checks if robot can move right
            if (x, y + 1) not in self.robots.values():
                if (x, y + 1) not in self.barriers["l"] and (x, y) not in self.barriers["r"]:
                    actions.append("r")
        if y != 1: #checks if robot can move left
            if (x, y - 1) not in self.robots.values():
                if (x, y - 1) not in self.barriers["r"] and (x, y) not in self.barriers["l"]:
                    actions.append("l")
        if x != self.size: #checks if robot can move down
            if (x + 1, y) not in self.robots.values():
                if (x + 1, y) not in self.barriers["u"] and (x, y) not in self.barriers["d"]:
                    actions.append("d")
        if x != 1: #checks if robot can move up
            if (x - 1, y) not in self.robots.values():
                if (x - 1, y) not in self.barriers["d"] and (x, y) not in self.barriers["u"]:
                    actions.append("u")
        
        return actions


def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    f = open(filename, "r")
    data = f.readlines()
    
    board = Board(eval(data[0]), None, None, None, None, {"u": [], "d": [], "l": [], "r": []})

    x, y = 0, 0
    for line in range(1, 5):
        robot = data[line].split()
        x = eval(robot[1])
        y = eval(robot[2])
        board.robots[robot[0]] = (x, y)

    goal = data[5].split()
    Board.goal = [goal[0], (eval(goal[1]), eval(goal[2]))]
    
    for line in range(7, 7 + eval(data[6])):
        barrier = data[line].split()
        x = eval(barrier[0])
        y = eval(barrier[1])
        board.barriers[barrier[2]].append((x, y))
    f.close()
    return board


class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        super().__init__(RRState(board), board.goal)


    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions = []
        for color in state.board.robots:
            for move in state.board.possible_actions(color):
                actions.append((color, move))
        return actions


    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        (robot, move) = action
        (x, y) = state.board.robot_position(robot)

        distx = state.board.size + 1
        disty = state.board.size + 1
        if move == "r":
            distx = 0
            for pos in state.board.barriers["r"]:
                if x == pos[0] and y < pos[1]:
                    disty = min(disty, pos[1] - y)
            
            for pos in state.board.barriers["l"] + list(state.board.robots.values()):
                if x == pos[0] and y < pos[1]:
                    disty = min(disty, pos[1] - y - 1)

            if disty == state.board.size + 1:
                disty = state.board.size - y
            
        elif move == "l":
            distx = 0
            for pos in state.board.barriers["r"] + list(state.board.robots.values()):
                if x == pos[0] and y > pos[1]:
                    disty = - min(abs(disty), y - pos[1] - 1)
            
            for pos in state.board.barriers["l"]:
                if x == pos[0] and y > pos[1]:
                    disty = - min(abs(disty), y - pos[1])
            
            if disty == state.board.size + 1:
                disty = 1 - y

        elif move == "u":
            disty = 0
            for pos in state.board.barriers["u"]:
                if y == pos[1] and x > pos[0]:
                    distx = - min(abs(distx), x - pos[0])
            
            for pos in state.board.barriers["d"] + list(state.board.robots.values()):
                if y == pos[1] and x > pos[0]:
                    distx = - min(abs(distx), x - pos[0] - 1)
            
            if distx == state.board.size + 1:
                distx = 1 - x

        elif move == "d":
            disty = 0
            for pos in state.board.barriers["u"] + list(state.board.robots.values()):
                if y == pos[1] and x < pos[0]:
                    distx = min(distx, pos[0] - x -1)
            
            for pos in state.board.barriers["d"]:
                if y == pos[1] and x < pos[0]:
                    distx = min(distx, pos[0] - x)

            if distx == state.board.size + 1:
                distx = state.board.size - x

        if robot == "R":
            return RRState(Board(state.board.size, (x + distx, y + disty), state.board.robot_position("B"),
                                 state.board.robot_position("Y"), state.board.robot_position("G"), state.board.barriers))
        
        elif robot == "B":
            return RRState(Board(state.board.size, state.board.robot_position("R"), (x + distx, y + disty),
                                 state.board.robot_position("Y"), state.board.robot_position("G"), state.board.barriers))
        
        elif robot == "Y":
            return RRState(Board(state.board.size, state.board.robot_position("R"), state.board.robot_position("B"),
                                 (x + distx, y + disty), state.board.robot_position("G"), state.board.barriers))
        
        elif robot == "G":
            return RRState(Board(state.board.size, state.board.robot_position("R"), state.board.robot_position("B"),
                                 state.board.robot_position("Y"), (x + distx, y + disty), state.board.barriers))
        
            

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        goal_robot = self.goal[0]
        goal_pos = self.goal[1]
        return state.board.robot_position(goal_robot) == goal_pos

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        (bx, by) = node.state.board.robot_position("B")
        (rx, ry) = node.state.board.robot_position("R")
        (yx, yy) = node.state.board.robot_position("Y")
        (gx, gy) = node.state.board.robot_position("G")

        blue_weight = red_weight = yellow_weight = green_weight = self.initial.board.size

        if self.goal[0] == "R":
            red_weight = 1
        elif self.goal[0] == "B":
            blue_weight = 1
        elif self.goal[0] == "G":
            green_weight = 1
        elif self.goal[0] == "Y":
            yellow_weight = 1

        """if(self.goal[1][0] == node.state.board.size or self.goal[1][1] == node.state.board.size or
        self.goal[1][0] == 1 or self.goal[1][1] == 1):
            (x, y) = node.state.board.robot_position(self.goal[0])
            return abs(x - self.goal[1][0]) + abs(y - self.goal[1][1])"""

        return (abs(bx - self.goal[1][0]) + abs(by - self.goal[1][1])) * blue_weight + \
               (abs(rx - self.goal[1][0]) + abs(ry - self.goal[1][1])) * red_weight + \
               (abs(yx - self.goal[1][0]) + abs(yy - self.goal[1][1])) * yellow_weight + \
               (abs(gx - self.goal[1][0]) + abs(gy - self.goal[1][1])) * green_weight


if __name__ == "__main__":
    start_time = time.time()

    board = parse_instance(sys.argv[1])

    problem = RicochetRobots(board)
    # instrumentProblem = InstrumentedProblem(problem)

    node = astar_search(problem, problem.h)
    print("Execution time:",time.time() - start_time, "seconds")
    solution = []

    while(node.parent):
        solution = [node.action] + solution
        node = node.parent
    
    print(len(solution))
    for move in solution:
       print(move[0] + " " + move[1])