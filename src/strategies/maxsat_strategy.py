from abc import ABC, abstractmethod


class MaxSatStrategy(ABC):
    """
    Defines the interface that every MaxSAT solving strategy must implement.
    """

    @abstractmethod
    def solve(self, max_sat):
        """
        Solves the given MaxSAT problem.

        :param max_sat: MaxSAT problem to solve
        :return: Best result and the hypotheses that achieve that result
        """
        pass