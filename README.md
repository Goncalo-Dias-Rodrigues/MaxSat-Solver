# MaxSat-Solver

A small Python project for solving MaxSAT instances using different search strategies. The project reads DIMACS CNF files, evaluates candidate assignments, and compares exact and heuristic approaches on the same problem instances.

The objective is educational: the solver is intentionally simple and modular, making it easy to understand how MaxSAT is modeled, how local search works, and how optimization algorithms can be structured around a shared core.

## Overview

Maximum Satisfiability (MaxSAT) generalizes SAT by maximizing the number of satisfied clauses rather than requiring all of them to be satisfied. In practice, each CNF instance is treated as a set of Boolean variables and clauses, and the solver looks for an assignment that satisfies as many clauses as possible.

The current codebase includes:

- brute-force exact search
- next-ascent hill climbing
- multi-start next-ascent hill climbing
- DIMACS CNF file parsing
- execution logging to CSV
- a simple CLI to configure and run experiments

## Project structure

```text
MaxSat-Solver/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── test_brute_force.yml
│       └── test_next_ascent_hillclimbing.yml
├── src/
│   ├── files/
│   │   ├── hoos.cnf
│   │   ├── 20variables/
│   │   ├── 100variables/
│   │   ├── 250variables/
│   │   └── ...
│   ├── reports/
│   │   └── Lab1 Metaheuristics Report.pdf
│   ├── strategies/
│   │   ├── brute_force_strategy.py
│   │   ├── maxsat_strategy.py
│   │   ├── multistart_next_ascent_hillclimbing.py
│   │   └── next_ascent_hillclimbing.py
│   ├── file_manager.py
│   ├── main.py
│   ├── maxsat.py
│   ├── result_manager.py
│   └── __pycache__/
├── README.md
├── results.csv
├── .gitignore
└── .gitattributes
```

### Main source files

- `src/main.py`: entry point for the interactive CLI. It lets the user select a CNF file, an algorithm, and the number of executions.
- `src/file_manager.py`: parses DIMACS CNF files and extracts the problem metadata and the clause list.
- `src/maxsat.py`: core evaluator. It stores the current assignment, checks whether a clause is satisfied, counts satisfied clauses, and supports early pruning.
- `src/result_manager.py`: saves execution metrics to `results.csv` with timestamp and results for each run.

### Strategy layer

- `src/strategies/maxsat_strategy.py`: abstract base interface for all algorithms.
- `src/strategies/brute_force_strategy.py`: exact search over every assignment of the Boolean variables.
- `src/strategies/next_ascent_hillclimbing.py`: local search that improves the current hypothesis by flipping one variable at a time.
- `src/strategies/multistart_next_ascent_hillclimbing.py`: repeated random-start hill climbing to improve robustness.

## DIMACS CNF support

The solver expects files in the standard DIMACS CNF format used in SAT/MaxSAT benchmarks:

- `p` lines describe the instance metadata (`num_vars num_clauses`)
- comments beginning with `c` are ignored
- clauses are written as integer literals, where positive numbers mean positive literals and negative numbers mean negated literals
- each clause ends with `0`

The parser in `FileManager` extracts the metadata and produces a list of clauses ready for evaluation.

## Core evaluation model

The `MaxSat` class is the center of the solver. It contains:

- the current assignment for each variable
- clause evaluation logic
- a count of satisfied clauses
- early stopping when a candidate hypothesis cannot beat the best result so far
- conversion from the current variable assignment to a binary string representation

Each clause is considered satisfied when at least one literal evaluates to `True`.

## Available algorithms

### 1. Brute Force

`BruteForceStrategy` enumerates every assignment of the variables in binary-count order. It checks each one against the formula and keeps the best value found. This is exact and useful as a baseline, but it grows exponentially with the number of variables.

### 2. Next Ascent Hill Climbing

`NextAscentHillClimbingStrategy` starts from a random assignment and iteratively flips one variable at a time. It accepts a move only if it improves the current score and avoids revisiting already explored neighbors. This makes it a simple greedy local-search strategy.

### 3. Multi-Start Next Ascent Hill Climbing

`MultiStartNextAscentHillClimbingStrategy` repeats the previous process from multiple random starts. The idea is to reduce the risk of being trapped in a poor local optimum by exploring several basins of attraction.

## Example CNF files

The repository ships with sample DIMACS instances under `src/files`:

- `hoos.cnf`
- `20variables/uf20-01.cnf`
- `20variables/uf20-02.cnf`
- `20variables/uf20-03.cnf`
- `100variables/uf100-01.cnf`
- `100variables/uf100-02.cnf`
- `100variables/uf100-03.cnf`
- `250variables/uf250-01.cnf`
- `250variables/uf250-02.cnf`
- `250variables/uf250-03.cnf`

These are useful for testing solver behavior across different instance sizes and difficulty levels.

## How to run

From the repository root, run:

```bash
python -m src.main
```

The CLI will ask for:

1. the CNF file to use
2. the algorithm to run
3. the number of executions
4. confirmation to start the run

After each execution, the program prints the elapsed time, evaluation count, best result, and best hypothesis. The results are also persisted to `results.csv`.

## Result tracking

`ResultManager` writes one row per execution with the following data:

- timestamp
- CNF filename
- algorithm name
- execution number
- number of variables
- number of clauses
- number of evaluations
- execution time in seconds
- best result
- number of solutions found
- best hypothesis

This makes it easy to compare runs and visualize performance differences between strategies.

## Why this project matters

This project is a practical introduction to MaxSAT solving and heuristic optimization. It demonstrates the contrast between:

- exact search, which guarantees optimality but scales poorly
- local search, which is faster and more flexible but may remain trapped in local optima

It also shows how to organize a solver around reusable abstractions and how to compare algorithms with measurable metrics instead of intuition alone.

## Notes

This repository is intentionally compact and educational. The design is easy to extend, so new strategies, pruning heuristics, or other SAT/MaxSAT techniques can be added without rewriting the core logic.

