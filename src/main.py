from src.file_manager import FileManager
from src.maxsat import MaxSat
from src.result_manager import ResultManager
import time

from src.strategies.brute_force_strategy import BruteForceStrategy
from src.strategies.multistart_next_ascent_hillclimbing import MultiStartNextAscentHillClimbingStrategy
from src.strategies.multistart_variable_neighbourhood_ascent_strategy import MultistartVariableNeighbourhoodAscent
from src.strategies.next_ascent_hillclimbing import NextAscentHillClimbingStrategy
from src.strategies.variable_neighbourhood_ascent_strategy import VariableNeighbourhoodAscent

if __name__ == '__main__':

    file_manager = FileManager()


    files = {
        1: "src/files/hoos.cnf",
        2: "src/files/20variables/uf20-01.cnf",
        3: "src/files/20variables/uf20-02.cnf",
        4: "src/files/20variables/uf20-03.cnf",
        5: "src/files/100variables/uf100-01.cnf",
        6: "src/files/100variables/uf100-02.cnf",
        7: "src/files/100variables/uf100-03.cnf",
        8: "src/files/250variables/uf250-01.cnf",
        9: "src/files/250variables/uf250-02.cnf",
        10: "src/files/250variables/uf250-03.cnf",
    }
    all_files_option = len(files) + 1
    benchmark_option = all_files_option + 1
    resume_option = benchmark_option + 1

    algorithms = {
        1: ("Brute Force", BruteForceStrategy),
        2: ("Next Ascent Hill Climbing", NextAscentHillClimbingStrategy),
        3: ("Multi-Start Next Ascent Hill Climbing", MultiStartNextAscentHillClimbingStrategy),
        4: ("Variable Neighbourhood Ascent", VariableNeighbourhoodAscent),
        5: ("Multi-Start Variable Neighbourhood Ascent", MultistartVariableNeighbourhoodAscent),
    }

    print("\n========== MAX-SAT SOLVER ==========")
    print("\nSelect a CNF file:")

    for option, filename in files.items():
        print(f"{option}. {filename}")
    print(f"{all_files_option}. All files")
    print(f"{benchmark_option}. All files with all algorithms (excluding hoos.cnf)")
    print(f"{resume_option}. Resume previous all-files/all-algorithms run")

    while True:
        try:
            file_option = int(input("\nEnter the file number: "))

            if file_option in files or file_option in (all_files_option, benchmark_option, resume_option):
                break

            print(f"Invalid option. Please select a number from 1 to {resume_option}.")

        except ValueError:
            print("Invalid input. Please enter a number.")

    resume_mode = file_option == resume_option
    benchmark_mode = file_option in (benchmark_option, resume_option)
    if benchmark_mode:
        selected_algorithms = list(algorithms.items())[1:]
    else:
        print("\nSelect an algorithm:")
        for option, (name, _) in algorithms.items():
            print(f"{option}. {name}")

        while True:
            try:
                algorithm_option = int(input("\nEnter the algorithm number: "))

                if algorithm_option in algorithms:
                    break

                print("Invalid option. Please select 1, 2, 3, 4 or 5.")

            except ValueError:
                print("Invalid input. Please enter a number.")

        selected_algorithms = [(algorithm_option, algorithms[algorithm_option])]

    while True:
        try:
            executions = int(input("\nHow many iterations do you want to run? "))

            if executions > 0:
                break

            print("The number of executions must be greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    result_manager = ResultManager()
    completed_executions = result_manager.get_completed_executions() if resume_mode else set()

    print("\n========== EXECUTION CONFIGURATION ==========")
    if benchmark_mode:
        print(f"CNF files: all {len(files) - 1} files (excluding hoos.cnf)")
        print("Algorithms: all, from Next Ascent Hill Climbing onwards")
        if resume_mode:
            print("Mode: resume, skipping iterations already saved in results.csv")
    elif file_option == all_files_option:
        print(f"CNF files: all {len(files)} files")
    else:
        print(f"CNF file: {files[file_option]}")
    if not benchmark_mode:
        print(f"Algorithm: {selected_algorithms[0][1][0]}")
    print(f"Number of iterations: {executions}")

    confirm = input("\nStart execution? (1 = Yes, 2 = No): ")

    if confirm == "1":

        if benchmark_mode:
            selected_files = list(files.items())[1:]
        elif file_option == all_files_option:
            selected_files = list(files.items())
        else:
            selected_files = [(file_option, files[file_option])]

        for _, (algorithm_name, strategy_class) in selected_algorithms:
            print(f"\n========== ALGORITHM: {algorithm_name} ==========")

            for _, cnf_file in selected_files:
                information, clauses = file_manager.get_info(cnf_file)

                print(f"\n========== CNF FILE: {cnf_file} ==========")
                print(f"Number of variables: {information[2]}")
                print(f"Number of clauses: {information[3]}")

                for execution in range(1, executions + 1):
                    completed_key = (cnf_file, algorithm_name, execution)
                    if resume_mode and completed_key in completed_executions:
                        print(f"\nSkipping iteration {execution}/{executions}; result already exists.")
                        continue

                    print(f"\n========== ITERATION {execution}/{executions} ==========")

                    start = time.perf_counter()

                    max_sat = MaxSat(information, clauses)
                    strategy = strategy_class(max_sat)
                    best_result, best_hypotheses, number_of_evaluations = strategy.solve(max_sat)

                    time_taken = time.perf_counter() - start

                    result_manager.save_result(
                        cnf_file=cnf_file,
                        algorithm=algorithm_name,
                        execution=execution,
                        num_variables=information[2],
                        num_clauses=information[3],
                        number_evaluations=number_of_evaluations,
                        execution_time=time_taken,
                        best_result=best_result,
                        num_solutions=len(best_hypotheses),
                        best_hypothesis=best_hypotheses
                    )
                    completed_executions.add(completed_key)

                    print(f"Algorithm execution time: {time_taken:.6f} seconds")
                    print(f"Number of variables: {information[2]}")
                    print(f"Number of clauses: {information[3]}")
                    print(f"Number of evaluations: {number_of_evaluations}")
                    print(f"Best result: {best_result}")
                    print(f"Number of solutions: {len(best_hypotheses)}")
                    print(f"Best hypothesis: {best_hypotheses}")
                    if isinstance(strategy, BruteForceStrategy):
                        for distance, count in strategy.local_optima_counts.items():
                            print(f"Number of local optima (Hamming distance {distance}): {count}")

    elif confirm == "2":
        print("\nExecution cancelled.")

    else:
        print("\nInvalid option. Execution cancelled.")
