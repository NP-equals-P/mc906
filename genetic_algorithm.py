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

        dna = np.random.randn(6)

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
        self.population.sort(key=lambda p: p.wins, reverse=True)
        elite = self.population[:num_parents // 2]
    
        # Roleta para o restante
        probabilities = [p.fitness for p in self.population]
        selected = list(np.random.choice(
            self.population, 
            size=num_parents // 2, 
            replace=False, 
            p=np.array(probabilities) / np.sum(probabilities)
        ))
        
        return elite + selected


    def crossover(self, parent1, parent2):
        mask = np.random.randint(0, 2, size=parent1.DNA.shape)
        child_dna = np.where(mask, parent1.DNA, parent2.DNA)
        return child_dna


    def mutate(self, dna):
        for i in range(len(dna)):
            if random.random() < self.mutation_rate:
                dna[i] += np.random.normal(0, 0.5)
        return dna
    
    def evolve(self):
        for gen in range(self.generations):
            print(f"Geração {gen + 1}")

            # Simula jogos
            self.simulate_games_1()
            
            # Avalia fitness
            self.evaluate_fitness()
            

            self.population.sort(key=lambda p: p.wins, reverse=True)
            for player in self.population[:4]:
                print(f"Player DNA: {player.DNA}, Wins: {player.wins}")
            
            # Seleciona pais
            parents = self.select_parents(self.population_size)
            
            # Gera nova população
            new_population = []
            for i in range(0, len(parents), 2):
                p1 = parents[i]
                p2 = parents[(i + 1) % len(parents)]
                for _ in range(2):  # dois filhos por par
                    child_dna = self.crossover(p1, p2)
                    child_dna = self.mutate(child_dna)
                    child = Player(name="", think_type=self.think_type)
                    child.set_DNA(child_dna)
                    new_population.append(child)

            self.population = new_population[:self.population_size]


            # Reset wins
            for player in self.population:
                player.wins = 0


    
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

gen = GeneticAlgorithm(32, 100, 0.1, "arbitrary")
gen.initialize_population()
gen.evolve()
