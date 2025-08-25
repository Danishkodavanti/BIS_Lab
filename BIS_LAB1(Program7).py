import random
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# 1. Define the Problem
def evaluate_svm(params, X_train, y_train):
    C, gamma, kernel = params
    svm = SVC(C=C, gamma=gamma, kernel=kernel)
    scores = cross_val_score(svm, X_train, y_train, cv=5)
    return scores.mean()

# 2. Initialize Parameters
def init_population(pop_size):
    population = []
    kernels = ['linear', 'poly', 'rbf', 'sigmoid']
    for _ in range(pop_size):
        C = random.uniform(0.1, 10)
        gamma = random.uniform(0.001, 1)
        kernel = random.choice(kernels)
        population.append((C, gamma, kernel))
    return population

# 3. Evaluate Fitness
def evaluate_population(population, X_train, y_train):
    fitness_scores = []
    for individual in population:
        fitness = evaluate_svm(individual, X_train, y_train)
        fitness_scores.append(fitness)
    return fitness_scores

# 4. Selection (Tournament or Roulette Wheel)
def select(population, fitness_scores):
    selected = []
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    for _ in range(len(population)//2):  # Half the population for mating
        selected.append(random.choices(population, probabilities)[0])
    return selected

# 5. Crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(0, 2)
    if crossover_point == 0:
        child1 = (parent1[0], parent2[1], parent2[2])
        child2 = (parent2[0], parent1[1], parent1[2])
    elif crossover_point == 1:
        child1 = (parent2[0], parent1[1], parent2[2])
        child2 = (parent1[0], parent2[1], parent1[2])
    else:
        child1 = (parent1[0], parent1[1], parent2[2])
        child2 = (parent2[0], parent2[1], parent1[2])
    return child1, child2

# 6. Mutation
def mutate(individual):
    mutation_point = random.randint(0, 2)
    if mutation_point == 0:
        individual = (random.uniform(0.1, 10), individual[1], individual[2])
    elif mutation_point == 1:
        individual = (individual[0], random.uniform(0.001, 1), individual[2])
    else:
        individual = (individual[0], individual[1], random.choice(['linear', 'poly', 'rbf', 'sigmoid']))
    return individual

# 7. Main Genetic Algorithm loop
def gene_expression_algorithm(X_train, y_train, generations=100, population_size=50, mutation_rate=0.1, crossover_rate=0.7):
    population = init_population(population_size)
    best_solution = None
    best_fitness = -float('inf')

    for gen in range(generations):
        fitness_scores = evaluate_population(population, X_train, y_train)
        print(f"Generation {gen}: Best Fitness = {max(fitness_scores)}")

        if max(fitness_scores) > best_fitness:
            best_fitness = max(fitness_scores)
            best_solution = population[fitness_scores.index(best_fitness)]

        selected = select(population, fitness_scores)
        offspring = []

        for i in range(0, len(selected), 2):
            if random.random() < crossover_rate:
                child1, child2 = crossover(selected[i], selected[i+1])
                offspring.extend([child1, child2])
            else:
                offspring.extend([selected[i], selected[i+1]])

        # Mutate the offspring
        population = [mutate(ind) if random.random() < mutation_rate else ind for ind in offspring]
    
    return best_solution

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Run the genetic algorithm
best_params = gene_expression_algorithm(X_train, y_train)
print(f"Best parameters found: C={best_params[0]}, gamma={best_params[1]}, kernel={best_params[2]}")
