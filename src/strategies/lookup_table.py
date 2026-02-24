"""
Translates a bitstring (chromosome) into game moves using memory.
Crucial for Genetic Algorithm (Person B) and Machine Learning (Person C).
"""
from strategies.baselines import Strategy

class LookupTableStrategy(Strategy):
    """
    Uses a 64-bit string to decide moves based on the outcomes 
    of the previous 3 rounds.
    """
    def __init__(self, bitstring, name="GA_Strategy"):
        super().__init__(name)
        self.bitstring = bitstring # A string of '0's (Cooperate) and '1's (Defect)

    def move(self, my_h, opp_h):
        # Round 1-3: History is insufficient for a 3-round memory depth.
        # Defaults to 'C' until enough history is accumulated.
        if len(my_h) < 3:
            return 'C' 
        
        # Outcome mapping: Maps round results to a base-4 digit
        m = {'CC': 0, 'CD': 1, 'DC': 2, 'DD': 3}
        
        # Retrieve the outcomes for the 3 most recent rounds
        r1 = m[my_h[-3] + opp_h[-3]] # 3 rounds ago
        r2 = m[my_h[-2] + opp_h[-2]] # 2 rounds ago
        r3 = m[my_h[-1] + opp_h[-1]] # Last round
        
        # Convert the sequence of three base-4 outcomes into a 
        # single base-10 index between 0 and 63.
        # Formula: (Round3 * 4^0) + (Round2 * 4^1) + (Round1 * 4^2)
        index = (r1 * 16) + (r2 * 4) + r3
        
        # Return move based on the bit value at that index position
        return 'C' if self.bitstring[index] == '0' else 'D'