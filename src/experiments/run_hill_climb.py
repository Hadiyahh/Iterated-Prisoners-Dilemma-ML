import csv  # For saving clean tables for Person C / report
from pathlib import Path  # OS-safe file paths (Windows-friendly)

# Builds the consistent opponent pool (must be fixed across experiments)
from src.experiments.opponent_pool import get_opponent_pool

# Hill climbing algorithm + config dataclass
from src.optim.hill_climb import run_hill_climb, HillConfig


def save_best(best_bitstring: str, best_fitness: float, cfg: HillConfig, out_path: Path):
    # Ensure output directory exists (creates results/tables if missing)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Open file for writing CSV
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)  # CSV writer object

        # Header row describing what’s in the file
        w.writerow(["method", "iterations", "rounds", "seed", "best_fitness", "best_bitstring"])

        # One row containing the best hill-climbing result + its settings
        w.writerow(["HILL", cfg.iterations, cfg.rounds, cfg.seed, best_fitness, best_bitstring])


def save_history(history, out_path: Path):
    # Ensure output directory exists
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Open file for writing
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        # Header for time-series history (good for plotting)
        w.writerow(["iteration", "current_fitness", "best_fitness", "improvements"])

        # Write each checkpoint
        for row in history:
            w.writerow([row["iteration"], row["current_fitness"], row["best_fitness"], row["improvements"]])


def main():
    # Create opponent pool with a fixed seed so every run is comparable
    pool = get_opponent_pool(seed=42, num_random=10)

    # Hill climbing settings (iterations affects runtime + quality)
    cfg = HillConfig(iterations=5000, rounds=200, seed=42)

    # Run hill climbing search
    best, best_fit, history = run_hill_climb(pool, cfg)

    # Print best result so you see it immediately
    print("HILL BEST FITNESS:", best_fit)
    print("HILL BEST BITSTRING:", best)

    # Define output directory results/tables
    out_dir = Path("results") / "tables"

    # Save summary of best strategy
    save_best(best, best_fit, cfg, out_dir / "hill_best.csv")

    # Save history checkpoints (for convergence plot)
    save_history(history, out_dir / "hill_history.csv")

    # Confirm outputs on console
    print(f"Saved: {out_dir / 'hill_best.csv'}")
    print(f"Saved: {out_dir / 'hill_history.csv'}")


# Standard Python entrypoint guard (so importing this file doesn’t auto-run it)
if __name__ == "__main__":
    main()