import os
import random
import pandas as pd

from src.experiments.opponent_pool import get_opponent_pool
from src.game.evaluate import evaluate_strategy
from src.strategies.lookup_table import LookupTableStrategy


# -----------------------------
# Config (keep consistent!)
# -----------------------------
SEED = 42
ROUNDS = 200
NUM_RANDOM_OPPONENTS = 10
MEMORY_DEPTH = 3               # memory=3 => 4^3 = 64 bits
NUM_RANDOM_STRATEGIES = 500    # generate this many random strategies

GA_BEST_PATH = "results/tables/ga_best.csv"
HILL_BEST_PATH = "results/tables/hill_best.csv"
OUT_PATH = "results/tables/ml_dataset.csv"


def lut_length(memory_depth: int) -> int:
    """Lookup table length for memory depth d is 4^d."""
    return 4 ** memory_depth


def bits_to_features(bits: str):
    """Convert bitstring -> list of ints [0/1]."""
    return [1 if ch == "1" else 0 for ch in bits.strip()]


def load_best_bitstring(path: str) -> str | None:
    """Load best_bitstring from a CSV (first row). Return None if file missing."""
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    if "best_bitstring" not in df.columns:
        raise ValueError(f"{path} missing 'best_bitstring'. Columns: {list(df.columns)}")
    return str(df.iloc[0]["best_bitstring"]).strip()


def make_random_bitstring(rng: random.Random, n: int) -> str:
    return "".join(rng.choice("01") for _ in range(n))


def main():
    rng = random.Random(SEED)
    n_bits = lut_length(MEMORY_DEPTH)

    # 1) Fixed opponent pool (same as comparisons)
    opponents = get_opponent_pool(seed=SEED, num_random=NUM_RANDOM_OPPONENTS)

    rows = []

    # 2) Add GA/Hill best strategies (if available)
    ga_bits = load_best_bitstring(GA_BEST_PATH)
    if ga_bits:
        rows.append(("GA_BEST", ga_bits))

    hill_bits = load_best_bitstring(HILL_BEST_PATH)
    if hill_bits:
        rows.append(("HILL_BEST", hill_bits))

    # 3) Add lots of random strategies
    for i in range(NUM_RANDOM_STRATEGIES):
        rows.append((f"RND_{i}", make_random_bitstring(rng, n_bits)))

    # 4) Score each strategy vs the opponent pool, build dataset
    data = []
    for name, bits in rows:
        if len(bits) != n_bits:
            # Skip incompatible strategies (important if some files are not memory=3)
            continue

        strat = LookupTableStrategy(bits, name=name)
        score = evaluate_strategy(strat, opponents, rounds=ROUNDS)

        feats = bits_to_features(bits)
        record = {f"b{i}": feats[i] for i in range(n_bits)}
        record["name"] = name
        record["score"] = float(score)
        data.append(record)

    df = pd.DataFrame(data)

    # 5) Create classification label: top 20% = good
    threshold = df["score"].quantile(0.8)
    df["label_good"] = (df["score"] >= threshold).astype(int)

    # 6) Save
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"Saved: {OUT_PATH}")
    print(f"Rows: {len(df)} | Features: {n_bits} | Good threshold (80th pct): {threshold:.3f}")
    print(df[["name", "score", "label_good"]].sort_values("score", ascending=False).head(10))


if __name__ == "__main__":
    main()
