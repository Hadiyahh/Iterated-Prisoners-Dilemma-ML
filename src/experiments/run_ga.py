# Runs the GA experiment and writes summary/history outputs to CSV files.

import csv  # CSV writer for saving experiment outputs.
from pathlib import Path  # Cross-platform path handling.

# Builds the pool of opponents the GA-evolved strategy is evaluated against.
from src.experiments.opponent_pool import get_opponent_pool
# GA runner + configuration dataclass.
from src.optim.genetic_algorithm import run_ga, GAConfig


# Save final best GA result (one row) to CSV.
def save_best(best_bitstring: str, best_fitness: float, cfg: GAConfig, out_path: Path):
    # Ensure output directory exists before writing.
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Open CSV in text mode with UTF-8.
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        # Header columns for reproducibility and reporting.
        w.writerow([
            "method", "population_size", "generations", "crossover_rate", "mutation_rate",
            "elite_size", "rounds", "seed", "best_fitness", "best_bitstring"
        ])

        # One summary row for this run.
        w.writerow([
            "GA",
            cfg.population_size,
            cfg.generations,
            cfg.crossover_rate,
            cfg.mutation_rate,
            cfg.elite_size,
            cfg.rounds,
            cfg.seed,
            best_fitness,
            best_bitstring
        ])


# Save per-generation fitness history to CSV.
def save_history(history, out_path: Path):
    # Ensure output directory exists before writing.
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        # History columns.
        w.writerow(["generation", "best_fitness", "avg_fitness"])

        # Write one row per generation.
        for row in history:
            w.writerow([row["generation"], row["best_fitness"], row["avg_fitness"]])


# Main GA experiment flow.
def main():
    # Build opponent pool (fixed seed for reproducibility).
    pool = get_opponent_pool(seed=42, num_random=10)

    # Configure GA hyperparameters.
    cfg = GAConfig(population_size=80, generations=200, mutation_rate=0.001, seed=42)

    # Run optimization.
    best, best_fit, history = run_ga(pool, cfg)

    # Console summary.
    print("BEST FITNESS:", best_fit)
    print("BEST BITSTRING:", best)

    # Save outputs if GA returned a valid best solution.
    if best is not None:
        results_dir = Path("results") / "tables"
        save_best(best, best_fit, cfg, results_dir / "ga_best.csv")
        save_history(history, results_dir / "ga_fitness_history.csv")


# Script entry point.
if __name__ == "__main__":
    main()