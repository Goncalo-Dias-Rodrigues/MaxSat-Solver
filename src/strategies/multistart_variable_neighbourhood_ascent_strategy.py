import random
from itertools import combinations

from src.strategies.maxsat_strategy import MaxSatStrategy


class MultistartVariableNeighbourhoodAscent(MaxSatStrategy):
    """
    Solves the MaxSAT problem with Multistart Variable Neighbourhood Ascent (MSVNA).

    Variable Neighbourhood Ascent is restarted from a new random solution until either:
      - a global optimum is found (all clauses satisfied), or
      - when a restart is about to begin, at least max_evaluations objective function evaluations
        have already been performed.
    """

    def __init__(self, *args, max_distance=3, max_evaluations=10_000_000, seed=None):
        """
        Extra positional arguments are ignored, so the strategy can be created the same way as the others.
        :param max_distance: Largest neighbourhood (number of flipped variables) explored by each ascent
        :param max_evaluations: Evaluation budget checked at the beginning of every restart
        :param seed: Optional seed for the random starting solutions
        """
        self.max_distance = max_distance
        self.max_evaluations = max_evaluations
        self.random = random.Random(seed)
        self.evaluations = 0

    def solve(self, max_sat):
        """
        Runs the multistart search.

        :param max_sat: MaxSAT problem to solve
        :return: Best number of True clauses, the distinct hypotheses (found) that achieve it and the number of
        evaluations performed
        """
        number_variables = max_sat.information[2]
        optimum = max_sat.information[3]  # global optimum: every clause is True
        self.evaluations = 0

        best_result = -1
        best_hypotheses = []

        while best_result < optimum and self.evaluations < self.max_evaluations:
            # Restart: random initial solution
            max_sat.variables = [self.random.random() < 0.5 for _ in range(number_variables)]
            result = self.variable_neighbourhood_ascent(max_sat, number_variables, optimum)

            hypothesis = max_sat.current_hypothesis_to_string()
            if result > best_result:
                best_result = result
                best_hypotheses = [hypothesis]
            elif result == best_result and hypothesis not in best_hypotheses:
                best_hypotheses.append(hypothesis)

        return best_result, best_hypotheses, self.evaluations

    def variable_neighbourhood_ascent(self, max_sat, number_variables, optimum):
        """
        Variable Neighbourhood Ascent starting from the current values of max_sat.variables;
        Leaves the local optimum found in max_sat.variables.
        :param max_sat: MaxSAT problem being solved
        :param number_variables: Number of variables of the problem
        :param optimum: Value of the global optimum (stops the ascent as soon as it is reached)
        :return: Number of True clauses of the local optimum found
        """
        current_value = max_sat.calculate_clauses(0)
        self.evaluations += 1

        k = 1
        while k <= self.max_distance and current_value < optimum:
            best_flip = None
            best_value = current_value

            for flip in combinations(range(number_variables), k):
                self.flip_variables(max_sat, flip)
                # Asking for best_value + 1 lets calculate_clauses stop early on neighbours that cannot improve
                value = max_sat.calculate_clauses(best_value + 1)
                self.evaluations += 1
                self.flip_variables(max_sat, flip)

                if value > best_value:
                    best_value = value
                    best_flip = flip

            if best_flip is not None:
                self.flip_variables(max_sat, best_flip)
                current_value = best_value
                k = 1
            else:
                k += 1

        return current_value

    @staticmethod
    def flip_variables(max_sat, indexes):
        """
        Inverts the value of the variables at the given indexes.
        :param max_sat: MaxSAT problem being solved
        :param indexes: Indexes of the variables to invert
        """
        for index in indexes:
            max_sat.variables[index] = not max_sat.variables[index]