# A classe Player representa nossos indivíduos.
# A classe Board é usada para criar 4 Players.

import random
import numpy as np

NEIGHBOR_DISTANCE = 13  # Distância entre a entrada de um jogador e o próximo.

class Player:

    def __init__(self, name, think_type):

        self.name = name
        self.wins = 0

        if (think_type == "arbitrary"):
            self.choose_action = self.choose_action_arbitrary
        elif (think_type == "random"):
            self.choose_action = self.choose_random
        # elif (think_type == "neural"):
            # self.choose_action = self.choose_action_neural

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

    def play(self):

        outcome = self.players_list[self.turn].play_turn()

        if (outcome):
            self.players_list[self.turn].wins += 1

            return self.players_list[self.turn]
        else:
            self.turn = (self.turn + 1) % 4
            return None
