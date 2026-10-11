import random

from maxsat_strategy import MaxSatStrategy


class NextAscentHillClimbingStrategy(MaxSatStrategy):
    """
    Next Ascent Hillclimbing using a 1-bit Hamming Distance neighbourhood
    """

    def __init__(self, maxsat):
        self.maxsat = maxsat
        self.variables = maxsat.variables
        self.get_random_start()
        self.index_to_change = 0

    def solve(self, max_sat):
        """
        """
        best_result = -1
        best_hypotheses = []
        visited_neighbours = []
        has_better_neighbour = True

        while has_better_neighbour:
            if len(visited_neighbours) >= max_sat.information[2]:
                break

            while tuple(self.variables) in visited_neighbours:
                self.go_back()
                self.get_neighbour()

            current_result = max_sat.calculate_clauses(best_result)
            visited_neighbours.append(tuple(self.variables))

            if current_result > best_result:
                best_hypotheses.clear()
                best_result = current_result
                best_hypotheses.append(max_sat.current_hypothesis_to_string())
                visited_neighbours.clear()
            else:
                self.go_back()
            self.get_neighbour()
        return best_result, best_hypotheses

    def get_neighbour(self):
        #print(self.variables)
        self.index_to_change = random.randint(0, len(self.variables) - 1)
        self.variables[self.index_to_change] = not self.variables[self.index_to_change]

    def go_back(self):
        self.variables[self.index_to_change] = not self.variables[self.index_to_change]

    def get_random_start(self):
        for index in range(len(self.variables) - 1):
            random_boolean = random.randint(0, 9)
            if random_boolean < 5:
                self.variables[index] = True
            elif random_boolean >= 5:
                self.variables[index] = False