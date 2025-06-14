import numpy as np
import random
import time

EXPECTIMAX_DEPTH = 3

NEIGHBOR_DISTANCE = 13  # Distância entre a entrada de um jogador e o próximo.

class Player:

    def __init__(self, name, think_type):

        self.name = name
        self.wins = 0
        self.board = None
        self.DNA = [0, 0, 0, 0, 0, 0]

        if (think_type == "arbitrary"):
            self.choose_action = self.choose_action_arbitrary
        elif (think_type == "random"):
            self.choose_action = self.choose_random
        elif (think_type == "search"):
            self.choose_action = self.choose_action_search

        self.walk = np.zeros(58)
        self.walk[0] = 4

    def restart_walk(self):
        self.walk = np.zeros(58)
        self.walk[0] = 4

    def set_oponents(self, oponents):
        self.oponents = oponents

    def set_DNA(self, DNA):
        self.DNA = DNA

    def set_cosmedics(self, order, color=None):
        if color is not None:
            self.color = color
        else:
            self.color = "#{:02x}{:02x}{:02x}".format(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
        self.order = order

    def play_turn(self):

        # Joga o dado.
        dice_roll = random.randint(1, 6) 

        # Escolhe qual peão andar (ou liberar).
        choice = self.choose_action(dice_roll)

        # Se escolha for 0, libere um peão. Se for None, perca a vez. Se for qualquer outro número, ande o peão da respectiva casa e cheque se ganhou.
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
         
        self.walk[0] -= 1
        self.walk[1] += 1

        self.check_collision(1)

        return

    def choose_random(self, dice_roll):

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
                indexes_walk.remove(0);

        if len(indexes_walk) == 0:
            return None;

        scores = [];
        for i in indexes_walk:
            features = self.extract_features(i, dice_roll);
            score = np.dot(weights, features);
            scores.append((i, score));

        best, best_score = max(scores, key=lambda x: x[1]);
        return best;

    def choose_action_search(self, dice_roll):
        sim_board = SimulatedBoard(self.board)
        return expectimax(sim_board.players_list[sim_board.turn], sim_board, dice_roll)

    def extract_features(self, position, dice_roll):
        future_position = position + dice_roll;
        distance = 57 - future_position;

        risk = 0;
        if future_position <= 51:
            for player in self.oponents:
                for pos in np.nonzero(player.walk[:52])[0]:
                    relative_position = (pos + 13*(4 - (player.order - self.order))) % 52;
                    if relative_position <= 51 and relative_position > 0:
                        if 0 < future_position - relative_position <= 6:    
                            risk += 1;

        capture = 0;
        if future_position <= 51:
            for player in self.oponents:
                if player.walk[future_position] != 0:
                    capture += player.walk[future_position];


        can_leave = int(position == 0 and (dice_roll == 6 or dice_roll == 1));
        is_hallway = int(future_position > 51);
        can_stack = int(position == 1 and self.walk[0] > 0);

        return np.array([distance, risk, capture, can_leave, is_hallway, can_stack]);

    def walk_pawn(self, choice, dice_roll):
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

        if (position <= 51):
            for player in self.oponents:
                relative_position = (position + 13*(4 - (player.order - self.order))) % 52

                if (relative_position <= 51 and relative_position > 0):
                    if (player.walk[relative_position] != 0):
                        player.walk[0] += player.walk[relative_position]
                        player.walk[relative_position] = 0

class Board:

    def __init__(self, players, color_type="random"):

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

        self.players_list = [green_player, yellow_player, blue_player, red_player]
        
        for player in self.players_list:
            player.board = self

    def play(self):

        outcome = self.players_list[self.turn].play_turn()

        if (outcome):
            self.players_list[self.turn].wins += 1

            return self.players_list[self.turn]
        else:
            self.turn = (self.turn + 1) % 4
            return None

class SimulatedPlayer(Player):
    def __init__(self, player: Player, stacking_factor=100):
        self.name = player.name
        self.wins = player.wins
        self.choose_action = player.choose_action
        self.walk = np.copy(player.walk)
        self.oponents = None
        self.color = player.color
        self.order = player.order
        self.DNA = np.copy(player.DNA)
        self.stacking_factor = stacking_factor
        self.board = None

    def get_possible_moves(self, dice_roll):
        pawns = np.nonzero(self.walk)[0]
        possible_moves = []
        for pawn in pawns:
            if pawn != 0:
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
        scores = np.array([0, 0, 0, 0, 0, 0])
        pawns = np.nonzero(self.walk)[0]
        for pawn in pawns:
            scores = (scores + self.extract_features(pawn, 0))

        scores[2] = int(scores[2] > 0)
        scores[3] = int(scores[3] > 0)
        scores[4] = int(scores[4] > 0)
        
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
            self.players_list[self.turn].wins += 1
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

    if possible_moves == None:
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
            return -99999999
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

    if possible_moves == None:
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
            return 99999999
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
    if possible_moves == None:
        return best_move

    best_value = -float("inf")
    for move in possible_moves:
        next_board = SimulatedBoard(board)
        if next_board.play(move, dice_roll) == "game_over":
            return move
        
        value = 0
        for roll in range(1, 7):
            value += (1 / 6) * expectimax_min(search_player, next_board, roll, EXPECTIMAX_DEPTH - 1)
            
        if value > best_value:
            best_value = value
            best_move = move

    return best_move

# DNA: [distance, risk, capture, can_leave, is_hallway, can_stack]
players1 = Player("green", "search")
players1.set_DNA(np.array([-1000, 100, 500, 1000, 1000, 500]))

players2 = Player("yellow", "random")

players3 = Player("blue", "random")

players4 = Player("red", "random")

players = [players1, players2, players3, players4]


test_board = Board(players)

start_time = time.time()

for i in range(1000):
    winner = None
    while (winner == None):
        winner = test_board.play()
    for p in test_board.players_list:
        p.restart_walk()

end_time = time.time()

print(players1.wins, players2.wins, players3.wins, players4.wins)
print(f"Execution time: {(end_time - start_time):.2f} seconds")