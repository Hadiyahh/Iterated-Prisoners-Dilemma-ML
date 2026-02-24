"""
Defines the scoring rules for the Prisoner's Dilemma.
This is the 'Source of Truth' for all point calculations in the project.
"""

def payoff(move1, move2):
    """
    Returns the points earned by player 1 and player 2 based on their moves.
    Moves: 'C' for Cooperate, 'D' for Defect.
    
    Point System:
    - Both Cooperate (CC): 3 points each (Reward)
    - Both Defect (DD): 1 point each (Punishment)
    - One Defects, One Cooperates: 5 points for the Defector (Temptation), 
      0 points for the Cooperator (Sucker's Payoff).
    """
    if move1 == "C" and move2 == "C":
        return 3, 3
    elif move1 == "C" and move2 == "D":
        return 0, 5
    elif move1 == "D" and move2 == "C":
        return 5, 0
    else:  # Both 'D'
        return 1, 1