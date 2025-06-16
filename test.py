from ludo import *
import time
# import multiprocessing

random_color = "#{:02x}{:02x}{:02x}".format(
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255)
)

players1 = Player("green", "random")
# players1.set_DNA(np.array([0, 0, 0, 0, 0, 0, 0, 0]))
# players1.set_search_depth(3)
players2 = Player("yellow", "random")
players3 = Player("blue", "random")
players4 = Player("red", "random")
players = [players1, players2, players3, players4]

test_board = Board(players)

winner = None

while (winner == None):
    winner = test_board.play()

print(players1.wins, players2.wins, players3.wins, players4.wins)

# Variações possíveis:
# 1. Sistema de pontuação diferente (distantas percorridas pelos peões)
# 2. Fazer função condicional que force a escolha entre um número determinado de opções.


# Versão com múltiplos processos

# player1_wins = multiprocessing.Value('i', 0)
# player2_wins = multiprocessing.Value('i', 0)
# player3_wins = multiprocessing.Value('i', 0)
# player4_wins = multiprocessing.Value('i', 0)

# def play_game(num_games, player1_wins, player2_wins, player3_wins, player4_wins):
#     players1 = Player("green", "random")

#     players2 = Player("yellow", "random")
#     # players2.set_DNA(np.array([0, 0, 0, 0, 0, 0, 0, 0]))

#     players3 = Player("blue", "random")
#     # players3.set_DNA(np.array([0, 0, 0, 0, 0, 0, 0, 0]))

#     players4 = Player("red", "random")
#     # players4.set_DNA(np.array([0, 0, 0, 0, 0, 0, 0, 0]))

#     players = [players1, players2, players3, players4]
#     test_board = Board(players)

#     for i in range(num_games):
#         winner = None
#         while (winner == None):
#             winner = test_board.play()
#         for p in test_board.players_list:
#             p.restart_walk()

#     with player1_wins.get_lock():
#         player1_wins.value += players1.wins

#     with player2_wins.get_lock():
#         player2_wins.value += players2.wins

#     with player3_wins.get_lock():
#         player3_wins.value += players3.wins

#     with player4_wins.get_lock():
#         player4_wins.value += players4.wins

# if __name__ == "__main__":
#     processes = []
#     num_processes = 4

#     print("Iniciando processos...")
#     start_time = time.time()
#     for i in range(num_processes):
#         p = multiprocessing.Process(target=play_game, args=(250, player1_wins, player2_wins, player3_wins, player4_wins))
#         processes.append(p)
#         p.start() # Inicia a execução do processo

#     # Espera que todos os processos terminem suas execuções
#     for p in processes:
#         p.join() 

#     end_time = time.time()
    
#     print("\nTodos os processos terminaram.")
    
#     print(player1_wins.value, player2_wins.value, player3_wins.value, player4_wins.value) # depth 3 1000 jogos: 700 vitórias vs aleatório
#     print(f"Execution time: {(end_time - start_time):.2f} seconds") # depth 3 1000 jogos: 1840 segundos
