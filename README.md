# MaxSat-Solver

A small Python project focused on solving MaxSAT instances using different search strategies. The repository is built as a learning-oriented implementation: it reads DIMACS CNF files, evaluates candidate assignments against the formula, and compares the performance of exact and heuristic approaches.

The goal is not to build the fastest industrial solver, but to understand how MaxSAT is modeled, how local search behaves, and how optimization strategies can be structured in a clean and reusable way.

## Overview

Maximum Satisfiability (MaxSAT) is a generalization of SAT where the objective is not to satisfy every clause, but to satisfy as many clauses as possible. In practice, this means finding an assignment of Boolean variables that maximizes the number of satisfied clauses in a formula.

This project treats each CNF file as a MaxSAT instance and evaluates assignments using the same logic used in classic SAT solving: every clause is an OR of literals and a clause is satisfied when at least one literal evaluates to True.

The solver currently supports:

- exhaustive search via brute force
- local optimization via next-ascent hill climbing
- execution logging with CSV-based result tracking
- a command-line interface to select instances and algorithms

The repository is intentionally modular so new algorithms can be added without rewriting the solver core.

## Project structure

```text
MaxSat-Solver/
├── .github/
│   └── workflows/
│       ├── test_brute_force.yml
│       └── test_next_ascent_hillclimbing.yml
├── src/
│   ├── files/
│   │   ├── hoos.cnf
│   │   ├── 20variables/
│   │   ├── 100variables/
│   │   └── 250variables/
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
└── .gitignore
```

### Source files

- `src/main.py`: entry point for the CLI. It lets the user pick a CNF instance, choose an algorithm, and run it multiple times.
- `src/file_manager.py`: parses DIMACS CNF files and extracts the problem information and clauses.
- `src/maxsat.py`: core evaluation engine. It contains the logic to evaluate a hypothesis, count satisfied clauses, and convert the current assignment into a binary string.
- `src/result_manager.py`: stores execution data in a CSV file with timestamp, algorithm name, instance size, runtime, and best result.

### Strategies

- `src/strategies/maxsat_strategy.py`: abstract base class that defines the common `solve(max_sat)` interface.
- `src/strategies/brute_force_strategy.py`: exact strategy that enumerates all possible assignments.
- `src/strategies/next_ascent_hillclimbing.py`: local search method that iteratively flips a variable and keeps improving moves.
- `src/strategies/multistart_next_ascent_hillclimbing.py`: placeholder for a multi-start extension of the same idea.

## Patterns used

The code follows a small set of clear patterns that make the solver easy to extend.

### 1. Strategy pattern

Each algorithm implements the same interface defined in `MaxSatStrategy`. This keeps the solver core independent from the search method. The evaluation logic is separated from the optimization logic, which means that a new algorithm can be added by writing a new class that implements `solve()`.

This is a useful pattern for comparing different optimization techniques without rewriting the problem definition or file parser.

### 2. DIMACS CNF parsing

The repository follows the DIMACS format used in SAT and MaxSAT benchmarks:

- header line starting with `p` gives the problem metadata
- comments starting with `c` are ignored
- clauses are listed as integer literals, where positive values indicate positive variables and negative values indicate negated variables
- each clause ends with `0`

The parser in `FileManager` turns this structure into a Python representation that the evaluator can work with.

### 3. Core evaluator

The `MaxSat` class is responsible for evaluating candidate assignments.

- each variable is represented as a Boolean value
- a clause is satisfied when at least one literal evaluates to True
- the solver counts how many clauses are satisfied for a given assignment
- it also uses pruning logic to stop early when a hypothesis cannot beat the current best result

This is the central object around which all strategies are built.

### 4. Result tracking

The `ResultManager` writes structured execution data to `results.csv`. This allows comparisons between algorithms on the same instances and keeps a log of performance metrics such as:

- execution time
- number of variables
- number of clauses
- best objective value
- number of solutions found
- best hypothesis string

### 5. Simple CLI orchestration

The program in `src/main.py` is intentionally minimal and direct. It:

- shows available CNF files
- lets the user pick one
- asks for the algorithm
- asks for the number of executions
- runs the strategy
- saves the results

This keeps the project easy to run and debug while staying close to the core logic.

## Algorithms implemented

### Brute Force

The brute force solver in `BruteForceStrategy` exhaustively enumerates every possible assignment for the variables in the instance.

It works by iterating over the assignment space like a binary counter. For each assignment, the solver evaluates the formula and compares the result to the best value found so far. Because the search space grows exponentially with the number of variables, this approach is only feasible for small or medium instances.

This algorithm is useful as a baseline because it guarantees the optimal value for a given formula.

### Next Ascent Hill Climbing

The next-ascent hill climbing implementation is a local search method designed to escape the rigidity of exhaustive search while keeping the code simple.

The strategy:

- starts from a random assignment
- flips one variable at a time
- evaluates the clause count after each flip
- keeps a move when it improves the current score
- avoids revisiting already tested neighbours
- stops when no better neighbour is available or a search limit is reached

This is a classic hill-climbing pattern: Greedy improvement with a local neighbourhood defined by single-variable flips. In this implementation, the neighbourhood is based on 1-bit Hamming distance changes, which means each neighbour differs from the current assignment by exactly one variable.

The algorithm is lightweight and easy to understand, but it is not guaranteed to reach the global optimum because it may get trapped in local maxima.

## Supported problem files

The repository includes a few DIMACS CNF examples in `src/files`:

- `hoos.cnf`
- `20variables/uf20-01.cnf`
- `100variables/uf100-01.cnf`
- `250variables/uf250-01.cnf`

These files are useful for testing solver behavior across different instance sizes and difficulty levels.

## How to run

From the repository root, run:

```bash
python -m src.main
```

The application will prompt for:

1. the CNF file to use
2. the algorithm to execute
3. the number of runs

After execution, results are stored in `results.csv`.

## Why this project matters

This repository is a practical introduction to MaxSAT solving and metaheuristic design. It demonstrates the difference between:

- exact search, which guarantees optimality but scales poorly
- local search, which is faster and more flexible but can be trapped in local optima

It also shows how to organize a solver around reusable abstractions and how to compare algorithms using observable metrics instead of intuition alone.

## Future direction

More algorithms will come as I advance in the metaheuristics class in university.
The project is intentionally structured to support that growth without breaking the existing solver core.

## Final note

This repository is a learning project, but it is already a solid base for experimenting with MaxSAT and metaheuristic optimization. The current implementations are simple, readable, and modular, which makes them ideal foundations for future comparisons and more advanced search strategies.

