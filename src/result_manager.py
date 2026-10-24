import csv
import os
from datetime import datetime


class ResultManager:

    def __init__(self, filename="results.csv"):
        self.filename = filename

        self.fields = [
            "timestamp",
            "cnf_file",
            "algorithm",
            "execution",
            "num_variables",
            "num_clauses",
            "number_evaluations",
            "execution_time_seconds",
            "best_result",
            "num_solutions",
            "best_hypothesis"
        ]

        # Create the CSV file with headers if it doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.fields)
                writer.writeheader()

    def save_result(self, cnf_file, algorithm, execution, num_variables, num_clauses, number_evaluations, execution_time, best_result,
                    num_solutions, best_hypothesis):
        with open(self.filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)

            writer.writerow({
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "cnf_file": cnf_file,
                "algorithm": algorithm,
                "execution": execution,
                "num_variables": num_variables,
                "num_clauses": num_clauses,
                "number_evaluations": number_evaluations,
                "execution_time_seconds": round(execution_time, 6),
                "best_result": best_result,
                "num_solutions": num_solutions,
                "best_hypothesis": best_hypothesis
            })

        print(f"Results saved to '{self.filename}'.")

    def get_completed_executions(self):
        completed = set()

        if not os.path.exists(self.filename):
            return completed

        with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row_number, row in enumerate(reader, start=2):
                try:
                    execution = int(row["execution"])
                    completed.add((row["cnf_file"], row["algorithm"], execution))
                except (KeyError, TypeError, ValueError) as error:
                    raise ValueError(
                        f"Invalid result entry in '{self.filename}' on row {row_number}."
                    ) from error

        return completed