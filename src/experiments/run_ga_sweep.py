import csv  # Save experiment results to tables
from pathlib import Path  # Safe file handling

# Fixed opponent pool = fair evaluation across GA parameter runs
from src.experiments.opponent_pool import get_opponent_pool

# Your GA implementation + config dataclass
from src.optim.genetic_algorithm import run_ga, GAConfig


def main():
    # Build the opponent pool ONCE with fixed settings, so all runs compare fairly
    pool = get_opponent_pool(seed=42, num_random=10)

    # The key parameter we want to compare: mutation rate
    # (This directly affects exploration vs stability in GA)
    mutation_rates = [0.0005, 0.001, 0.005]

    # Make sure results/tables exists
    out_dir = Path("results") / "tables"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Summary CSV path that contains 1 row per GA run
    summary_path = out_dir / "ga_runs_summary.csv"

    # Open the summary file for writing
    with summary_path.open("w", newline="", encoding="utf-8") as fsum:
        summary_writer = csv.writer(fsum)

        # Header row describing the columns
        summary_writer.writerow([
            "run_id",                 # 1, 2, 3...
            "population_size",        # GA population
            "generations",            # number of generations evolved
            "crossover_rate",         # probability of crossover
            "mutation_rate",          # the parameter we’re sweeping
            "elite_size",             # number of top strategies kept unchanged
            "rounds",                 # rounds per match
            "seed",                   # random seed
            "best_fitness",           # best fitness across the entire run
            "best_bitstring",         # the best chromosome
            "final_avg_fitness",      # avg fitness at last generation
            "final_best_fitness"      # best fitness at last generation
        ])

        # Iterate through each mutation rate and run GA once
        for run_id, mr in enumerate(mutation_rates, start=1):
            # Create a GA config for this run
            cfg = GAConfig(
                population_size=80,   # decent default
                generations=200,      # matches your earlier run
                mutation_rate=mr,     # this is the sweep variable
                crossover_rate=0.8,   # typical value
                elite_size=2,         # keep top 2 unchanged to prevent regression
                rounds=200,           # consistent with other experiments
                seed=42               # keep constant so only mutation changes
            )

            # Run GA and get:
            # - best chromosome (bitstring)
            # - best fitness
            # - per-generation history (best and average fitness)
            best, best_fit, history = run_ga(pool, cfg)

            # Save per-run history so Person C can plot convergence curves
            hist_path = out_dir / f"ga_fitness_history_run{run_id}.csv"
            with hist_path.open("w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh)

                # Header for the time series
                w.writerow(["generation", "best_fitness", "avg_fitness"])

                # Write each generation’s stats
                for row in history:
                    w.writerow([row["generation"], row["best_fitness"], row["avg_fitness"]])

            # Pull final-generation stats (last element of history list)
            final_best = history[-1]["best_fitness"]
            final_avg = history[-1]["avg_fitness"]

            # Write one summary row for this run to ga_runs_summary.csv
            summary_writer.writerow([
                run_id,
                cfg.population_size,
                cfg.generations,
                cfg.crossover_rate,
                cfg.mutation_rate,
                cfg.elite_size,
                cfg.rounds,
                cfg.seed,
                best_fit,
                best,
                final_avg,
                final_best
            ])

            # Print progress so you know it worked
            print(f"[Run {run_id}] mutation_rate={mr} | best_fit={best_fit:.3f} | saved {hist_path}")

    # Confirm summary output location
    print(f"\nSaved GA sweep summary to: {summary_path}")


# Standard entrypoint guard
if __name__ == "__main__":
    main()