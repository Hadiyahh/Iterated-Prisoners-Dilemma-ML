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
    
    standard_results = play_tournament(strategies, rounds=200)
    
    # Save and Print Standard results
    with open("baselines_standard.csv", "w", newline="") as f:
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
    stress_results = play_tournament(stress_strategies, rounds=200)

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

if __name__ == "__main__":
    main()