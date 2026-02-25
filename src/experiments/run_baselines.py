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

    results = play_tournament(strategies, rounds=200)

    print("Tournament Results:")
    for name, score in results.items():
        print(f"{name}: {score}")

if __name__ == "__main__":
    main()