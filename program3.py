import random
import math

# Step 1: Define the Problem (Sphere function)
def fitness_function(x, y):
    return x**2 + y**2  # minimize this function

# Step 2: Initialize Parameters
num_nests = 15          # number of nests
num_iterations = 100    # total iterations
pa = 0.25               # discovery rate (abandonment probability)
lower_bound = -10
upper_bound = 10

# Step 3: Initialize Population (random nests)
nests = [[random.uniform(lower_bound, upper_bound),
          random.uniform(lower_bound, upper_bound)] for _ in range(num_nests)]

def levy_flight(Lambda):
    """Generate Lévy flight step"""
    sigma = (math.gamma(1 + Lambda) * math.sin(math.pi * Lambda / 2) /
             (math.gamma((1 + Lambda) / 2) * Lambda * 2 ** ((Lambda - 1) / 2))) ** (1 / Lambda)
    u = random.gauss(0, sigma)
    v = random.gauss(0, 1)
    step = u / (abs(v) ** (1 / Lambda))
    return step

# Evaluate fitness for all nests
fitness = [fitness_function(n[0], n[1]) for n in nests]

# Step 7: Iterate
for iteration in range(num_iterations):
    # Find the best nest
    best_index = fitness.index(min(fitness))
    best_nest = nests[best_index]

    # Generate new solutions using Lévy flights
    for i in range(num_nests):
        step = levy_flight(1.5)
        new_nest = [
            nests[i][0] + step * (nests[i][0] - best_nest[0]),
            nests[i][1] + step * (nests[i][1] - best_nest[1])
        ]
        # Keep within bounds
        new_nest[0] = max(min(new_nest[0], upper_bound), lower_bound)
        new_nest[1] = max(min(new_nest[1], upper_bound), lower_bound)

        new_fit = fitness_function(new_nest[0], new_nest[1])
        if new_fit < fitness[i]:
            nests[i] = new_nest
            fitness[i] = new_fit

    # Step 6: Abandon some nests
    for i in range(num_nests):
        if random.random() < pa:
            nests[i] = [random.uniform(lower_bound, upper_bound),
                        random.uniform(lower_bound, upper_bound)]
            fitness[i] = fitness_function(nests[i][0], nests[i][1])

    # Print progress every 10 iterations
    if iteration % 10 == 0 or iteration == num_iterations - 1:
        print(f"Iteration {iteration+1}/{num_iterations}, Best Fitness = {min(fitness):.6f}")

# Step 8: Output Best Solution
best_index = fitness.index(min(fitness))
print("\nOptimal Solution Found:")
print(f"Best Position = {nests[best_index]}")
print(f"Best Fitness = {fitness[best_index]:.6f}")
