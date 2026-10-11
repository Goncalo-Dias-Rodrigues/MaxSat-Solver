from src.strategies.maxsat_strategy import MaxSatStrategy

class BruteForceStrategy(MaxSatStrategy):

    def __init__(self, maxsat):
        self.maxsat = maxsat
        self.variables = maxsat.variables

    def solve(self, max_sat):
        """
        Solves the given MaxSAT problem.

        :param max_sat: MaxSAT problem to solve
        :return: Best result and the hypotheses that achieve that result
        """
        best_result = -1
        best_hypotheses = []
        for _ in range(1 << max_sat.information[2]):
            current_result = max_sat.calculate_clauses(best_result)
            if current_result == max_sat.information[3]:
                if not best_result == max_sat.information[3]:
                    best_hypotheses.clear()
                best_result = current_result
                best_hypotheses.append(max_sat.current_hypothesis_to_string())
            elif current_result >= best_result:
                if not current_result == best_result:
                    best_hypotheses.clear()
                best_result = current_result
                best_hypotheses.append(max_sat.current_hypothesis_to_string())
            self.next_hypothesis()
        return best_result, best_hypotheses

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
