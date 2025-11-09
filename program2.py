import random
import math

# Step 1: Define the problem (Sphere function)
def fitness_function(x, y):
    return x**2 + y**2  # minimize this function

# Step 2: Initialize PSO parameters
num_particles = 30
num_iterations = 100
w = 0.7      # inertia weight
c1 = 1.5     # cognitive (particle) coefficient
c2 = 1.5     # social (swarm) coefficient

# Define search space boundaries
x_min, x_max = -10, 10
y_min, y_max = -10, 10

# Step 3: Initialize particles
particles = []
for i in range(num_particles):
    x = random.uniform(x_min, x_max)
    y = random.uniform(y_min, y_max)
    vx = random.uniform(-1, 1)
    vy = random.uniform(-1, 1)
    particles.append({
        'position': [x, y],
        'velocity': [vx, vy],
        'best_position': [x, y],
        'best_value': fitness_function(x, y)
    })

# Initialize global best
global_best_position = min(particles, key=lambda p: p['best_value'])['best_position']
global_best_value = fitness_function(global_best_position[0], global_best_position[1])

# Step 6: Iterate
for iteration in range(num_iterations):
    for particle in particles:
        x, y = particle['position']
        vx, vy = particle['velocity']

        # Step 4: Evaluate fitness
        fitness_val = fitness_function(x, y)

        # Step 5: Update personal best
        if fitness_val < particle['best_value']:
            particle['best_value'] = fitness_val
            particle['best_position'] = [x, y]

        # Update global best
        if fitness_val < global_best_value:
            global_best_value = fitness_val
            global_best_position = [x, y]

    # Update velocity and position for each particle
    for particle in particles:
        r1, r2 = random.random(), random.random()

        particle['velocity'][0] = (
            w * particle['velocity'][0]
            + c1 * r1 * (particle['best_position'][0] - particle['position'][0])
            + c2 * r2 * (global_best_position[0] - particle['position'][0])
        )

        particle['velocity'][1] = (
            w * particle['velocity'][1]
            + c1 * r1 * (particle['best_position'][1] - particle['position'][1])
            + c2 * r2 * (global_best_position[1] - particle['position'][1])
        )

        # Update position
        particle['position'][0] += particle['velocity'][0]
        particle['position'][1] += particle['velocity'][1]

        # Keep within bounds
        particle['position'][0] = max(min(particle['position'][0], x_max), x_min)
        particle['position'][1] = max(min(particle['position'][1], y_max), y_min)

    # Print progress
    if iteration % 10 == 0 or iteration == num_iterations - 1:
        print(f"Iteration {iteration+1}/{num_iterations}, Best Value = {global_best_value:.6f}")

# Step 7: Output final result
print("\nOptimal Solution Found:")
print(f"Best Position = {global_best_position}")
print(f"Best Value = {global_best_value:.6f}")
