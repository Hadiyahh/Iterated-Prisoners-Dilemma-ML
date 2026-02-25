# Genetic Algorithm for evolving 64-bit lookup-table IPD strategies.

import random  # Provides randomness for initialization and genetic operators.
from dataclasses import dataclass  # Provides the @dataclass decorator.

from src.strategies.lookup_table import LookupTableStrategy  # Wraps bitstrings as strategies.
from src.game.evaluate import evaluate_strategy  # Computes fitness vs opponent pool.


def random_strategy(length: int) -> str:  # Function signature for random chromosome creation.
    return ''.join(random.choice('01') for _ in range(length))  # Build a bitstring of 0/1.


@dataclass  # Turns the class into a simple data container.
class GAConfig:  # Holds GA hyperparameters.
    population_size: int = 100  # Number of individuals per generation.
    generations: int = 300  # Number of evolutionary iterations.
    crossover_rate: float = 0.8  # Probability of crossover between parents.
    mutation_rate: float = 0.001  # Probability of mutating each bit.
    elite_size: int = 2  # How many top individuals to copy unchanged.
    rounds: int = 200  # Rounds per match for fitness evaluation.
    seed: int = 42  # Random seed for reproducibility.


def _tournament_select(population, fitnesses, k=3):  # Selects one parent by tournament.
    contenders = random.sample(range(len(population)), k)  # Pick k random indices.
    best_idx = max(contenders, key=lambda i: fitnesses[i])  # Choose index with best fitness.
    return population[best_idx]  # Return selected parent chromosome.


def _single_point_crossover(p1: str, p2: str):  # Recombine two parents into two children.
    if len(p1) != len(p2):  # Validate equal lengths.
        raise ValueError("Parents must have same length")  # Enforce same-length chromosomes.
    if len(p1) < 2:  # Cannot split a length-1 chromosome.
        return p1, p2  # Return parents unchanged.
    point = random.randint(1, len(p1) - 1)  # Choose a split point.
    c1 = p1[:point] + p2[point:]  # Child 1: left from p1, right from p2.
    c2 = p2[:point] + p1[point:]  # Child 2: left from p2, right from p1.
    return c1, c2  # Return both children.


def _mutate(bitstring: str, mutation_rate: float):  # Bit-flip mutation operator.
    bits = list(bitstring)  # Convert string to mutable list of chars.
    for i in range(len(bits)):  # Iterate over each bit position.
        if random.random() < mutation_rate:  # Flip with given probability.
            bits[i] = '1' if bits[i] == '0' else '0'  # Toggle 0 <-> 1.
    return ''.join(bits)  # Convert back to string.


def run_ga(opponent_pool, config: GAConfig):  # Main GA training loop.
    random.seed(config.seed)  # Set seed for reproducibility.

    population = [random_strategy(64) for _ in range(config.population_size)]  # Init population.

    history = []  # Track fitness stats per generation.
    best_overall = None  # Best chromosome seen so far.
    best_overall_fit = float("-inf")  # Best fitness seen so far.

    for gen in range(config.generations):  # Loop over generations.
        fitnesses = []  # Fitness values for the current population.
        for i, chrom in enumerate(population):  # Evaluate each chromosome.
            strat = LookupTableStrategy(chrom, name=f"GA_{gen}_{i}")  # Wrap as strategy.
            fit = evaluate_strategy(strat, opponent_pool, rounds=config.rounds)  # Compute fitness.
            fitnesses.append(fit)  # Store fitness.

        gen_best_fit = max(fitnesses)  # Best fitness in this generation.
        gen_avg_fit = sum(fitnesses) / len(fitnesses)  # Average fitness this generation.
        gen_best_idx = max(range(len(population)), key=lambda i: fitnesses[i])  # Best index.
        gen_best = population[gen_best_idx]  # Best chromosome.

        if gen_best_fit > best_overall_fit:  # Update global best if improved.
            best_overall_fit = gen_best_fit  # Store best fitness.
            best_overall = gen_best  # Store best chromosome.

        history.append({  # Save history row for later reporting.
            "generation": gen,  # Generation index.
            "best_fitness": gen_best_fit,  # Best fitness for this generation.
            "avg_fitness": gen_avg_fit,  # Average fitness for this generation.
        })

        elite_indices = sorted(  # Rank indices by fitness descending.
            range(len(population)),
            key=lambda i: fitnesses[i],
            reverse=True
        )[:config.elite_size]  # Take top N as elites.
        new_population = [population[i] for i in elite_indices]  # Carry elites forward.

        while len(new_population) < config.population_size:  # Fill the rest of population.
            parent1 = _tournament_select(population, fitnesses, k=3)  # Pick parent 1.
            parent2 = _tournament_select(population, fitnesses, k=3)  # Pick parent 2.

            if random.random() < config.crossover_rate:  # Decide crossover.
                child1, child2 = _single_point_crossover(parent1, parent2)  # Recombine.
            else:
                child1, child2 = parent1, parent2  # No crossover; copy parents.

            child1 = _mutate(child1, config.mutation_rate)  # Mutate child 1.
            child2 = _mutate(child2, config.mutation_rate)  # Mutate child 2.

            new_population.append(child1)  # Add child 1.
            if len(new_population) < config.population_size:  # Check capacity.
                new_population.append(child2)  # Add child 2 if space remains.

        population = new_population  # Replace old population with new.

        if (gen + 1) % 25 == 0:  # Periodic progress logging.
            print(f"Gen {gen+1}/{config.generations} | best={gen_best_fit:.3f} avg={gen_avg_fit:.3f}")  # Log.

    return best_overall, best_overall_fit, history  # Return best and stats.