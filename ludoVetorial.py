import random
import numpy as np

NEIGHBOR_DISTANCE = 13  # Distância entre a entrada de um jogador e o próximo.

class Player_Vector:    # Jogador de Ludo (usando a representação vetorial).

    number_players = 0 

    def __init__(self, name):
        self.name = name
        self.order = self.number_players
        self.number_players += 1

        self.home_pawns = 4
        self.walk = np.zeros(59)

    def play_turn(self, oponents):

        dice_roll = random.randint(1, 6)
        print(dice_roll)

        if (self.home_pawns == 4):                            # Se não houver peões para andar.
            if (dice_roll == 1 or dice_roll == 6):

                self.free_pawn()

                if (dice_roll == 6):
                    return self.play_turn(oponents)
                else:
                    return False
            else:
                return False
        else:

            choice = self.choose_random(dice_roll)

            print("Choice:",  choice)

            if (choice == "Libertar"):
                self.free_pawn()
            else:
                self.walk_pawn(choice, dice_roll)
                if (self.walk[58] == 4):
                    return True
                
            if (dice_roll == 6):
                return self.play_turn(oponents)
            else:
                return False

    def free_pawn(self):             # Libertar um peão.
         
        self.home_pawns -= 1

        self.walk[0] += 1

        return

    def choose_random(self, dice_roll):

        indexes_walk = np.nonzero(self.walk[:-1])

        if ((dice_roll == 1 or dice_roll == 6) and self.home_pawns != 0):
            choices = ["Libertar"] + list(indexes_walk[0])
        else:
            choices = list(indexes_walk[0])

        return choices[random.randint(0, len(choices) - 1)]

    def walk_pawn(self, choice, dice_roll):
        if (choice + dice_roll <= 58):
            self.walk[choice + dice_roll] += self.walk[choice]
            self.walk[choice] = 0
        else:
            aux = 58 - (dice_roll + choice - 58)

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
