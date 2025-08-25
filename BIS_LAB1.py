import numpy as np
import random

# -----------------------------
# Step 1: Simulated Stock Prices
# -----------------------------
np.random.seed(42)
prices = np.cumsum(np.random.randn(100) + 0.5) + 100  # 100 days of prices

# -----------------------------
# Step 2: GA Setup
# -----------------------------
POP_SIZE = 20
GENS = 50
MUT_RATE = 0.1

# Each chromosome = [buy_threshold, sell_threshold]
# Thresholds are based on price % change

def create_individual():
    return [random.uniform(-2, 2), random.uniform(-2, 2)]

def evaluate(ind):
    buy_t, sell_t = ind
    cash, stock = 1000, 0  # Start with $1000

    for i in range(1, len(prices)):
        change = (prices[i] - prices[i-1]) / prices[i-1] * 100

        # Buy Rule
        if change <= buy_t and cash >= prices[i]:
            stock += cash // prices[i]
            cash -= stock * prices[i]

        # Sell Rule
        elif change >= sell_t and stock > 0:
            cash += stock * prices[i]
            stock = 0

    return cash + stock * prices[-1]  # Final value

# -----------------------------
# Step 3: GA Operators
# -----------------------------
def selection(pop):
    return sorted(pop, key=lambda x: evaluate(x), reverse=True)[:POP_SIZE//2]

def crossover(p1, p2):
    return [(p1[0], p2[1]), (p2[0], p1[1])]

def mutate(ind):
    if random.random() < MUT_RATE:
        ind[0] += random.uniform(-0.5, 0.5)
    if random.random() < MUT_RATE:
        ind[1] += random.uniform(-0.5, 0.5)
    return ind

# -----------------------------
# Step 4: Run GA
# -----------------------------
population = [create_individual() for _ in range(POP_SIZE)]

for gen in range(GENS):
    selected = selection(population)
    offspring = []
    for i in range(0, len(selected), 2):
        if i+1 < len(selected):
            offspring.extend(crossover(selected[i], selected[i+1]))
    offspring = [mutate(list(child)) for child in offspring]
    population = selected + offspring

best = max(population, key=lambda x: evaluate(x))
print("Best Strategy (Buy%, Sell%):", best)
print("Final Portfolio Value:", evaluate(best))
