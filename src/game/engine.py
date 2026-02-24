"""
Logic for running simulations, including individual matches 
and round-robin tournaments.
"""
from game.payoff import payoff

def play_match(strategy1, strategy2, rounds=200):
    """
    Runs a simulation between two specific strategies.
    - Resets strategies before starting.
    - Iterates for the specified number of rounds.
    - Tracks move history for both players.
    """
    history1, history2 = [], []
    score1, score2 = 0, 0
    strategy1.reset(); strategy2.reset()
    
    for _ in range(rounds):
        # Determine current round moves based on full previous history
        move1 = strategy1.move(history1, history2)
        move2 = strategy2.move(history2, history1)
        
        # Calculate and accumulate scores
        p1, p2 = payoff(move1, move2)
        score1 += p1
        score2 += p2
        
        # Log moves to the history list
        history1.append(move1)
        history2.append(move2)
    return score1, score2

def play_tournament(strategies, rounds=200):
    """
    Executes a round-robin tournament where every strategy plays 
    every other strategy once.
    Returns: A dictionary mapping strategy names to their total accumulated scores.
    """
    results = {s.name: 0 for s in strategies}
    for i, s1 in enumerate(strategies):
        for s2 in strategies[i+1:]:
            sc1, sc2 = play_match(s1, s2, rounds)
            results[s1.name] += sc1
            results[s2.name] += sc2
    return results