"""
Implementation of standard human-designed strategies for the 
Prisoner's Dilemma tournament.
"""
import random

class Strategy:
    """Base class that all strategies must inherit from."""
    def __init__(self, name): 
        self.name = name
    def reset(self): 
        """Resets internal memory or state if necessary."""
        pass
    def move(self, my_history, opp_history): 
        """Decides 'C' or 'D' based on match history."""
        pass

class ALLC(Strategy):
    """The 'Sucker': Always cooperates regardless of opponent behavior."""
    def move(self, my_h, opp_h): return 'C'

class ALLD(Strategy):
    """The 'Grinch': Always defects to maximize short-term gain."""
    def move(self, my_h, opp_h): return 'D'

class RAND(Strategy):
    """The 'Unpredictable': Cooperates or Defects with a 50/50 probability."""
    def move(self, my_h, opp_h): return random.choice(['C', 'D'])

class TFT(Strategy):
    """
    Tit-for-Tat: Starts with Cooperation, then copies the opponent's 
    previous move. Simple, fair, and highly effective.
    """
    def move(self, my_h, opp_h):
        return 'C' if not opp_h else opp_h[-1]

class TF2T(Strategy):
    """
    Tit-for-Two-Tats: More forgiving than TFT. Only defects if the 
    opponent has defected in both of the last two rounds.
    """
    def move(self, my_h, opp_h):
        if len(opp_h) < 2: return 'C'
        return 'D' if opp_h[-1] == 'D' and opp_h[-2] == 'D' else 'C'

class STFT(Strategy):
    """
    Suspicious Tit-for-Tat: Like TFT, but starts the match with a Defection.
    Used to test how opponents react to early aggression.
    """
    def move(self, my_h, opp_h):
        return 'D' if not opp_h else opp_h[-1]