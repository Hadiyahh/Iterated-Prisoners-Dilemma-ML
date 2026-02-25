import random  # Randomness for generating random strategies.
from src.strategies.baselines import ALLC, ALLD, RAND, TFT, TF2T, STFT  # Baseline strategies.
from src.strategies.lookup_table import LookupTableStrategy  # Strategy using a lookup table.

def random_strategy(n=64):  # Create a random bitstring of length n.
    return ''.join(random.choice('01') for _ in range(n))  # Choose 0/1 for each position.

def get_opponent_pool(seed=42, num_random=10):  # Build a reproducible opponent pool.
    random.seed(seed)  # Fix RNG for repeatable pools.
    pool = [  # Start with standard baseline opponents.
        ALLC("ALLC"),
        ALLD("ALLD"),
        RAND("RAND"),
        TFT("TFT"),
        TF2T("TF2T"),
        STFT("STFT"),
    ]
    for i in range(num_random):  # Add random lookup-table opponents.
        pool.append(LookupTableStrategy(random_strategy(64), name=f"RND_LUT_{i}"))  # Append each.
    return pool  # Return the full list of opponents.

if __name__ == "__main__":  # Run a quick check when executed directly.
    pool = get_opponent_pool()  # Build the default pool.
    print(f"Generated {len(pool)} opponents:")  # Print count.
    for p in pool:  # Print each opponent name.
        print("-", p.name)  # Output the strategy label.