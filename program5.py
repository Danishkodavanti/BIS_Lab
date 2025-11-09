import random

# Step 1: Define the Problem (Sphere function to minimize)
def fitness_function(x, y):
    return x**2 + y**2  # minimize this function

# Step 2: Initialize Parameters
num_wolves = 15        # population size
num_iterations = 100   # total iterations
lower_bound = -10
upper_bound = 10

# Step 3: Initialize Population (random wolf positions)
wolves = [[random.uniform(lower_bound, upper_bound),
           random.uniform(lower_bound, upper_bound)] for _ in range(num_wolves)]

# Step 4: Evaluate initial fitness
fitness = [fitness_function(w[0], w[1]) for w in wolves]

# Identify alpha, beta, and delta wolves (best three)
def sort_wolves(wolves, fitness):
    sorted_pairs = sorted(zip(wolves, fitness), key=lambda x: x[1])
    sorted_wolves = [w for w, f in sorted_pairs]
    sorted_fitness = [f for w, f in sorted_pairs]
    return sorted_wolves, sorted_fitness

# Step 6: Iterate
for iteration in range(num_iterations):
    # Sort wolves based on fitness
    wolves, fitness = sort_wolves(wolves, fitness)

    alpha = wolves[0]   # best
    beta = wolves[1]    # second best
    delta = wolves[2]   # third best

    a = 2 - 2 * (iteration / num_iterations)  # linearly decreases from 2 to 0

    new_wolves = []
    for i in range(num_wolves):
        X = wolves[i]

        # Calculate distances to alpha, beta, delta
        for_best = []
        for leader in [alpha, beta, delta]:
            r1 = random.random()
            r2 = random.random()
            A = 2 * a * r1 - a
            C = 2 * r2
            D = [abs(C * leader[j] - X[j]) for j in range(2)]
            for_best.append([leader[j] - A * D[j] for j in range(2)])

        # Update position (average of three leaders)
        new_pos = [(for_best[0][j] + for_best[1][j] + for_best[2][j]) / 3 for j in range(2)]

        # Keep within bounds
        new_pos[0] = max(min(new_pos[0], upper_bound), lower_bound)
        new_pos[1] = max(min(new_pos[1], upper_bound), lower_bound)
        new_wolves.append(new_pos)

    wolves = new_wolves
    fitness = [fitness_function(w[0], w[1]) for w in wolves]

    if iteration % 10 == 0 or iteration == num_iterations - 1:
        print(f"Iteration {iteration+1}/{num_iterations}, Best Fitness = {fitness[0]:.6f}")

# Step 7: Output Best Solution
wolves, fitness = sort_wolves(wolves, fitness)
print("\nOptimal Solution Found:")
print(f"Best Position = {wolves[0]}")
print(f"Best Fitness = {fitness[0]:.6f}")
