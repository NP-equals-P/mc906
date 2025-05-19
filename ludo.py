import random
from tkinter import * 

DISTANCE = 13 # Distância entre a entrada de um jogador e o próximo.

class Player_Scalar:
    def __init__(self, name, order):
        self.name = name
        self.order = order
        self.relative_start = DISTANCE*order + 1
        self.relative_end = self.relative_start + 58

        self.home_pawns = 4
        self.free_pawns = []
        self.end_pawns = 0

    def choose(self, dice_roll):
        if (self.home_pawns != 0 and (dice_roll == 1 or dice_roll == 6)):
            choice = random.randint(0, len(self.free_pawns))

            if choice == 0:
                return 0
            else:
                return self.free_pawns[choice - 1][1]
        else:
            choice = random.randint(1, len(self.free_pawns))
            return self.free_pawns[choice - 1][1]

    def free_pawn(self):
        self.home_pawns -= 1

        for pawn in self.free_pawns:
            if (pawn[1] == self.relative_start):
                pawn[0] += 1
                return
            
        self.free_pawns.append([1, self.relative_start])
        return

    def walk_pawn(self, pawn_number, dice_roll):
        for pawn in self.free_pawns:
            if (pawn[1] == pawn_number):
                self.free_pawns.remove(pawn)

                new_location = pawn[1] + dice_roll

                if (new_location == self.relative_end): # Se chegar exatamente no final => soma em end_pawns
                    self.end_pawns += pawn[0]
                    return
                elif (new_location > self.relative_end): # Se passar do final => volta algumas casas
                    new_location = self.relative_end - (new_location - self.relative_end)
                
                for i in range(len(self.free_pawns)):
                    if (self.free_pawns[i][1] == new_location):
                            self.free_pawns[i][0] += pawn[0]
                            return

                self.free_pawns.append([pawn[0], new_location])
                return

    def print_state(self):
        board = []
        board.append(self.home_pawns)

        for i in range(1, 60):
            board.append(0)

        for pawn in self.free_pawns:
            board[pawn[1]] = pawn[0]

        board.append(self.end_pawns)

        print(board)

    def play_turn(self, oponents):

        dice_roll = random.randint(1, 6)
        print(dice_roll)

        if (len(self.free_pawns) == 0):
            if (dice_roll == 1 or dice_roll == 6):

                self.free_pawn()

                if (dice_roll == 6):
                    return self.play_turn(oponents)
                else:
                    return False
            else:
                return False
        else:

            choice = self.choose(dice_roll)

            if (choice == False):
                self.free_pawn()
            else:
                self.walk_pawn(choice, dice_roll)
                if (self.end_pawns == 4):
                    return True
                
            if (dice_roll == 6):
                return self.play_turn(oponents)
            else:
                return False
            
amarelo = Player_Scalar("amarelo", 0)
flag = False
while (not flag):
    print()
    flag = amarelo.play_turn([])
    amarelo.print_state()
    input()

# root = Tk()

# class Application():
#     def __init__(self):
#         self.root = root
#         self.tela()
#         root.mainloop()
    
#     def tela(self):
#         self.root.title("Ludo")
#         self.root.configure(background="darkgray")
#         self.root.geometry("1000x800")
#         self.root.resizable(False, False)
        

# Application()