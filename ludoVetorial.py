import random
import numpy as np

NEIGHBOR_DISTANCE = 13  # Distância entre a entrada de um jogador e o próximo.

class Player_Vector:    # Jogador de Ludo (usando a representação vetorial).

    number_players = 0 

    def __init__(self, name):
        self.name = name
        self.order = self.number_players
        self.number_players += 1

        self.walk = np.zeros(58)
        self.walk[0] = 4;

    def play_turn(self, oponents):

        dice_roll = random.randint(1, 6)
        print("Valor do dado: ", dice_roll);



        choice = self.choose_random(dice_roll)

        print("Choice:",  choice)

        if (choice == 0):
            self.free_pawn()
        elif choice == None:
            return False;
        else:
            self.walk_pawn(choice, dice_roll)
            if (self.walk[57] == 4):
                return True
                
        if (dice_roll == 6):
            self.print_state();
            return self.play_turn(oponents)
        else:
            return False

    def free_pawn(self):             # Libertar um peão.
         
        self.walk[0] -= 1;
        self.walk[1] += 1;

        return

    def choose_random(self, dice_roll):

        indexes_walk = np.nonzero(self.walk[:-1])
        indexes_walk = list(indexes_walk[0]);

        if dice_roll != 1 and dice_roll != 6:
            if indexes_walk[0] == 0:
                indexes_walk = indexes_walk[1:];

        if len(indexes_walk) == 0:
            return None;
        return indexes_walk[random.randint(0, len(indexes_walk) - 1)]


    def walk_pawn(self, choice, dice_roll):
        if (choice + dice_roll <= 57):
            self.walk[choice + dice_roll] += self.walk[choice]
            self.walk[choice] = 0
        else:
            aux = 57 - (dice_roll + choice - 57)

            if (aux != choice):
                self.walk[aux] += self.walk[choice]
                self.walk[choice] = 0

    def print_state(self):
        print(self.walk)

amarelo = Player_Vector("amarelo")

flag = False

while (not flag):
    flag = amarelo.play_turn([])
    amarelo.print_state()
    input()
    if flag == True:
        print("Tamo junto");

