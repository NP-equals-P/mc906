from ludo import *

random_color = "#{:02x}{:02x}{:02x}".format(
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255)
)

players1 = Player("green", "random")
players2 = Player("yellow", "random")
players3 = Player("blue", "random")
players4 = Player("red", "random")
players = [players1, players2, players3, players4]

test_board = Board(players)

winner = None

while (winner == None):
    winner = test_board.play()

print(players1.wins, players2.wins, players3.wins, players4.wins)
