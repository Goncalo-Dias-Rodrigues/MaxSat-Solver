
class MaxSat:
    """
        Solves the maxsat problem with brute-force
    """

    def __init__(self, info, clauses):
        """
        Initializes the MaxSat instance with the problem information and clauses;
        Creates the variables array with all variables initialized to False.
        :param info: Information from the header of the file
        :param clauses: Every clause from the formula with the respective index and polarity of each variable
        """
        self.information = info
        self.clauses = clauses
        self.variables = [False] * self.information[2]

    def calculate_clauses(self, best_result):
        """
        Counts how many clauses are True for the current hypothesis;
        Stops as soon as the false clauses make it impossible to reach the best result so far.
        :param best_result: Best number of True clauses found until now
        :return: Number of True clauses, or -1 if this hypothesis cannot reach best_result
        """
        allowed_failures = self.information[3] - best_result
        failures = 0
        for clause in self.clauses:
            if not self.calculate_result(clause):
                failures += 1
                if failures > allowed_failures:
                    return -1
        return self.information[3] - failures

    def calculate_result(self, clause):
        """
        Calculates the result of a specific clause by evaluating each variable according to its polarity;
        Since all variables inside a clause are connected by "or" operators, the clause is True as soon as at least one
        literal evaluates to True.
        :param clause: Clause that will be analysed
        :return: True if at least 1 True exists, false otherwise
        """
        for value in clause:
            if value - 1 >= 0:
                if self.variables[value-1]:
                    return True
            else:
                if not self.variables[abs(value) - 1]:
                    return True
        return False

    def current_hypothesis_to_string(self):
        """
        Converts the current values of the variables to a binary String (False -> 0, True -> 1).
        Only used when a hypothesis is good enough to be stored.
        :return: Current hypothesis as a String
        """
        hypothesis = ""
        for value in self.variables:
            if value:
                hypothesis += "1"
            else:
                hypothesis += "0"
        return hypothesis
