import csv  # CSV output for saving matchup results.
from pathlib import Path  # Path handling for output files.

from src.strategies.lookup_table import LookupTableStrategy  # Wraps GA bitstring into a strategy.
from src.strategies.baselines import TFT, TF2T, ALLD, ALLC, RAND, STFT  # Baseline opponents.
from src.game.engine import play_match  # Runs a match between two strategies.


# Paste the best bitstring you got from GA:
BEST = "1000011110111001010011101101111110111110111111101111011110101101"  # GA champion.


def main():  # Main comparison routine.
    ga = LookupTableStrategy(BEST, name="GA_BEST")  # Create the GA strategy instance.
    opponents = [  # Define baseline opponents to compare against.
        TFT("TFT"),
        TF2T("TF2T"),
        ALLD("ALLD"),
        ALLC("ALLC"),
        RAND("RAND"),
        STFT("STFT"),
    ]

    rounds = 200  # Number of rounds per matchup.
    rows = []  # Accumulate results for CSV export.

    print(f"Matchups over {rounds} rounds:")  # Console header.
    for opp in opponents:  # Loop over opponents.
        ga_score, opp_score = play_match(ga, opp, rounds=rounds)  # Play a match.

        ga_per_round = ga_score / rounds  # Average GA score per round.
        opp_per_round = opp_score / rounds  # Average opponent score per round.

        rows.append({  # Store structured results for CSV.
            "ga_strategy": ga.name,
            "opponent": opp.name,
            "rounds": rounds,
            "ga_score": ga_score,
            "opponent_score": opp_score,
            "ga_per_round": ga_per_round,
            "opponent_per_round": opp_per_round,
            "ga_minus_opp": ga_score - opp_score
        })

        print(f"{ga.name} vs {opp.name}: {ga_score} - {opp_score} "
              f"(per round: {ga_per_round:.2f} - {opp_per_round:.2f})")  # Console summary.

    # Save CSV
    out_path = Path("results") / "tables" / "ga_best_vs_baselines.csv"  # Output location.
    out_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists.

    with out_path.open("w", newline="", encoding="utf-8") as f:  # Open output CSV.
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))  # Use dict writer.
        writer.writeheader()  # Write header row.
        writer.writerows(rows)  # Write all matchup rows.

    print(f"\nSaved matchup table to: {out_path}")  # Final message.


if __name__ == "__main__":  # Script entry point.
    main()  # Run the comparison.