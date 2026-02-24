def payoff(move1, move2):
    if move1 == "C" and move2 == "C":
        return 3, 3
    elif move1 == "C" and move2 == "D":
        return 0, 5
    elif move1 == "D" and move2 == "C":
        return 5, 0
    else:
        return 1, 1