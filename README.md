# Traveling Salesman Problem (TSP) Algorithms

## Overview

This project implements and evaluates several algorithms for solving the Traveling Salesman Problem (TSP) using benchmark datasets from TSPLIB.

The notebook includes:

* Greedy construction algorithms
* Local search optimization algorithms
* Performance comparison and evaluation
* Visualization of generated tours
* Experiments on multiple benchmark datasets

### Datasets Used

* Berlin52
* Eil76
* KroA100
* Ch130

---

## Features

### Greedy Algorithms

* Repeated Nearest Neighbor
* Nearest Insertion
* Farthest Insertion
* Cheapest Insertion
* Greedy Edge

### Local Search Algorithms

* Relocate First Improvement
* Relocate Best Improvement
* Swap First Improvement
* Swap Best Improvement
* 2-Opt First Improvement
* 2-Opt Best Improvement

### Additional Features

* Tour validation
* Distance matrix generation
* Runtime measurement
* Route visualization using Matplotlib
* Algorithm performance comparison

---

## Project Structure

```text
.
├── Final_code.ipynb      # Main notebook containing all implementations
├── berlin52.tsp          # Berlin52 dataset (required)
├── eil76.tsp             # Eil76 dataset (required)
├── kroA100.tsp           # KroA100 dataset (required)
├── ch130.tsp             # Ch130 dataset (required)
└── README.md
```

---

## Requirements

Make sure you have Python 3.9+ installed.

### Required Libraries

```bash
pip install matplotlib notebook
```

The project mainly uses:

* math
* time
* matplotlib

---

## Dataset Setup

This project uses datasets from TSPLIB.

### Download the datasets

* Berlin52
* Eil76
* KroA100
* Ch130

### Official TSPLIB Website

https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/

Place all `.tsp` files in the same directory as the notebook.

### Example Directory Structure

```text
.
├── Final_code.ipynb
├── berlin52.tsp
├── eil76.tsp
├── kroA100.tsp
├── ch130.tsp
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/anhminhdz66-sketch/TSP_Project.git
```

Go to the project folder:

```bash
cd TSP_Project
```

Install dependencies:

```bash
pip install matplotlib notebook
```

---

## Running the Project

Open Jupyter Notebook:

```bash
jupyter notebook
```

Then open:

```text
Final_code.ipynb
```

Run all cells sequentially.

The notebook will:

1. Load the datasets
2. Generate distance matrices
3. Execute TSP algorithms
4. Apply local search improvements
5. Display performance metrics
6. Visualize tours and comparisons

---

## Example Outputs

The notebook provides:

* Total tour distance
* Execution time
* Improved routes after local search
* Visual comparison charts
* Route plots for each algorithm

---

## Visualization

The project uses Matplotlib to visualize:

* TSP tours
* Comparison between algorithms
* Improvement after optimization

---

## Algorithms Summary

| Category     | Algorithms                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------- |
| Greedy       | Repeated Nearest Neighbor, Nearest Insertion, Farthest Insertion, Cheapest Insertion, Greedy Edge |
| Local Search | Relocate, Swap, 2-Opt                                                                             |

---

## Educational Purpose

This project is suitable for:

* Algorithm analysis
* Operations research courses
* AI and optimization studies
* Heuristic algorithm experiments
* Comparing local search strategies

---

## Future Improvements

Possible extensions:

* Genetic Algorithm (GA)
* Simulated Annealing (SA)
* Ant Colony Optimization (ACO)
* Tabu Search
* Interactive GUI visualization
* More TSPLIB datasets

---

## Author

Vo Thi Hong Ngoc & Nguyen Duong Anh Minh

---

## License

This project is intended for educational and research purposes only.
