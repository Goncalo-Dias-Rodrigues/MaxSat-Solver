from itertools import combinations

from src.strategies.maxsat_strategy import MaxSatStrategy


class VariableNeighbourhoodAscent(MaxSatStrategy):
    """
    Solves the MaxSAT problem with Variable Neighbourhood Ascent.

    The neighbourhood N_k(s) is the set of all solutions that differ from s in exactly k variables
    (Hamming distance k). The search starts with k = 1 and, whenever an improvement is found, moves to
    the better solution and goes back to k = 1; otherwise it moves on to the next neighbourhood.
    """

    def __init__(self, *args, max_distance=3):
        """
        Extra positional arguments are ignored, so the strategy can be created the same way as the others
        (e.g. VariableNeighbourhoodAscent() or VariableNeighbourhoodAscent(max_sat)).
        :param max_distance: Largest neighbourhood (number of flipped variables) that will be explored
        """
        self.max_distance = max_distance
        self.evaluations = 0

    def solve(self, max_sat):
        """
        Runs the Variable Neighbourhood Ascent starting from the solution with all variables False.

        :param max_sat: MaxSAT problem to solve
        :return: Best number of True clauses, a list with the hypothesis that achieves it and the number of
        evaluations performed
        """
        number_variables = max_sat.information[2]
        self.evaluations = 0

        # s <- initial solution (all variables False); f(s) <- number of True clauses
        current_value = max_sat.calculate_clauses(0)
        self.evaluations += 1

        k = 1
        while k <= self.max_distance:
            best_flip = None
            best_value = current_value

            for flip in combinations(range(number_variables), k):
                candidate_value = self.evaluate_neighbour(max_sat, flip, best_value)
                if candidate_value > best_value:
                    best_value = candidate_value
                    best_flip = flip

            if best_flip is not None:
                # s <- best ; k <- 1
                self.flip_variables(max_sat, best_flip)
                current_value = best_value
                k = 1
            else:
                k += 1

        return current_value, [max_sat.current_hypothesis_to_string()], self.evaluations

    def evaluate_neighbour(self, max_sat, flip, best_value):
        """
        Evaluates the neighbour obtained by flipping the given variables of the current solution;
        The current solution is restored before returning.
        :param max_sat: MaxSAT problem being solved
        :param flip: Indexes of the variables to flip
        :param best_value: Best value found so far in this neighbourhood
        :return: Number of True clauses of the neighbour, or -1 if it cannot be better than best_value
        """
        self.flip_variables(max_sat, flip)
        # Asking for best_value + 1 lets calculate_clauses stop early on neighbours that cannot improve
        value = max_sat.calculate_clauses(best_value + 1)
        self.evaluations += 1
        self.flip_variables(max_sat, flip)
        return value

    @staticmethod
    def flip_variables(max_sat, indexes):
        """
        Inverts the value of the variables at the given indexes.
        :param max_sat: MaxSAT problem being solved
        :param indexes: Indexes of the variables to invert
        """
        for index in indexes:
            max_sat.variables[index] = not max_sat.variables[index]