import random
import numpy as np

NEIGHBOR_DISTANCE = 13  # Distância entre a entrada de um jogador e o próximo.

class Player:    # Jogador de Ludo (usando a representação vetorial).

    def __init__(self, name, order, color):
        self.name = name
        self.order = order
        self.color = color

        self.walk = np.zeros(58)
        self.walk[0] = 4

    def set_oponents(self, oponents):
        self.oponents = oponents

    def play_turn(self, weights):

        dice_roll = random.randint(1, 6)
        # print("Valor do dado: ", dice_roll)

        choice = self.choose_random(dice_roll)
        # choice = self.choose_action(weights, dice_roll);

        # print("Escolha:",  choice)

        if (choice == 0):
            self.free_pawn()
        elif choice == None:
            if self.walk[57] == 4:
                return True;
                # Coloquei isos aqui por causa do comentário abaixo, mas não sei se ele tá certo
            return False
            # Tem o caso de quando todo mundo cheguo no final, ele retorna None, mas aqui ta dando False, mas deveria ser True eu acho
        else:
            self.walk_pawn(choice, dice_roll)
            if (self.walk[57] == 4):
                return True
                
        if (dice_roll == 6):
            # self.print_state()
            return self.play_turn()
        else:
            return False

    def free_pawn(self):             # Libertar um peão.
         
        self.walk[0] -= 1
        self.walk[1] += 1

        self.check_collision(1)

        return

    def choose_random(self, dice_roll):

        indexes_walk = np.nonzero(self.walk[:-1])
        indexes_walk = list(indexes_walk[0])

        if (not indexes_walk):
            return None

        if dice_roll != 1 and dice_roll != 6:
            if indexes_walk[0] == 0:
                indexes_walk = indexes_walk[1:]

        if len(indexes_walk) == 0:
            return None
        return indexes_walk[random.randint(0, len(indexes_walk) - 1)]

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

    def print_state(self):
        print(self.walk)



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


    def choose_action(self, weights, dice_roll):

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


class Board:

    def __init__(self):

        self.turn = 0

        green_player = Player("green", 0, "green")
        yellow_player = Player("yellow", 1, "yellow")
        blue_player = Player("blue", 2, "deepskyblue")
        red_player = Player("red", 3, "red")

        green_player.set_oponents([yellow_player, blue_player, red_player])
        yellow_player.set_oponents([green_player, blue_player, red_player])
        blue_player.set_oponents([yellow_player, green_player, red_player])
        red_player.set_oponents([yellow_player, blue_player, green_player])

        self.players_list = [green_player, yellow_player, blue_player, red_player]

    def play(self):

        outcome = self.players_list[self.turn].play_turn()

        if (outcome):
            return self.players_list[self.turn]
        else:
            self.turn = (self.turn + 1) % 4
            return None
