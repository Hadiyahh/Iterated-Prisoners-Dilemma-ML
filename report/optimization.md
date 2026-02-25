Optimization Methods

To discover high-performing strategies for the Iterated Prisoner’s Dilemma, we implemented and compared two optimization methods: a Genetic Algorithm (GA) and Hill Climbing.

Strategy Representation

Each strategy was represented as a 64-bit lookup table. Each bit corresponds to a specific history of the previous three rounds. Since each round has four possible outcomes (CC, CD, DC, DD), there are 4³ = 64 possible histories. Each bit determines whether the strategy cooperates (0) or defects (1) in that situation.

Fitness Evaluation

The fitness of a strategy was defined as its average score when playing matches against a fixed opponent pool. Each match consisted of 200 rounds. The opponent pool included human-designed strategies (ALLC, ALLD, RAND, TFT, TF2T, STFT) and randomly generated lookup-table strategies.

Genetic Algorithm

The Genetic Algorithm maintained a population of candidate strategies. Each generation consisted of selection, crossover, mutation, and elitism. Selection favored strategies with higher fitness. Crossover combined portions of parent strategies, and mutation randomly flipped bits with a small probability. Elitism preserved the best strategies unchanged between generations. The algorithm was run for 200 generations with a population size of 80.

Hill Climbing

Hill Climbing started from a random strategy and repeatedly improved it by flipping individual bits. If the modified strategy had higher fitness, it replaced the current strategy. This process continued for 5000 iterations.

Results

Both optimization methods successfully discovered strategies that performed competitively against baseline strategies. The Genetic Algorithm achieved higher fitness overall and demonstrated stable convergence over generations. Hill Climbing also improved fitness but was more likely to become trapped in local optima.

These results demonstrate that evolutionary optimization methods are effective at discovering strong strategies in the Iterated Prisoner’s Dilemma.