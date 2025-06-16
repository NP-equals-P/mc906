# A classe Player representa nossos indivíduos.
# A classe Board é usada para agrupar 4 Players e fazer um jogo entre eles.

import random
import numpy as np

NEIGHBOR_DISTANCE = 13  # Distância entre a entrada de um jogador e o próximo.

class Player:

    def __init__(self, name, think_type="random"):

        # "name" é somente para identificar um player. Não indica nada concreto.
        # "think_type" define que tipo de algoritmo de decisão o player usará (pode ser "random", "arbitrary", "neural" ou "search"):
        #  - "random": escolhe aleatoriamente qual peão andar.
        #  - "arbitrary": usa a função arbitrária que a gente criou.
        #  - "neural": usa uma rede neural para escolher qual peão andar.
        #  - "search": usa um algoritmo de busca para escolher qual peão andar.
        # "walk" é o vetor que representa o caminho que esse player percorre.

        self.name = name
        self.wins = 0
        self.fitness = 0.0
        self.board = None
        self.search_depth = 2
        self.DNA = None

        if (think_type == "arbitrary"):
            self.choose_action = self.choose_action_arbitrary
        elif (think_type == "search"):
            self.choose_action = self.choose_action_search
        elif (think_type == "neural"):
            self.choose_action = self.choose_action_neural
        else:
            self.choose_action = self.choose_action_random

        self.walk = np.zeros(58)
        self.walk[0] = 4

    def restart_walk(self):
        # Reinicia o vetor de andamentos do jogador.

        self.walk = np.zeros(58)
        self.walk[0] = 4

    def set_oponents(self, oponents):
        self.oponents = oponents

    def set_DNA(self, DNA):
        self.DNA = DNA

    def set_search_depth(self, value):
        self.search_depth = value

    def set_board(self, board):
        self.board = board

    def set_cosmedics(self, order, color=None):
        # Define a ordem do jogador e a cor que ele usará.

        if color is not None:
            self.color = color
        else:
            self.color = "#{:02x}{:02x}{:02x}".format(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
        self.order = order

    def set_safe_spots(self):
        self.safe_spots = np.zeros(58)
        self.safe_spots[0] = 1
        self.safe_spots[1] = 1
        self.safe_spots[9] = 1
        self.safe_spots[22] = 1
        self.safe_spots[27] = 1
        self.safe_spots[35] = 1
        self.safe_spots[40] = 1
        self.safe_spots[48] = 1
        self.safe_spots[52] = 1
        self.safe_spots[53] = 1
        self.safe_spots[54] = 1
        self.safe_spots[55] = 1
        self.safe_spots[56] = 1
        self.safe_spots[57] = 1

    def play_turn(self):

        # Joga o dado.
        dice_roll = random.randint(1, 6) 

        # Escolhe qual peão andar (ou liberar).
        choice = self.choose_action(dice_roll)

        # Se escolha for 0, libere um peão. Se for <None>, perca a vez. Se for qualquer outro número, ande o peão da respectiva casa e cheque se ganhou.
        if (choice == 0):
            self.free_pawn()
        elif choice == None:
            return False
        else:
            self.walk_pawn(choice, dice_roll)

            if (self.walk[57] == 4):
                return True
                
        # Se rodou 6, jogue novamente.
        if (dice_roll == 6):
            return self.play_turn()
        else:
            return False

    def free_pawn(self):
        # Libera um peão da primeira casa.

        self.walk[0] -= 1
        self.walk[1] += 1

        self.check_collision(1)

        return

    def choose_action_random(self, dice_roll):

        # Pega os índices em que há peões (não-zeros), sem considerar a última casa.
        indexes_walk = np.nonzero(self.walk[:-1])
        indexes_walk = list(indexes_walk[0])

        # Se não rodou 1 nem 6 e ainda há peões na primeira casa, retira a opção de liberar o peão.
        if dice_roll != 1 and dice_roll != 6:
            if indexes_walk[0] == 0:
                indexes_walk = indexes_walk[1:]

            # Se a primeira casa era a única opção, não retorna nada.
            if len(indexes_walk) == 0:
                return None
        
        # Retorna um índice aleatório de onde há peões jogáveis.
        return indexes_walk[random.randint(0, len(indexes_walk) - 1)]

    def choose_action_arbitrary(self, dice_roll):

        weights = self.DNA

        indexes_walk = np.nonzero(self.walk[:-1])[0].tolist();
        if not indexes_walk:
            return None;
        # Não sei se isso aqui deveria voltar None, porque se cair aqui, é porque todo mundo já chegou no final

        if dice_roll != 1 and dice_roll != 6:
            if 0 in indexes_walk:
                indexes_walk.remove(0)

        if len(indexes_walk) == 0:
            return None

        scores = []
        for i in indexes_walk:
            features = self.extract_features(i, dice_roll)
            score = np.dot(weights, features)
            scores.append((i, score))

        best, best_score = max(scores, key=lambda x: x[1]);
        return best

    def choose_action_neural(self, dice_roll):

        pesos, bias = self.DNA

        # Concatena os 4 vetores walk de cada player e o dice_roll em um único vetor de entrada
        input_vec = np.concatenate([
            self.walk,
            self.oponents[0].walk,
            self.oponents[1].walk,
            self.oponents[2].walk,
            np.array([dice_roll])
        ])

        # Calcula a saída da rede neural: saída = pesos @ input_vec + bias
        output = np.dot(pesos.T, input_vec) + bias

        best = np.argmax(output)

        indexes_walk = np.nonzero(self.walk[:-1])
        indexes_walk = list(indexes_walk[0])

        # print(best)

        if best + 1 > len(indexes_walk):
            # print("        00000000")
            if (0 in indexes_walk):
                best = random.choice(indexes_walk)
            else:
                best = random.choice(indexes_walk)

        else:
            # print("00000000")
            best = indexes_walk[best]

        return best

    def choose_action_search(self, dice_roll):
        sim_board = SimulatedBoard(self.board)
        return expectimax(sim_board.players_list[sim_board.turn], sim_board, dice_roll)

    def extract_features(self, position, dice_roll):
        future_position = position + dice_roll
        distance = 57 - future_position

        risk = 0;
        if future_position <= 51:
            for player in self.oponents:
                for pos in np.nonzero(player.walk[:52])[0]:
                    relative_position = (pos + 13*(4 - (player.order - self.order))) % 52;
                    if relative_position <= 51 and relative_position > 0:
                        if 0 < future_position - relative_position <= 6:    
                            risk += 1

        capture = 0;
        if future_position <= 51:
            for player in self.oponents:
                if player.walk[future_position] != 0 and player.safe_spots[future_position] != 1:
                    capture += player.walk[future_position]

        can_leave = int(position == 0 and (dice_roll == 6 or dice_roll == 1))
        is_hallway = int(future_position > 51);
        can_stack = int(position == 1 and self.walk[0] > 0);
        is_safe = int(self.safe_spots[position] == 1);
        if future_position > 57:
            future_position = 57 - (future_position - 57)
        will_be_safe = int(self.safe_spots[future_position] == 1);

        return np.array([distance, risk, capture, can_leave, is_hallway, can_stack, is_safe, will_be_safe])

    def walk_pawn(self, choice, dice_roll):
        # Andar o peão da casa "choice" com o dado "dice_roll".
        # Se a casa alvo não passar do final, ande normalmente.
        # Se a casa alvo passar do final, ande até o final e volte para a casa "aux".

        if (choice + dice_roll <= 57):
            self.walk[choice + dice_roll] += self.walk[choice]
            self.walk[choice] = 0

            self.check_collision(choice + dice_roll)
        else:
            aux = 57 - (dice_roll + choice - 57)

            if (aux != choice):
                self.walk[aux] += self.walk[choice]
                self.walk[choice] = 0

    def check_collision(self, position):
        # Verifica se há colisão com outros jogadores e atualiza o vetor dos respectivos adversários.

        if (position <= 51):
            for player in self.oponents:
                relative_position = (position + 13*(4 - (player.order - self.order))) % 52

                if (relative_position <= 51 and relative_position > 0):
                    if (player.safe_spots[relative_position] != 1):
                        if (player.walk[relative_position] != 0):
                            player.walk[0] += player.walk[relative_position]
                            player.walk[relative_position] = 0

class Board:

    def __init__(self, players, color_type="random"):

        # Recebe os players e define a ordem de cada um (ordem de chegada).
        # Define as cores para cada player.
        # Guarda o estado "turn" que indica qual é o player da vez.
        # Usa a função "play()" para fazer uma jogada com o player da vez.

        self.turn = 0

        green_player = players[0]
        yellow_player = players[1] 
        blue_player = players[2] 
        red_player = players[3]

        if color_type == "random":
            green_player.set_cosmedics(0)
            yellow_player.set_cosmedics(1)
            blue_player.set_cosmedics(2)
            red_player.set_cosmedics(3)
        elif color_type == "fixed":
            green_player.set_cosmedics(0, "green")
            yellow_player.set_cosmedics(1, "yellow")
            blue_player.set_cosmedics(2, "deep sky blue")
            red_player.set_cosmedics(3, "red")

        green_player.set_oponents([yellow_player, blue_player, red_player])
        yellow_player.set_oponents([green_player, blue_player, red_player])
        blue_player.set_oponents([yellow_player, green_player, red_player])
        red_player.set_oponents([yellow_player, blue_player, green_player])

        green_player.set_safe_spots()
        yellow_player.set_safe_spots()
        blue_player.set_safe_spots()
        red_player.set_safe_spots()

        green_player.set_board(self)
        yellow_player.set_board(self)
        blue_player.set_board(self)
        red_player.set_board(self)

        self.players_list = [green_player, yellow_player, blue_player, red_player]

    def play(self):

        outcome = self.players_list[self.turn].play_turn()

        if (outcome):
            self.players_list[self.turn].wins += 1

            return self.players_list[self.turn]
        else:
            self.turn = (self.turn + 1) % 4
            return None
        
class SimulatedPlayer(Player):
    def __init__(self, player: Player):
        self.name = player.name
        self.wins = player.wins
        self.choose_action = player.choose_action
        self.walk = np.copy(player.walk)
        self.oponents = None
        self.color = player.color
        self.order = player.order
        self.DNA = np.copy(player.DNA)
        self.board = None
        self.search_depth = player.search_depth
        self.safe_spots = np.copy(player.safe_spots)

    def get_possible_moves(self, dice_roll):
        pawns = np.nonzero(self.walk)[0]
        possible_moves = []
        for pawn in pawns:
            if pawn != 0:
                if pawn + dice_roll <= 57:
                    possible_moves.append(pawn)
            elif dice_roll == 1 or dice_roll == 6:
                possible_moves.append(pawn)

        return possible_moves

    def play_move(self, move, dice_roll):
        if (move == 0):
            self.free_pawn()
        elif move == None:
            return "next_turn"
        else:
            self.walk_pawn(move, dice_roll)

            if (self.walk[57] == 4):
                return "game_over"
                
        # Se rodou 6, jogue novamente.
        if (dice_roll == 6):
            return "same_turn"
        else:
            return "next_turn"
        
    def score(self):
        scores = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        positions = np.nonzero(self.walk)[0]
        for pos in positions:
            distance = 57 - pos;

            risk = 0
            if pos <= 51:
                for player in self.oponents:
                    for pos in np.nonzero(player.walk[:52])[0]:
                        relative_position = (pos + 13*(4 - (player.order - self.order))) % 52;
                        if relative_position <= 51 and relative_position > 0:
                            if 0 < pos - relative_position <= 6:    
                                risk += 1

            capture = 0;
            if pos <= 51:
                for player in self.oponents:
                    capture += player.walk[0]

            is_hallway = int(pos > 51)
            has_stacked = int(self.walk[pos] > 1)
            is_safe = int(self.safe_spots[pos] == 1)

            scores = (scores + np.array([distance, risk, capture, 0, is_hallway, has_stacked, is_safe, 0])) # can_leave e will_be_safe não são relevantes
            # score() avalia estado atual ao invés de estado futuro

        has_left = 4 - self.walk[0]
        scores[3] = has_left

        return self.DNA @ scores


class SimulatedBoard(Board):
    def __init__(self, board: Board):
        self.turn = board.turn
        self.players_list = []
        for player in board.players_list:
            self.players_list.append(SimulatedPlayer(player))

        sim_players = self.players_list
        sim_players[0].set_oponents([sim_players[1], sim_players[2], sim_players[3]])
        sim_players[1].set_oponents([sim_players[0], sim_players[2], sim_players[3]])
        sim_players[2].set_oponents([sim_players[0], sim_players[1], sim_players[3]])
        sim_players[3].set_oponents([sim_players[0], sim_players[1], sim_players[2]])

        for player in self.players_list:
            player.board = self

    def play(self, move, dice_roll):

        outcome = self.players_list[self.turn].play_move(move, dice_roll)

        if outcome == "game_over":
            return "game_over"
        elif outcome == "next_turn":
            self.turn = (self.turn + 1) % 4
            return None      
        else:
            return None

def expectimax_min(search_player: SimulatedPlayer, board: SimulatedBoard, dice_roll, depth):
    if depth == 0:
        return search_player.score()
    
    current_player: SimulatedPlayer = None
    for player in board.players_list:
        if player.order == board.turn:
            current_player = player
            break

    best_value = float("inf")
    possible_moves = current_player.get_possible_moves(dice_roll)

    if len(possible_moves) == 0:
        next_board = SimulatedBoard(board)
        next_board.play(None, dice_roll)
        value = 0
        for roll in range(1, 7):
            if next_board.turn == search_player.order:
                value += (1 / 6) * expectimax_max(search_player, next_board, roll, depth - 1)
            else:
                value += (1 / 6) * expectimax_min(search_player, next_board, roll, depth - 1)
            
        return value

    for move in possible_moves:
        next_board = SimulatedBoard(board)
        if next_board.play(move, dice_roll) == "game_over":
            return -999999999
        value = 0
        for roll in range(1, 7):
            if next_board.turn == search_player.order:
                value += (1 / 6) * expectimax_max(search_player, next_board, roll, depth - 1)
            else:
                value += (1 / 6) * expectimax_min(search_player, next_board, roll, depth - 1)
            
        if value < best_value:
            best_value = value

    return best_value

def expectimax_max(search_player: SimulatedPlayer, board: SimulatedBoard, dice_roll, depth):
    if depth == 0:
        return search_player.score()
    
    current_player: SimulatedPlayer = None
    for player in board.players_list:
        if player.order == board.turn:
            current_player = player
            break

    best_value = -float("inf")
    possible_moves = current_player.get_possible_moves(dice_roll)

    if len(possible_moves) == 0:
        next_board = SimulatedBoard(board)
        next_board.play(None, dice_roll)
        value = 0
        for roll in range(1, 7):
            if next_board.turn == search_player.order:
                value += (1 / 6) * expectimax_max(search_player, next_board, roll, depth - 1)
            else:
                value += (1 / 6) * expectimax_min(search_player, next_board, roll, depth - 1)
            
        return value

    for move in possible_moves:
        next_board = SimulatedBoard(board)
        if next_board.play(move, dice_roll) == "game_over":
            return 999999999
        value = 0
        for roll in range(1, 7):
            if next_board.turn == search_player.order:
                value += (1 / 6) * expectimax_max(search_player, next_board, roll, depth - 1)
            else:
                value += (1 / 6) * expectimax_min(search_player, next_board, roll, depth - 1)
            
        if value > best_value:
            best_value = value

    return best_value

def expectimax(search_player: SimulatedPlayer, board: SimulatedBoard, dice_roll):
    best_move = None
    possible_moves = search_player.get_possible_moves(dice_roll)
    if len(possible_moves) == 0:
        return best_move

    best_value = -float("inf")
    for move in possible_moves:
        next_board = SimulatedBoard(board)
        if next_board.play(move, dice_roll) == "game_over":
            return move
        
        value = 0
        for roll in range(1, 7):
            if next_board.turn == search_player.order:
                value += (1 / 6) * expectimax_max(search_player, next_board, roll, search_player.search_depth - 1)
            else:
                value += (1 / 6) * expectimax_min(search_player, next_board, roll, search_player.search_depth - 1)
            
        if value > best_value:
            best_value = value
            best_move = move

    return best_move