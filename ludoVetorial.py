import random
import numpy as np

NEIGHBOR_DISTANCE = 13  # Distância entre a entrada de um jogador e o próximo.

class Player_Vector:    # Jogador de Ludo (usando a representação vetorial).

    number_players = 0 
    players = []

    def __init__(self, name):
        self.name = name
        self.order = self.number_players
        Player_Vector.number_players += 1
        self.players.append(self)

        self.walk = np.zeros(58)
        self.walk[0] = 4

    def play_turn(self):

        dice_roll = random.randint(1, 6)
        print("Valor do dado: ", dice_roll)

        choice = self.choose_random(dice_roll)

        print("Escolha:",  choice)

        if (choice == 0):
            self.free_pawn()
        elif choice == None:
            return False
        else:
            self.walk_pawn(choice, dice_roll)
            if (self.walk[57] == 4):
                return True
                
        if (dice_roll == 6):
            self.print_state()
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
            for player in self.players:
                if (player != self):
                    relative_position = (position + 13*(4 - (player.order - self.order))) % 52

                    if (relative_position <= 51 and relative_position > 0):
                        if (player.walk[relative_position] != 0):
                            print("HIIIIIIIIIIIIIIITTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT!!!!!", position, relative_position, player.order, self.order, player.name)
                            player.walk[0] += player.walk[relative_position]
                            player.walk[relative_position] = 0

    def print_state(self):
        print(self.walk)

verde = Player_Vector("verde")
amarelo = Player_Vector("amarelo")
azul = Player_Vector("azul")
vermelho = Player_Vector("vermelho")


flag1 = False
flag2 = False
flag3 = False
flag4 = False
while (not (flag1 or flag2 or flag3 or flag4)):
    print("Verde:")
    flag1 = verde.play_turn()
    verde.print_state()
    input()

    print("Amarelo")
    flag2 = amarelo.play_turn()
    amarelo.print_state()
    input()

    print("Azul")
    flag3 = azul.play_turn()
    azul.print_state()
    input()

    print("Vermelho")
    flag3 = vermelho.play_turn()
    vermelho.print_state()
    input()

print("Tamo junto")

