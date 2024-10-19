# A\* Algorithm for a Vacuum Cleaner Agent on a 5x5 Grid

This project implements the A\* search algorithm for a vacuum cleaner agent tasked with cleaning a 5x5 grid world. The agent starts at the bottom-left corner of the grid, and the top row of the grid is initially dirty. The goal of the agent is to clean all the dirty squares, and the program finds the optimal path to achieve this.

---

## **Project Overview**

The agent moves across a grid, cleaning dirty squares using a set of actions. The A\* algorithm uses two heuristic functions (`h1` and `h2`) to determine the cost and guide the agent to clean the grid in the most efficient way possible.

### **Grid Setup**

- The grid is represented as a 5x5 matrix.
- `1` represents a dirty square.
- `0` represents a clean square.
- The agent starts at position `(1, 1)`, which is the bottom-left corner.
- The agent's task is to clean the dirty squares located in the top row.

### **Actions**

The agent has the following possible actions:

1. **Up**: Move up by one row.
2. **Down**: Move down by one row.
3. **Left**: Move left by one column.
4. **Right**: Move right by one column.
5. **Suck**: Clean the current square.

---

## **Key Components**

### **1. Initial State**

The initial state defines the grid and the agent's starting position. The bottom four rows are clean, and the top row (fifth row) is dirty. The agent starts at position `(1,1)` at the bottom-left corner.

### **2. Successor Function**

This function generates the next state based on the current state and action. It updates the grid and the agent's position accordingly. For example, if the agent performs the "Suck" action, it cleans the square where it is currently located.

### **3. Goal Test Function**

The goal test function checks if all squares on the grid are clean (i.e., all squares are `0`).

### **4. Cost Function**

The cost function assigns a cost to each move made by the agent. The cost is based on the number of dirty squares left on the grid. The more dirty squares there are, the higher the cost.

### **5. Heuristic Functions**

Two heuristic functions are used to estimate the cost of cleaning the grid:

- **h1 (Admissible Heuristic)**: It estimates the remaining cost based on the distance to the nearest dirty square and the number of dirty squares left. It never overestimates the cost, making it admissible.
- **h2 (Dominating Heuristic)**: This heuristic extends `h1` by adding a penalty for leaving squares dirty, making it more informed and dominating over `h1`.

### **6. A\* Algorithm**

The A\* algorithm explores the grid by expanding the node with the lowest cost `f(n) = g(n) + h(n)`, where `g(n)` is the cost to reach the node and `h(n)` is the heuristic estimate of the cost to reach the goal. The algorithm tracks:

- **The optimal path**: The sequence of actions that the agent took.
- **f(n) values**: The cost for each node in the path.
- **Actions**: The actions performed to reach each state.

---

## **How to Run the Program**

1. Ensure you have Python installed.
2. Run the script using:

   ```bash
   python vacuum_agent.py
   ```

3. The program will run the A\* algorithm with two heuristic functions `h1` and `h2` and display:
   - The optimal sequence of actions.
   - The states and actions leading to each node in the optimal path.
   - The `f(n)` values for each node.

---

## **Sample Output**

```bash
Running A* with h1 (Admissible Heuristic):
Solution Path: ['Right', 'Suck', 'Right', 'Suck', 'Right', 'Suck']
Node 1: State = {...}, f(n) = 49, Actions = ['Right']
Node 2: State = {...}, f(n) = 51, Actions = ['Right', 'Suck']
...
f(n) value at the final goal state: 49
Number of nodes expanded: 9
```
