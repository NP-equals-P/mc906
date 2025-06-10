from tkinter import *
from ludo import *
import random


CELL_SIDE = 60
PAWN_WIDTH = 3
PAWN_RADIUS = 8

root = Tk()

class Application():
    def __init__(self, board):
        self.board = board
        self.root = root
        self.tela()
        # self.printar_estado()
        # root.mainloop()
    
    def tela(self):
        self.root.title("Ludo")
        self.root.configure(background="darkgray")
        self.root.geometry("850x900")
        self.boardFrame = Frame(self.root, height=CELL_SIDE*15, width=CELL_SIDE*15, highlightbackground="black", highlightthickness=1)
        # self.root.resizable(False, False)
        
    def printar_quadrante(self, cor, ordem, num_peoes):

        originx = 0
        originy = 0

        match(ordem):
            case (1):
                originx = 9
                originy = 0
            case(2):
                originx = 9
                originy = 9
            case(3):
                originx = 0
                originy = 9

        canvas = Canvas(self.boardFrame, width=6 * CELL_SIDE, height=6 * CELL_SIDE, bg="white", highlightthickness=0)
        canvas.create_rectangle(0, 0, 6*CELL_SIDE, 6*CELL_SIDE, fill=cor)
        canvas.create_rectangle(CELL_SIDE, CELL_SIDE, 5*CELL_SIDE-1, 5*CELL_SIDE - 1, fill="white")

        if (num_peoes >= 1):
            x, y, r = 2*CELL_SIDE, 2*CELL_SIDE, PAWN_RADIUS*1.5
            canvas.create_oval(x - r, y - r, x + r, y + r, fill=cor, outline="black", width=PAWN_WIDTH)

            if (num_peoes >= 2):
                x, y, r = 4*CELL_SIDE, 2*CELL_SIDE, PAWN_RADIUS*1.5
                canvas.create_oval(x - r, y - r, x + r, y + r, fill=cor, outline="black", width=PAWN_WIDTH)

                if (num_peoes >= 3):
                    x, y, r = 2*CELL_SIDE, 4*CELL_SIDE, PAWN_RADIUS*1.5
                    canvas.create_oval(x - r, y - r, x + r, y + r, fill=cor, outline="black", width=PAWN_WIDTH)

                    if (num_peoes >= 4):
                        x, y, r = 4*CELL_SIDE, 4*CELL_SIDE, PAWN_RADIUS*1.5
                        canvas.create_oval(x - r, y - r, x + r, y + r, fill=cor, outline="black", width=PAWN_WIDTH)

        canvas.grid(row=originy, column=originx, rowspan=6, columnspan=6)

    def printar_caminho(self):

        white_cell_list = []
        
        for i in range(52):
            canvas = Canvas(
                self.boardFrame,
                height=CELL_SIDE,
                width=CELL_SIDE,
                bg="white",
                highlightthickness=0
            )
            canvas.create_rectangle(0, 0, CELL_SIDE - 1, CELL_SIDE - 1, outline="black", width=1)
            white_cell_list.append(canvas)

        # Mapeia a casa inicial de cada jogador
        start_cells = {
            0: 0,    # green
            1: 13,   # yellow
            2: 26,   # blue
            3: 39    # red
        }

        # Cores dos jogadores (assumindo que board.players_list[order].color está definido corretamente)
        player_colors = {p.order: p.color for p in self.board.players_list}

        # Adiciona marcador colorido nas células iniciais
        for player_order, cell_index in start_cells.items():
            canvas = white_cell_list[cell_index]

            # Coordenadas para o marcador
            center = CELL_SIDE // 2
            radius = PAWN_RADIUS + 2

            canvas.create_oval(
                center - radius*2, center - radius*2,
                center + radius*2, center + radius*2,
                outline=player_colors[player_order],
                width=PAWN_WIDTH,
                fill="white"  # anel branco com borda colorida
            )

        green_cell_list = []
        yellow_cell_list = []
        blue_cell_list = []
        red_cell_list = []

        colorful_cell_list = [green_cell_list, yellow_cell_list, blue_cell_list, red_cell_list]

        for i in range(6):
            for cell_list, color in zip(
                [green_cell_list, yellow_cell_list, blue_cell_list, red_cell_list],
                [p.color for p in self.board.players_list]
            ):
                canvas = Canvas(self.boardFrame, bg=color, height=CELL_SIDE, width=CELL_SIDE, highlightthickness=0)
                canvas.create_rectangle(0, 0, CELL_SIDE - 1, CELL_SIDE - 1, outline="black", width=1)
                cell_list.append(canvas)

        # Desenhar os peões nas células
        for player in self.board.players_list:
            for index, count in enumerate(player.walk):
                if count > 0:
                    # Célula comum (0-51)
                    if 0 < index <= 51:
                        cell = white_cell_list[((index - 1) + 13 * player.order) % 52]
                    # Célula final (52+)
                    elif index > 51:
                        cell = colorful_cell_list[player.order][index - 52]
                    else:
                        continue

                    # Limpa o canvas antes de desenhar
                    cell.create_rectangle(0, 0, CELL_SIDE - 1, CELL_SIDE - 1, outline="black", width=1)

                    # Coordenadas base
                    center = CELL_SIDE // 2
                    offset = PAWN_RADIUS + 2

                    positions = []
                    if count == 1:
                        positions = [(center, center)]
                    elif count == 2:
                        positions = [
                            (center - offset, center - offset),
                            (center + offset, center + offset),
                        ]
                    elif count == 3:
                        positions = [
                            (center + offset, center - offset),
                            (center, center),
                            (center - offset, center + offset),
                        ]

                    else:  # 4 ou mais (mostra até 4 peões)
                        positions = [
                            (center - offset, center - offset),
                            (center + offset, center - offset),
                            (center - offset, center + offset),
                            (center + offset, center + offset),
                        ]

                    for i in range(min(int(count), 4)):
                        x, y = positions[i]
                        cell.create_oval(
                            x - PAWN_RADIUS, y - PAWN_RADIUS,
                            x + PAWN_RADIUS, y + PAWN_RADIUS,
                            fill=player.color,
                            outline="black",
                            width=PAWN_WIDTH
                        )

        # Posicionar as células do tabuleiro branco
        for i, cell in enumerate(white_cell_list):
            if i <= 4:
                cell.grid(row=6, column=1 + i)
            elif i <= 9:
                cell.grid(row=5 - (i - 5), column=6)
            elif i <= 12:
                cell.grid(row=0, column=5 + (13 - i))
            elif i <= 17:
                cell.grid(row=i - 12, column=8)
            elif i <= 22:
                cell.grid(row=6, column=9 + (i - 18))
            elif i <= 25:
                cell.grid(row=6 + (i - 23), column=14)
            elif i <= 30:
                cell.grid(row=8, column=14 - (i - 25))
            elif i <= 35:
                cell.grid(row=9 + (i - 31), column=8)
            elif i <= 38:
                cell.grid(row=14, column=8 - (i - 36))
            elif i <= 43:
                cell.grid(row=15 - (i - 37), column=6)
            elif i <= 48:
                cell.grid(row=8, column=5 - (i - 44))
            elif i <= 51:
                cell.grid(row=8 - (i - 49), column=0)

        # Posicionar as células coloridas (caminho final)
        for i in range(6):
            green_cell_list[i].grid(row=7, column=1 + i)
            yellow_cell_list[i].grid(row=1 + i, column=7)
            blue_cell_list[i].grid(row=7, column=13 - i)
            red_cell_list[i].grid(row=13 - i, column=7)

        # Células centrais (pretas)
        for row, col in [(6, 6), (8, 6), (6, 8), (8, 8), (7, 7)]:
            center_canvas = Canvas(self.boardFrame, bg="black", height=CELL_SIDE, width=CELL_SIDE, highlightthickness=0)
            center_canvas.create_rectangle(0, 0, CELL_SIDE - 1, CELL_SIDE - 1, outline="black", width=1)
            center_canvas.grid(row=row, column=col)

    def printar_estado(self):

        for widget in self.boardFrame.winfo_children():
            widget.destroy()

        for i in range(4):
            self.printar_quadrante(self.board.players_list[i].color, i, self.board.players_list[i].walk[0])

        self.printar_caminho()

        self.boardFrame.place(relx=1/17, rely=1/17)

    def start(self):
        self.board.play()
        self.printar_estado()

random_color = "#{:02x}{:02x}{:02x}".format(
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255)
)

players = [Player("green", "random"), Player("yellow", "random"), Player("blue", "random"), Player("red", "random")]

test_board = Board(players, "fixed")

app = Application(test_board)

app.printar_estado()

def atualizar():
    app.board.play()       
    app.printar_estado()     

botao = Button(root, text="Avançar", command=atualizar)
botao.pack()

root.mainloop()