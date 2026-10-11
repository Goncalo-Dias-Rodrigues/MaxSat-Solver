from file_manager import FileManager
from maxsat import MaxSat
import time

from brute_force_strategy import BruteForceStrategy
from src.next_ascent_hillclimbing import NextAscentHillClimbingStrategy

if __name__ == '__main__':

    file_manager = FileManager()

    #information, clauses = file_manager.get_info("files/20variables/uf20-01.cnf")
    #information, clauses = file_manager.get_info("files/hoos.cnf")
    #information, clauses = file_manager.get_info("files/100variables/uf100-01.cnf")
    information, clauses = file_manager.get_info("files/250variables/uf250-01.cnf")


    # start = time.perf_counter()
    # max_sat = MaxSat(information, clauses)
    # strategy = BruteForceStrategy(max_sat)
    #
    # best_result, best_hypotheses = strategy.solve(max_sat)
    #
    # end = time.perf_counter()
    #
    # time1 = end - start
    # print(f"Algorithm execution time: {time1:.6f} segundos")
    # print(f"Number of variables: {information[2]}")
    # print(f"Number of Clauses: {information[3]}")
    # print(f"Best Result: {best_result}")
    # print(f"Number of solutions: {len(best_hypotheses)}")
    # print(f"Best Hypothesis: {best_hypotheses}")


    for _ in range(0, 30):
        start = time.perf_counter()
        max_sat = MaxSat(information, clauses)
        strategy = NextAscentHillClimbingStrategy(max_sat)

        best_result, best_hypotheses = strategy.solve(max_sat)

        end = time.perf_counter()

        time2 = end - start
        print(f"Algorithm execution time: {time2:.6f} segundos")
        print(f"Number of variables: {information[2]}")
        print(f"Number of Clauses: {information[3]}")
        print(f"Best Result: {best_result}")
        print(f"Number of solutions: {len(best_hypotheses)}")
        print(f"Best Hypothesis: {best_hypotheses}")


    # print(information)
    # print(clauses)

