import random  # Used for randomness: picking bits to flip and seeding reproducibility
from dataclasses import dataclass  # Lightweight config container

# We wrap a bitstring into an actual playable strategy for the IPD engine
from src.strategies.lookup_table import LookupTableStrategy

# This computes "fitness" by playing the strategy vs an opponent pool
from src.game.evaluate import evaluate_strategy


def random_strategy(length: int) -> str:
    """Generate a random bitstring strategy of the requested length."""
    return ''.join(random.choice('01') for _ in range(length))


@dataclass
class HillConfig:
    # How many neighbor attempts we do (more = better chance to improve, slower runtime)
    iterations: int = 5000

    # How many rounds per match (same as the rest of your experiments)
    rounds: int = 200

    # Seed so results are repeatable (critical for a report)
    seed: int = 42

    # Optional: allow starting from a specific bitstring instead of random
    start_strategy: str | None = None


def _flip_one_bit(bitstring: str):
    """Return a neighbor strategy by flipping exactly one random bit."""
    i = random.randrange(len(bitstring))  # Pick a random position 0..63
    flipped = '1' if bitstring[i] == '0' else '0'  # Flip 0->1 or 1->0
    # Return the new bitstring with that one bit changed + the index we flipped (useful for debugging)
    return bitstring[:i] + flipped + bitstring[i + 1:], i


def run_hill_climb(opponent_pool, config: HillConfig):
    """
    Hill climbing (greedy local search):
      - Start with a strategy (random or provided).
      - Try small changes (neighbors) by flipping 1 bit.
      - If the change improves fitness, accept it.
      - Repeat for a fixed number of iterations.

    Returns:
      best_bitstring, best_fitness, history(list of dict snapshots)
    """
    random.seed(config.seed)  # Make random flips reproducible

    # Choose starting solution: either provided or a random 64-bit strategy
    current = config.start_strategy if config.start_strategy is not None else random_strategy(64)

    # Compute starting fitness (score) by playing against the entire opponent pool
    current_fit = evaluate_strategy(
        LookupTableStrategy(current, "HC_START"),  # Wrap bitstring into a playable Strategy object
        opponent_pool,                             # The fixed pool used to measure fitness
        rounds=config.rounds                       # Rounds per match
    )

    # Track best solution we have ever seen (not just "current")
    best = current
    best_fit = current_fit

    history = []          # We will store checkpoints for plotting (iteration, best fitness, etc.)
    improvements = 0      # How many times we accepted a better neighbor

    # Main search loop: try one random neighbor per iteration
    for it in range(config.iterations):
        # Create a neighbor by flipping one bit in the current bitstring
        neighbor, idx = _flip_one_bit(current)

        # Evaluate neighbor fitness the same way as all other strategies
        neighbor_fit = evaluate_strategy(
            LookupTableStrategy(neighbor, f"HC_{it}"),
            opponent_pool,
            rounds=config.rounds
        )

        # Greedy acceptance rule: only move if strictly better
        if neighbor_fit > current_fit:
            current, current_fit = neighbor, neighbor_fit  # Move “uphill” (improvement)
            improvements += 1                              # Count accepted improvements

            # Update global best if this is the best we’ve ever seen
            if current_fit > best_fit:
                best, best_fit = current, current_fit

        # Log every 100 iterations so plots aren’t huge (and runtime is reasonable)
        if (it + 1) % 100 == 0:
            history.append({
                "iteration": it + 1,            # 1-based iteration count for readability
                "current_fitness": current_fit, # Fitness of the current accepted strategy
                "best_fitness": best_fit,       # Best fitness seen so far
                "improvements": improvements    # Count of accepted improvements so far
            })

    # Return the best strategy found, its fitness, and history for plotting/reporting
    return best, best_fit, history