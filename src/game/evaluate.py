from game.engine import play_match

def evaluate_strategy(strategy, opponent_pool, rounds=200):
    total_score = 0
    for opponent in opponent_pool:
        s1, _ = play_match(strategy, opponent, rounds)
        total_score += s1
    return total_score / len(opponent_pool)