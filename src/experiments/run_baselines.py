# from src.strategies.baselines import ALLC, ALLD, RAND, TFT, TF2T, STFT  # Import baseline strategies.
# from src.game.engine import play_tournament  # Tournament runner for round-robin play.

# def main():  # Main baseline experiment.
#     strategies = [  # List of baseline strategy instances.
#         ALLC("ALLC"),
#         ALLD("ALLD"),
#         RAND("RAND"),
#         TFT("TFT"),
#         TF2T("TF2T"),
#         STFT("STFT")
#     ]

#     results = play_tournament(strategies, rounds=200)  # Run tournament for 200 rounds per matchup.

#     print("Tournament Results:")  # Header for console output.
#     for name, score in results.items():  # Iterate through result scores.
#         print(f"{name}: {score}")  # Print each strategy's score.

# if __name__ == "__main__":  # Script entry point guard.
#     main()  # Execute the baseline tournament.
import csv
import argparse
import random
import statistics
from pathlib import Path
from src.strategies.baselines import ALLC, ALLD, RAND, TFT, TF2T, STFT
from src.game.engine import play_tournament

N_RUNS = 100
SEED_START = 0
ROUNDS = 200


def build_strategies():
    return [
        ALLC("ALLC"),
        ALLD("ALLD"),
        RAND("RAND"),
        TFT("TFT"),
        TF2T("TF2T"),
        STFT("STFT")
    ]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run baseline IPD tournament with multi-seed summary."
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=N_RUNS,
        help="Number of tournament runs with different seeds (default: 100)."
    )
    parser.add_argument(
        "--seed-start",
        type=int,
        default=SEED_START,
        help="Starting seed; run i uses seed_start + i (default: 0)."
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=ROUNDS,
        help="Rounds per head-to-head match (default: 200)."
    )
    return parser.parse_args()


def main(runs=N_RUNS, seed_start=SEED_START, rounds=ROUNDS):
    if runs < 1:
        raise ValueError("--runs must be >= 1")
    if rounds < 1:
        raise ValueError("--rounds must be >= 1")

    all_results = []
    for run_idx in range(runs):
        random.seed(seed_start + run_idx)
        results = play_tournament(build_strategies(), rounds=rounds)
        all_results.append(results)

    first_run_results = all_results[0]

    print(f"Tournament Results (run 1 of {runs}, rounds={rounds}):")
    for name, score in first_run_results.items():
        print(f"{name}: {score}")

    strategy_names = list(first_run_results.keys())
    summary_rows = []
    for name in strategy_names:
        scores = [run[name] for run in all_results]
        summary_rows.append({
            "strategy": name,
            "mean_score": statistics.mean(scores),
            "std_score": statistics.pstdev(scores)
        })

    summary_rows.sort(key=lambda row: row["mean_score"], reverse=True)

    print(f"\nTournament Summary ({runs} runs, rounds={rounds}):")
    for row in summary_rows:
        print(
            f"{row['strategy']}: mean={row['mean_score']:.2f}, "
            f"std={row['std_score']:.2f}"
        )

    # SAVE CSV
    out = Path("results/tables/baselines_tournament.csv")
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["strategy", "score"])
        for name, score in first_run_results.items():
            writer.writerow([name, score])

    print("Saved baselines_tournament.csv")

    summary_out = Path("results/tables/baselines_tournament_summary.csv")
    with summary_out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["strategy", "mean_score", "std_score"])
        for row in summary_rows:
            writer.writerow([
                row["strategy"],
                f"{row['mean_score']:.2f}",
                f"{row['std_score']:.2f}"
            ])

    print("Saved baselines_tournament_summary.csv")

if __name__ == "__main__":
    args = parse_args()
    main(runs=args.runs, seed_start=args.seed_start, rounds=args.rounds)