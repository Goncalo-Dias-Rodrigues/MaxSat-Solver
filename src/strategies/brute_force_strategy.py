from itertools import combinations

from src.strategies.maxsat_strategy import MaxSatStrategy


class BruteForceStrategy(MaxSatStrategy):

    def __init__(self, maxsat):
        self.maxsat = maxsat
        self.variables = maxsat.variables
        self.local_optima_counts = {}

    def solve(self, max_sat):
        """
        Solves the given MaxSAT problem.

        :param max_sat: MaxSAT problem to solve
        :return: Best result and the hypotheses that achieve that result
        """
        number_of_variables = max_sat.information[2]
        max_sat.variables[:] = [False] * number_of_variables
        self.variables = max_sat.variables

        best_result = -1
        number_of_evaluations = 0
        best_hypotheses = []
        scores = []

        for _ in range(1 << max_sat.information[2]):
            current_result = max_sat.calculate_clauses(-1)
            number_of_evaluations += 1
            scores.append(current_result)

            if current_result > best_result:
                best_hypotheses.clear()
                best_result = current_result
                best_hypotheses.append(max_sat.current_hypothesis_to_string())
            elif current_result == best_result:
                best_hypotheses.append(max_sat.current_hypothesis_to_string())
            self.next_hypothesis()

        self.local_optima_counts = self.count_local_optima(scores, number_of_variables)
        return best_result, best_hypotheses, number_of_evaluations

    @staticmethod
    def count_local_optima(scores, number_of_variables, max_distance=4):
        """
        Counts assignments that have no strictly better neighbour at each exact Hamming distance.

        :param scores: Objective value for every assignment in binary-count order
        :param number_of_variables: Number of Boolean variables in the problem
        :param max_distance: Largest Hamming distance to examine
        :return: Mapping from distance k to the number of local optima in its neighbourhood
        """
        flip_masks_by_distance = {
            distance: tuple(
                sum(1 << index for index in indexes)
                for indexes in combinations(range(number_of_variables), distance)
            )
            for distance in range(1, max_distance + 1)
        }
        local_optima_counts = {}

        for distance, flip_masks in flip_masks_by_distance.items():
            local_optima_counts[distance] = sum(
                not any(scores[assignment ^ flip_mask] > score for flip_mask in flip_masks)
                for assignment, score in enumerate(scores)
            )

        return local_optima_counts

    def next_hypothesis(self):
        """
        Calculates the next hypothesis by adding 1 to the variables array, like a binary counter;
        Changes the array in place, so nothing needs to be rebuilt.
        The first variable is the most significant one, so the order is the same as the binary String.
        """
        index = len(self.variables) - 1
        while index >= 0 and self.variables[index]:
            self.variables[index] = False
            index -= 1
        if index >= 0:
            self.variables[index] = True
