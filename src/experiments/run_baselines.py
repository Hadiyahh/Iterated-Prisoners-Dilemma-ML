import csv
import argparse
import random
import statistics
from pathlib import Path
from src.strategies.baselines import ALLC, ALLD, RAND, TFT, TF2T, STFT
from src.game.engine import play_tournament

def main(runs=1, seed_start=0, rounds=200):
    # --- 1. SET UP THE BASELINE STRATEGIES ---
    strategies = [
        ALLC("ALLC"),
        ALLD("ALLD"),
        RAND("RAND"),
        TFT("TFT"),
        TF2T("TF2T"),
        STFT("STFT")
    ]

    # --- 2. RUN STANDARD TOURNAMENT ---
    print("\n" + "="*30)
    print("RUNNING STANDARD TOURNAMENT")
    print("="*30)
    
    all_runs = []
    for run in range(runs):
        standard_results = play_tournament(strategies, rounds=rounds)
        all_runs.append(standard_results)
        
        # Save and Print Standard results
        with open(f"baselines_standard_run{run}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Strategy", "Score"])
            for name in standard_results:
                score = standard_results[name]
                print(f"{name}: {score}") # Print to terminal
                writer.writerow([name, score])

    # --- 3. RUN STRESS TEST (Adding 3 more ALLD) ---
    print("\n" + "="*30)
    print("RUNNING STRESS TEST (+3 ALLD)")
    print("="*30)
    
    stress_strategies = strategies + [ALLD("ALLD_2"), ALLD("ALLD_3"), ALLD("ALLD_4")]
    stress_results = play_tournament(stress_strategies, rounds=rounds)

    # Save and Print Stress Test results
    with open("baselines_stress_test.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Strategy", "Score"])
        for name in stress_results:
            score = stress_results[name]
            print(f"{name}: {score}") # Print to terminal
            writer.writerow([name, score])

    print("\n" + "-"*30)
    print("Done! CSV files generated successfully.")
    print("-"*30)

    # Calculate summary statistics
    summary_rows = []
    strategy_names = list(strategies[0].__class__.__dict__.keys()) if all_runs else []
    
    for strategy in strategies:
        scores = [run[strategy.name] for run in all_runs]
        mean_score = statistics.mean(scores) if scores else 0
        std_score = statistics.stdev(scores) if len(scores) > 1 else 0
        summary_rows.append({
            "strategy": strategy.name,
            "mean_score": mean_score,
            "std_score": std_score
        })

    summary_out = Path("results/tables/baselines_tournament_summary.csv")
    summary_out.parent.mkdir(parents=True, exist_ok=True)
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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--seed-start", "--seed_start", dest="seed_start", type=int, default=0)
    parser.add_argument("--rounds", type=int, default=200)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(runs=args.runs, seed_start=args.seed_start, rounds=args.rounds)