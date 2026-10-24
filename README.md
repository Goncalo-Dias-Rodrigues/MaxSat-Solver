# MaxSat-Solver

A compact Python project for benchmarking exact and heuristic MaxSAT strategies on DIMACS CNF instances.

The solver reads CNF files, evaluates assignments against the formula, and compares algorithms on the same instances under a shared execution loop. It is intentionally simple and modular so that the core MaxSAT logic remains easy to inspect while the strategy layer can be swapped out for different search methods.

## Overview

Maximum Satisfiability (MaxSAT) extends SAT by maximizing the number of satisfied clauses instead of requiring every clause to be satisfied. In this project each instance is parsed as a Boolean formula and the solver searches for assignments that satisfy as many clauses as possible.

The repository currently includes these strategies:

- brute-force exact search
- next-ascent hill climbing
- multi-start next-ascent hill climbing
- variable neighbourhood ascent
- multi-start variable neighbourhood ascent

It also includes utilities to persist benchmark results and generate summary tables/plots from `results.csv`.

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
│   │   ├── multistart_variable_neighbourhood_ascent_strategy.py
│   │   ├── next_ascent_hillclimbing.py
│   │   └── variable_neighbourhood_ascent_strategy.py
│   ├── file_manager.py
│   ├── graph.py
│   ├── main.py
│   ├── maxsat.py
│   ├── result_manager.py
│   ├── tabelas/
│   ├── tabelas_medias.py
│   └── __pycache__/
├── README.md
├── results.csv
├── .gitignore
├── .gitattributes
└── .idea/
```

### Core files

- `src/main.py`: interactive runner for choosing a CNF instance, algorithm, and number of executions.
- `src/file_manager.py`: parses DIMACS CNF files and extracts metadata, variables, and clauses.
- `src/maxsat.py`: core evaluator that tracks variable assignments, clause satisfaction, and early pruning.
- `src/result_manager.py`: stores execution metrics in `results.csv`.

### Strategy layer

- `src/strategies/maxsat_strategy.py`: shared interface for all strategies.
- `src/strategies/brute_force_strategy.py`: exact search over the full assignment space.
- `src/strategies/next_ascent_hillclimbing.py`: greedy local search that flips one variable at a time.
- `src/strategies/multistart_next_ascent_hillclimbing.py`: repeated hill climbing from random restarts.
- `src/strategies/variable_neighbourhood_ascent_strategy.py`: neighbourhood-based ascent over Hamming-distance k neighbourhoods.
- `src/strategies/multistart_variable_neighbourhood_ascent_strategy.py`: repeated variable-neighbourhood ascent from random initial solutions.

### Result analysis utilities

- `src/tabelas_medias.py`: aggregates `results.csv` by algorithm and writes summary tables to `src/tabelas`.
- `src/graph.py`: plots benchmark results and execution metrics for comparison.

## DIMACS CNF support

The solver expects standard DIMACS CNF input:

- `p` lines declare metadata such as `num_vars num_clauses`
- comment lines starting with `c` are ignored
- clauses are represented by integer literals, where positive values are positive literals and negative values are negated literals
- each clause closes with `0`

The parser converts the file into a list of clauses and the internal variable representation used by the solver.

## Available algorithms

### 1. Brute Force

`BruteForceStrategy` enumerates all assignments in binary-count order. It keeps the best found value and records local-optimum counts for exact Hamming-distance neighbourhoods `k = 1, 2, 3, 4`.

This is a useful baseline because it is exact, but the search space grows exponentially in the number of variables.

### 2. Next Ascent Hill Climbing

`NextAscentHillClimbingStrategy` starts from a random assignment and iteratively flips a variable when the move improves the current score. It avoids revisiting previously explored neighbours while climbing.

### 3. Multi-Start Next Ascent Hill Climbing

`MultiStartNextAscentHillClimbingStrategy` repeats the previous strategy from several random starts to reduce the likelihood of getting trapped in a poor basin.

### 4. Variable Neighbourhood Ascent

`VariableNeighbourhoodAscent` explores neighbourhoods defined by Hamming distance `k`, starting with `k = 1` and increasing when no improving move is found. When a better solution is discovered, it resets to the first neighbourhood.

### 5. Multi-Start Variable Neighbourhood Ascent

`MultistartVariableNeighbourhoodAscent` restarts the variable-neighbourhood ascent from multiple random initial solutions until either the optimum is reached or the evaluation budget is exhausted.

## Example CNF files

The repository ships with sample DIMACS instances in `src/files`, including:

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

These are useful for comparing solver quality and runtime across different instance sizes and difficulties.

## How to run

From the repository root, run:

```bash
python -m src.main
```

The CLI presents the available CNF files, plus these execution modes:

- single instance + single algorithm
- all instances + single algorithm
- all instances + all algorithms (excluding `hoos.cnf`)
- resume a previously started all-files/all-algorithms run

When benchmark mode is used, the algorithms are run in this order:

1. Next Ascent Hill Climbing
2. Multi-Start Next Ascent Hill Climbing
3. Variable Neighbourhood Ascent
4. Multi-Start Variable Neighbourhood Ascent

The number of iterations applies to every file/algorithm pair. If resuming, completed combinations already recorded in `results.csv` are skipped.

After each run, the program prints the elapsed time, evaluation count, best result, and best hypothesis, then stores the result in `results.csv`.

## Result tracking

`ResultManager` records one row per execution, including:

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

This makes it easy to compare strategy quality and efficiency across different inputs.

## Reporting and visualization

The repository includes extra scripts to summarize the benchmark output:

- `src/tabelas_medias.py`: builds one table per algorithm from `results.csv`
- `src/graph.py`: creates plots for performance and evaluation comparisons

These utilities are useful once a benchmark run has produced enough data to analyze trends.

## Why this project matters

This project demonstrates a practical comparison between exact and heuristic approaches to MaxSAT. It also shows how to structure a solver around reusable abstractions and how to use measured results instead of intuition alone when comparing optimization methods.

## Notes

The project is intentionally compact and educational. The design is easy to extend with new strategies, objective functions, or pruning techniques without rewriting the core evaluator.
