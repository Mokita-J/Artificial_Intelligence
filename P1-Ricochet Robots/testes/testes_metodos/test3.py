# test3.py: testa actions e goal_test

from ricochet_robots import *

# Ler tabuleiro do ficheiro "i1.txt":
board = parse_instance("instances/i1.txt")
problem = RicochetRobots(board)
s0 = RRState(board)

# Aplicar as ações que resolvem a instância
print(('B', 'l') in problem.actions(s0))
s1 = problem.result(s0, ('B', 'l'))
print("+++++++", s1.board.robot_position('B'))
print(('Y', 'u') in problem.actions(s1))
s2 = problem.result(s1, ('Y', 'u'))
print("+++++++", s2.board.robot_position('Y'))
print(('R', 'r') in problem.actions(s2))
s3 = problem.result(s2, ('R', 'r'))
print("+++++++", s3.board.robot_position('R'))
print(('R', 'u') in problem.actions(s3))
s4 = problem.result(s3, ('R', 'u'))
print("+++++++", s4.board.robot_position('R'))

# Verificar que o robô está no alvo só no último estado:
print(problem.goal_test(s0))
print(problem.goal_test(s1))
print(problem.goal_test(s2))
print(problem.goal_test(s3))
print(problem.goal_test(s4))
print(s4.board.robot_position('R'))

# ---
# Ler tabuleiro do ficheiro "i11.txt":
board = parse_instance("instances/i11.txt")
problem = RicochetRobots(board)
s0 = RRState(board)
print("===============instance11================")
# Aplicar as ações que resolvem a instância
print(('Y', 'l') in problem.actions(s0))
s1 = problem.result(s0, ('Y', 'l'))
print("+++++++", s1.board.robot_position('Y'))
print(('R', 'l') in problem.actions(s1))
s2 = problem.result(s1, ('R', 'l'))
print("+++++++", s2.board.robot_position('R'))
print(('R', 'u') in problem.actions(s2))
s3 = problem.result(s2, ('R', 'u'))
print("+++++++", s3.board.robot_position('R'))
print(('B', 'd') in problem.actions(s3))
s4 = problem.result(s3, ('B', 'd'))
print("+++++++", s4.board.robot_position('B'))
print(('B', 'r') in problem.actions(s4))
s5 = problem.result(s4, ('B', 'r'))
print("+++++++", s5.board.robot_position('B'))
print(('B', 'u') in problem.actions(s5))
s6 = problem.result(s5, ('B', 'u'))
print("+++++++", s6.board.robot_position('B'))
print(('B', 'r') in problem.actions(s6))
s7 = problem.result(s6, ('B', 'r'))
print("+++++++", s7.board.robot_position('B'))
print(('B', 'd') in problem.actions(s7))
s8 = problem.result(s7, ('B', 'd'))
print("+++++++", s8.board.robot_position('B'))
print(('B', 'r') in problem.actions(s8))
s9 = problem.result(s8, ('B', 'r'))
print("+++++++", s9.board.robot_position('B'))

# Verificar que o robô está no alvo só no último estado:
print(problem.goal_test(s1))
print(problem.goal_test(s2))
print(problem.goal_test(s3))
print(problem.goal_test(s4))
print(problem.goal_test(s5))
print(problem.goal_test(s6))
print(problem.goal_test(s7))
print(problem.goal_test(s8))
print(problem.goal_test(s9))
print(s7.board.robot_position('B'))
