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
from pathlib import Path
from src.strategies.baselines import ALLC, ALLD, RAND, TFT, TF2T, STFT
from src.game.engine import play_tournament

def main():
    strategies = [
        ALLC("ALLC"),
        ALLD("ALLD"),
        RAND("RAND"),
        TFT("TFT"),
        TF2T("TF2T"),
        STFT("STFT")
    ]

    results = play_tournament(strategies)

    print("Tournament Results:")
    for name, score in results.items():
        print(f"{name}: {score}")

    # SAVE CSV
    out = Path("results/tables/baselines_tournament.csv")
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["strategy", "score"])
        for name, score in results.items():
            writer.writerow([name, score])

    print("Saved baselines_tournament.csv")

if __name__ == "__main__":
    main()