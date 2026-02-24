from pathlib import Path  # Utilities for robust filesystem path handling.
import sys  # Access to Python runtime settings like import search paths.

try:  # First attempt: standard project import when repo root is already on sys.path.
    from src.strategies.lookup_table import random_strategy  # Function under test.
except ModuleNotFoundError:  # Fallback for direct script execution from nested folders.
    repo_root = Path(__file__).resolve().parents[2]  # Move from src/tests to repository root.
    if str(repo_root) not in sys.path:  # Avoid inserting duplicates into import path.
        sys.path.insert(0, str(repo_root))  # Prepend root so `import src...` resolves correctly.
    from src.strategies.lookup_table import random_strategy  # Retry import after path fix.

def main():  # Simple test entry point.
    s = random_strategy()  # Generate a random 64-bit lookup-table strategy string.
    assert len(s) == 64  # Strategy must contain exactly 64 positions.
    assert set(s).issubset({"0", "1"})  # Strategy characters must be only '0' or '1'.
    print("PASS:", s)  # Report success and show generated strategy.

if __name__ == "__main__":  # Execute test only when file is run directly.
    main()  # Invoke test routine.


    ## python src/tests/test_lookup_table.py  # Example command to run this script directly.