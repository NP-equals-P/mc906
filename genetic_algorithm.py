from ludo import *
import random

class GeneticAlgorithm:
    def __init__(self, population_size, generations, mutation_rate, think_type):
        self.population_size = population_size + (population_size % 4)
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.think_type = think_type

    def initialize_population(self):
        self.population = [self.random_individual() for _ in range(self.population_size)]
        random.shuffle(self.population)
    
    def random_individual(self):
       
        random_color = "#{:02x}{:02x}{:02x}".format(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        random_player = Player(
            name = "",
            think_type = self.think_type
        )

        return random_player
    
    def simulate_games_1(self):

        for i in range(len(self.population) // 4):

            for k in range(10):
                players = self.population[i * 4:(i + 1) * 4]
                for j in range(4):
                    players[j].set_oponents(players[:j] + players[j + 1:])
                    players[j].set_cosmedics(j)

                board = Board(players)
                winner = None

                while winner is None:
                    winner = board.play()

                for player in players:
                    player.restart_walk()

gen = GeneticAlgorithm(32, 100, 0.1, "random")
gen.initialize_population()

gen.simulate_games_1()
for player in gen.population:
    print(f"Player Color: {player.color}, Wins: {player.wins}")