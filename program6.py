import random
import math

# Step 1: Define the Problem (Sphere function)
def fitness_function(x, y):
    # We minimize f(x, y) = x^2 + y^2
    return x**2 + y**2

# Step 2: Initialize Parameters
grid_size = 5             # 5x5 grid of cells
num_iterations = 50       # total iterations
lower_bound = -10
upper_bound = 10

# Step 3: Initialize Population (each cell = one solution)
cells = [[(random.uniform(lower_bound, upper_bound),
           random.uniform(lower_bound, upper_bound)) for _ in range(grid_size)] for _ in range(grid_size)]

# Evaluate fitness
def get_fitness_grid(cells):
    return [[fitness_function(x, y) for (x, y) in row] for row in cells]

# Get neighbors (with wrap-around / toroidal boundary)
def get_neighbors(i, j, grid_size):
    neighbors = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni = (i + di) % grid_size
            nj = (j + dj) % grid_size
            neighbors.append((ni, nj))
    return neighbors

# Step 6: Iterate
for iteration in range(num_iterations):
    fitness_grid = get_fitness_grid(cells)

    new_cells = [[None for _ in range(grid_size)] for _ in range(grid_size)]

    for i in range(grid_size):
        for j in range(grid_size):
            neighbors = get_neighbors(i, j, grid_size)
            best_neighbor = cells[i][j]
            best_fit = fitness_grid[i][j]

            # Rule: adopt position of the best neighbor (local imitation)
            for ni, nj in neighbors:
                if fitness_grid[ni][nj] < best_fit:
                    best_fit = fitness_grid[ni][nj]
                    best_neighbor = cells[ni][nj]

            # Small random mutation to encourage exploration
            x, y = best_neighbor
            x += random.uniform(-0.1, 0.1)
            y += random.uniform(-0.1, 0.1)

            # Keep within bounds
            x = max(min(x, upper_bound), lower_bound)
            y = max(min(y, upper_bound), lower_bound)

            new_cells[i][j] = (x, y)

    cells = new_cells

    # Find best fitness overall
    all_fitness = [fitness_grid[i][j] for i in range(grid_size) for j in range(grid_size)]
    best_fitness = min(all_fitness)
    if iteration % 10 == 0 or iteration == num_iterations - 1:
        print(f"Iteration {iteration+1}/{num_iterations}, Best Fitness = {best_fitness:.6f}")

# Step 7: Output Best Solution
fitness_grid = get_fitness_grid(cells)
best_val = float("inf")
best_pos = None
for i in range(grid_size):
    for j in range(grid_size):
        if fitness_grid[i][j] < best_val:
            best_val = fitness_grid[i][j]
            best_pos = cells[i][j]

print("\nOptimal Solution Found:")
print(f"Best Position = {best_pos}")
print(f"Best Fitness = {best_val:.6f}")
