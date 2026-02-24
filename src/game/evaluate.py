"""
Determines the fitness of a strategy by testing it against a pool of opponents.
Used by the GA to decide which strategies survive to the next generation.
"""
from game.engine import play_match

def evaluate_strategy(strategy, opponent_pool, rounds=200):
    """
    Plays the given strategy against every opponent in the pool.
    Returns: The average score per match.
    """
    total_score = 0
    for opponent in opponent_pool:
        # We only care about player 1's score (the strategy being tested)
        s1, _ = play_match(strategy, opponent, rounds)
        total_score += s1
    
    # Return average fitness across the entire population of opponents
    return total_score / len(opponent_pool)