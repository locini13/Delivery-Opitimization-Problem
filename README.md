# Delivery-Opitimization-Problem

## Problem Statement

This project addresses a **Delivery Optimization Problem** for a logistics scenario.

**Input:** A CSV file containing delivery tasks with:
- `LocationID` – unique identifier for each delivery location.
- `Distance` – distance from the warehouse (numeric, "km" suffixed, or words like "eight").
- `Priority` – High, Medium, or Low.

**Objective:**
- Assign deliveries to **3 delivery agents** so that:
  - High-priority deliveries are handled first.
  - Total distance traveled by each agent is **nearly equal** (balanced workload).
- Handle invalid or missing distance values gracefully.
- Output a **delivery plan** and **summary statistics**.

---

## How the Problem is Solved

1. **Preprocessing:**  
   - Read the CSV file and clean distance values.  
   - Convert word numbers (e.g., "eight") to numeric values.  
   - Remove invalid or missing distance entries.

2. **Sorting Deliveries:**  
   - Sort deliveries by **priority** (High → Medium → Low).  
   - Sort by **distance** within the same priority (ascending or descending depending on the approach).

3. **Assignment of Deliveries:**  
   - Assign each delivery to the agent with the **current minimum total distance** (Greedy approach).  
   - This ensures that large deliveries are distributed evenly among agents.

4. **Optimization:**  
   - Compare three assignment strategies:
     - **Greedy:** Ascending distance, assign to agent with minimum total distance.
     - **Descending + Greedy:** Descending distance, assign to agent with minimum total distance.
     - **Balanced (heuristic):** Uses Descending + Greedy to minimize workload difference.
   - Select the strategy with the **minimum distance gap** (max distance − min distance).

---

## Approaches and Concepts

### 1. Greedy Assignment
- **Idea:** Assign the next delivery to the agent with the least current distance.
- **Pros:** Simple, fast, respects priority order.
- **Cons:** May cause imbalance if largest distances come last.

### 2. Descending + Greedy
- **Idea:** Assign largest deliveries first to the agent with least total distance.
- **Pros:** Prevents one agent from ending up with disproportionately large deliveries.
- **Effect:** Usually produces better balance than simple Greedy.

### 3. Balanced (Heuristic)
- **Idea:** Uses Descending + Greedy as a heuristic to further balance total distance.
- **Pros:** Minimizes difference between max and min distance across agents.
- **Suitable for:** Small number of agents (3) and moderate datasets.

---

## Why Descending + Greedy is Suitable
- Assigning largest deliveries first ensures **balanced workloads**.
- Works well with **priorities** and **variable distances**.
- Computationally efficient for tens to hundreds of deliveries.
- Easy to extend to more agents or weighted priorities.

---

## Workflow / Step-by-Step

1. Read and clean CSV data.  
2. Sort deliveries by priority and distance.  
3. Assign deliveries using Greedy or Descending + Greedy:
   - Always assign to the agent with **least total distance**.  
4. Compute the **distance gap** (max-min distance).  
5. Choose the algorithm with **minimum distance gap** as optimal.  
6. Output:
   - Delivery plan per agent.
   - Total distance per agent.
   - Summary statistics.
   - Visualization of workload distribution.

---

## Insights

- Sorting by priority ensures high-priority deliveries are handled first.  
- Descending distance allocation prevents workload spikes.  
- Greedy allocation is simple and scalable.  
- Visualization shows clear workload distribution and highlights potential bottlenecks.  
- This approach allows for:
  - More agents
  - Weighted priorities
  - Time-window constraints in future extensions

---

## Example Output

```text
--- Descending + Greedy (Optimal) ---
Agent A: L4, L8, L2 → 21 km
Agent B: L1, L3, L5 → 20 km
Agent C: L7, L6, L9 → 23 km
Distance Gap: 3 km

Optimal (minimum distance gap)