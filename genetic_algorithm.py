from ludo import *
import random
import time

def evaluate_player(player, num_games=100):

    old_wins = player.wins
    player.wins = 0

    for _ in range(num_games):

        player.restart_walk()
        player.set_oponents([])

        players = [player, Player("", "random"), Player("", "random"), Player("", "random")]

        random.shuffle(players)

        evaluetion_board = Board(players)

        winner = None

        while winner is None:
            winner = evaluetion_board.play()

    num = player.wins / num_games

    player.wins = old_wins

    return num

class GeneticAlgorithm:
    def __init__(self, population_size, generations, mutation_rate, think_type, num_games, simulation_type, crossover_type=1, selection_type=1):
        self.population_size = population_size + (population_size % 4)
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.think_type = think_type
        self.num_games = num_games
        self.simulation_type = simulation_type
        self.crossover_type = crossover_type
        self.selection_type = selection_type

    def initialize_population(self):
        self.population = [self.random_individual() for _ in range(self.population_size)]
        random.shuffle(self.population)
    
    def random_individual(self):


        if (self.think_type == "arbitrary"):
            dna = np.random.randn(8)
        elif (self.think_type == "neural"):
            dna = (np.random.randn(233, 4), np.random.randn(4))
            
        random_player = Player(
            name = "",
            think_type = self.think_type
        )

        random_player.set_DNA(dna)

        return random_player
    
    def evaluate_fitness(self):
        total_wins = sum(player.wins for player in self.population)
        if total_wins == 0:
            for player in self.population:
                player.fitness = 1.0 / self.population_size
        else:
            for player in self.population:
                player.fitness = player.wins / total_wins

    def select_parents(self, num_parents):
        # print([p.wins for p in self.population])

        self.population.sort(key=lambda p: p.wins, reverse=True)
        if (self.selection_type == 1):

            elite = self.population[:num_parents // 4]
        
            # Roleta para o restante
            probabilities = [p.fitness for p in self.population]
            selected = list(np.random.choice(
                self.population, 
                size=(num_parents // 4)*3, 
                replace=True, 
                p=np.array(probabilities) / np.sum(probabilities)
            ))
        elif (self.selection_type == 2):
        
            elite = []

            probabilities = [p.fitness for p in self.population]
            selected = list(np.random.choice(
                self.population, 
                size=num_parents, 
                replace=True, 
                p=np.array(probabilities) / np.sum(probabilities)
            ))

        return elite + selected

    def crossover(self, parent1, parent2):
        if (self.crossover_type == 1):
            if (self.think_type == "arbitrary"):
                child_dna = (parent1.DNA + parent2.DNA) / 2
            elif (self.think_type == "neural"):
                child_dna = (
                    (parent1.DNA[0] + parent2.DNA[0]) / 2,
                    (parent1.DNA[1] + parent2.DNA[1]) / 2
                )
        else:
            if (self.think_type == "arbitrary"):
                # Crossover por máscara binária (como já estava)
                mask = np.random.randint(0, 2, size=parent1.DNA.shape)
                child_dna = np.where(mask, parent1.DNA, parent2.DNA)
            elif (self.think_type == "neural"):
                # Crossover por máscara binária para redes neurais
                mask1 = np.random.randint(0, 2, size=parent1.DNA[0].shape)
                mask2 = np.random.randint(0, 2, size=parent1.DNA[1].shape)
                child_dna = (
                    np.where(mask1, parent1.DNA[0], parent2.DNA[0]),
                    np.where(mask2, parent1.DNA[1], parent2.DNA[1])
                )

        return child_dna

    def mutate(self, dna):

        if (self.think_type == "arbitrary"):
            for i in range(len(dna)):
                if random.random() < self.mutation_rate:
                    dna[i] += np.random.normal(0, 0.05)
        elif (self.think_type == "neural"):
            for i in range(len(dna[0])):
                if random.random() < self.mutation_rate:
                    dna[0][i] += np.random.normal(0, 0.05)
            for i in range(len(dna[1])):
                if random.random() < self.mutation_rate:
                    dna[1][i] += np.random.normal(0, 0.05)

        return dna
    
    def evolve(self):
        for gen in range(self.generations):
            print(f"gen: {gen + 1}... ")

            # Simula jogos.
            self.simulate_games(self.simulation_type)
            
            # Avalia fitness.
            self.evaluate_fitness()
            
            self.population.sort(key=lambda p: p.wins, reverse=True)
            for player in self.population:
                print(f"{player.wins}", end=" ")
            
            print("Player evaluation:", (evaluate_player(self.population[0], 1000) + evaluate_player(self.population[1], 1000) + evaluate_player(self.population[2], 1000))/3)
            # print(self.population[0].DNA)

            # Seleciona pais
            parents = self.select_parents(self.population_size)
            
            # Gera nova população
            new_population = []
            for i in range(0, len(parents), 2):
                p1 = parents[i]
                p2 = parents[(i + 1) % len(parents)]

                parents_aux = [p1, p2]

                for m in range(2):  # dois filhos por par
                    child_dna = self.crossover(parents_aux[m], parents_aux[m - 1])
                    child_dna = self.mutate(child_dna)
                    child = Player(name="", think_type=self.think_type)
                    child.set_DNA(child_dna)
                    new_population.append(child)

            self.population = new_population[:self.population_size]

        self.population.sort(key=lambda p: p.wins, reverse=True)

    def simulate_games(self, mode=1):
        # Simula jogos entre os jogadores da população.
        # mode 1: Define os quartetos e cada quarteto joga "num_games" vezes.
        # mode 2: Embaralha a população "num_games" vezes, cada vez quartetos novos são definidos.

        if (mode == 1):
            for i in range(len(self.population) // 4):

                for k in range(self.num_games):

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
        else:
            for i in range(self.num_games):

                random.shuffle(self.population)

                for j in range(0, len(self.population), 4):
                    players = self.population[j:j + 4]
                    for k in range(4):
                        players[k].set_oponents(players[:k] + players[k + 1:])
                        players[k].set_cosmedics(k)

                    board = Board(players)
                    winner = None

                    while winner is None:
                        winner = board.play()

                    for player in players:
                        player.restart_walk()



# start_time = time.time()
# gen = GeneticAlgorithm(200, 1000, 0.05, "arbitrary", 100, 2, 1)
# gen.initialize_population()
# gen.evolve()
# end_time = time.time()
# print(f"Tempo de execução do evolve: {end_time - start_time:.2f} segundos")


# print("Player evaluation:", evaluate_player(gen.population[0], 1000))

gen = GeneticAlgorithm(100, 1000, 0.05, "neural", 100, 2, 1, 2)
gen.initialize_population()
gen.evolve()
