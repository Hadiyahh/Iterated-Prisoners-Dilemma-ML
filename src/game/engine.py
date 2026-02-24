from game.payoff import payoff

def play_match(strategy1, strategy2, rounds=200):
    history1, history2 = [], []
    score1, score2 = 0, 0
    strategy1.reset(); strategy2.reset()
    
    for _ in range(rounds):
        move1 = strategy1.move(history1, history2)
        move2 = strategy2.move(history2, history1)
        
        p1, p2 = payoff(move1, move2)
        score1 += p1
        score2 += p2
        
        history1.append(move1)
        history2.append(move2)
    return score1, score2

def play_tournament(strategies, rounds=200):
    results = {s.name: 0 for s in strategies}
    for i, s1 in enumerate(strategies):
        for s2 in strategies[i+1:]:
            sc1, sc2 = play_match(s1, s2, rounds)
            results[s1.name] += sc1
            results[s2.name] += sc2
    return results