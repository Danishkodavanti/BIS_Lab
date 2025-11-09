import math
import random

# Step 1: Define the Problem — Cities with coordinates
cities = {
    0: (0, 0),
    1: (1, 5),
    2: (5, 2),
    3: (6, 6),
    4: (8, 3)
}

num_cities = len(cities)

# Function to calculate Euclidean distance between two cities
def distance(city1, city2):
    x1, y1 = cities[city1]
    x2, y2 = cities[city2]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Step 2: Initialize Parameters
num_ants = 10
num_iterations = 100
alpha = 1.0     # pheromone importance
beta = 5.0      # distance importance
rho = 0.5       # pheromone evaporation rate
Q = 100         # total pheromone per ant
pheromone_init = 1.0

# Initialize pheromone matrix
pheromone = [[pheromone_init for _ in range(num_cities)] for _ in range(num_cities)]

# Precompute distances
distances = [[distance(i, j) if i != j else float('inf') for j in range(num_cities)] for i in range(num_cities)]

# Helper function to calculate tour length
def tour_length(tour):
    return sum(distances[tour[i]][tour[(i + 1) % num_cities]] for i in range(num_cities))

# Step 5: Iterate
best_tour = None
best_length = float('inf')

for iteration in range(num_iterations):
    all_tours = []

    # Step 3: Construct Solutions
    for ant in range(num_ants):
        unvisited = list(range(num_cities))
        start_city = random.choice(unvisited)
        tour = [start_city]
        unvisited.remove(start_city)

        current_city = start_city
        while unvisited:
            probabilities = []
            for next_city in unvisited:
                tau = pheromone[current_city][next_city] ** alpha
                eta = (1 / distances[current_city][next_city]) ** beta
                probabilities.append(tau * eta)
            total = sum(probabilities)
            probabilities = [p / total for p in probabilities]

            next_city = random.choices(unvisited, weights=probabilities)[0]
            tour.append(next_city)
            unvisited.remove(next_city)
            current_city = next_city

        all_tours.append(tour)

    # Step 4: Update Pheromones
    # Evaporation
    for i in range(num_cities):
        for j in range(num_cities):
            pheromone[i][j] *= (1 - rho)

    # Deposit new pheromone
    for tour in all_tours:
        length = tour_length(tour)
        for i in range(num_cities):
            a, b = tour[i], tour[(i + 1) % num_cities]
            pheromone[a][b] += Q / length
            pheromone[b][a] += Q / length

        # Update best tour
        if length < best_length:
            best_length = length
            best_tour = tour

    if iteration % 10 == 0 or iteration == num_iterations - 1:
        print(f"Iteration {iteration + 1}/{num_iterations}, Best Length = {best_length:.4f}")

# Step 6: Output the Best Solution
print("\nOptimal Tour Found:")
print(" → ".join(map(str, best_tour)) + f" → {best_tour[0]}")
print(f"Tour Length = {best_length:.4f}")
