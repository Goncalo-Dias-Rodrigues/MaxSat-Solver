from file_manager import FileManager
from maxsat import MaxSat
from result_manager import ResultManager
import time

from brute_force_strategy import BruteForceStrategy
from src.next_ascent_hillclimbing import NextAscentHillClimbingStrategy


if __name__ == '__main__':

    file_manager = FileManager()


    files = {
        1: "files/20variables/uf20-01.cnf",
        2: "files/hoos.cnf",
        3: "files/100variables/uf100-01.cnf",
        4: "files/250variables/uf250-01.cnf"
    }

    print("\n========== MAX-SAT SOLVER ==========")
    print("\nSelect a CNF file:")

    for option, filename in files.items():
        print(f"{option}. {filename}")

    while True:
        try:
            file_option = int(input("\nEnter the file number: "))

            if file_option in files:
                break

            print("Invalid option. Please select a number from 1 to 4.")

        except ValueError:
            print("Invalid input. Please enter a number.")

    information, clauses = file_manager.get_info(files[file_option])

    print("\nSelect an algorithm:")
    print("1. Brute Force")
    print("2. Next Ascent Hill Climbing")

    while True:
        try:
            algorithm_option = int(input("\nEnter the algorithm number: "))

            if algorithm_option in (1, 2):
                break

            print("Invalid option. Please select 1 or 2.")

        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            executions = int(input("\nHow many times do you want to run the algorithm? "))

            if executions > 0:
                break

            print("The number of executions must be greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    result_manager = ResultManager()

    algorithm_name = (
        "Brute Force"
        if algorithm_option == 1
        else "Next Ascent Hill Climbing"
    )

    print("\n========== EXECUTION CONFIGURATION ==========")
    print(f"CNF file: {files[file_option]}")
    print(f"Number of variables: {information[2]}")
    print(f"Number of clauses: {information[3]}")
    print(f"Algorithm: {algorithm_name}")
    print(f"Number of executions: {executions}")

    confirm = input("\nStart execution? (1 = Yes, 2 = No): ")

    if confirm == "1":

        for execution in range(1, executions + 1):

            print(f"\n========== EXECUTION {execution}/{executions} ==========")

            start = time.perf_counter()

            max_sat = MaxSat(information, clauses)

            if algorithm_option == 1:
                strategy = BruteForceStrategy(max_sat)
            else:
                strategy = NextAscentHillClimbingStrategy(max_sat)

            best_result, best_hypotheses = strategy.solve(max_sat)

            end = time.perf_counter()

            time_taken = end - start

            result_manager.save_result(
                cnf_file=files[file_option],
                algorithm=algorithm_name,
                execution=execution,
                num_variables=information[2],
                num_clauses=information[3],
                execution_time=time_taken,
                best_result=best_result,
                num_solutions=len(best_hypotheses),
                best_hypothesis=best_hypotheses
            )

            print(f"Algorithm execution time: {time_taken:.6f} seconds")
            print(f"Number of variables: {information[2]}")
            print(f"Number of clauses: {information[3]}")
            print(f"Best result: {best_result}")
            print(f"Number of solutions: {len(best_hypotheses)}")
            print(f"Best hypothesis: {best_hypotheses}")

    elif confirm == "2":
        print("\nExecution cancelled.")

    else:
        print("\nInvalid option. Execution cancelled.")
