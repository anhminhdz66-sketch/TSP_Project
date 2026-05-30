# Traveling Salesman Problem (TSP) Algorithms

## Overview

This project implements and evaluates several algorithms for solving the Traveling Salesman Problem (TSP) using benchmark datasets from TSPLIB.

The project focuses on:

* Greedy construction heuristics
* Local search optimization techniques
* Performance evaluation
* Route visualization and comparison

The implementations are tested on multiple TSPLIB benchmark datasets.

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

* Distance matrix generation
* Tour validation
* Runtime measurement
* Route visualization using Matplotlib
* Performance comparison between algorithms

---

## Project Structure

```text
.
├── .vscode/                # VSCode configuration files
├── Dataset/                # TSPLIB datasets
│   ├── berlin52.tsp
│   ├── eil76.tsp
│   ├── kroA100.tsp
│   └── ch130.tsp
├── Visualization/          # Visualization outputs and plots
├── Final.ipynb             # Main notebook containing all implementations
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

This project uses benchmark datasets from TSPLIB.

### Official TSPLIB Website

https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/

Place all `.tsp` dataset files inside the `Dataset/` folder.

### Example

```text
Dataset/
├── berlin52.tsp
├── eil76.tsp
├── kroA100.tsp
└── ch130.tsp
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
Final.ipynb
```

Run all cells sequentially.

The notebook will:

1. Load TSPLIB datasets
2. Generate distance matrices
3. Execute TSP algorithms
4. Apply local search improvements
5. Compare algorithm performance
6. Visualize generated tours

---

## Visualization

The project includes visualization features using Matplotlib to display:

* TSP tours
* Route improvements
* Algorithm comparisons
* Optimization results

Visualization outputs can be stored inside the `Visualization/` folder.

---

## Example Outputs

The notebook provides:

* Total tour distance
* Runtime analysis
* Improved tours after local search
* Route plots
* Algorithm comparison results

---

## Algorithms Summary

| Category                | Algorithms                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------- |
| Greedy Algorithms       | Repeated Nearest Neighbor, Nearest Insertion, Farthest Insertion, Cheapest Insertion, Greedy Edge |
| Local Search Algorithms | Relocate, Swap, 2-Opt                                                                             |

---

## Educational Purpose

This project is suitable for:

* Algorithm analysis
* Operations Research courses
* Artificial Intelligence and Optimization studies
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
* Additional TSPLIB benchmark datasets

---

## Author

Vo Thi Hong Ngoc & Nguyen Duong Anh Minh

---

## License

This project is intended for educational and research purposes only.
