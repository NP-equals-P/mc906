from tkinter import *

CELL_SIDE = 50

root = Tk()

class Application():
    def __init__(self):
        self.root = root
        self.tela()
        self.printar_estado_inicial()
        root.mainloop()
    
    def tela(self):
        self.root.title("Ludo")
        self.root.configure(background="darkgray")
        self.root.geometry("850x900")
        self.root.resizable(False, False)
        
    def printar_quadrante(cor, ordem):
        pass

    def printar_estado_inicial(self):

        self.printar_quadrante("red", 0)


        cellList = []

        boardFrame = Frame(self.root, height=CELL_SIDE*15, width=CELL_SIDE*15)

        for _ in range(15):
            for __ in range(15):
                cellList.append(Frame(boardFrame, background="white", height=CELL_SIDE, width=CELL_SIDE,highlightbackground="black", highlightthickness=1))

        for n, cell in enumerate(cellList):
            cell.grid(row=n//15, column=n%15)

        boardFrame.place(relx=1/17, rely=1/17)


Application()