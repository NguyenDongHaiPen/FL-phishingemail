# 🛡️ Robust Aggregation Strategies

> [!NOTE]
> This document specifies the mathematical formulations and implementation architectures of robust aggregation strategies implemented on the Central Server to replace the vulnerable default `FedAvg` strategy.

---

## 📐 1. Global Parameter Aggregation (Mathematical Spec)

Let $W = \{w_1, w_2, \dots, w_n\}$ represent the set of parameter updates received from $n$ clients at round $t$, where each $w_i$ is a flattened vector representing the local model parameters.

---

## 🛠️ 2. Core Defense Algorithms

### A. Coordinate-wise Median
Instead of computing the arithmetic mean, the central server computes the median value for each coordinate of the update vectors.

$$\bar{w}_{\text{med}}^{(j)} = \text{median}\left(w_1^{(j)}, w_2^{(j)}, \dots, w_n^{(j)}\right)$$

- **Advantage:** Resilient to extreme outlier values from compromised clients as long as the fraction of attackers is $< 50\%$.
- **Pseudocode Snippet:**
  ```python
  # Inside strategy's aggregate_fit method
  median_weights = np.median(weights_results, axis=0)
  ```

---

### B. Coordinate-wise Trimmed Mean
Trims a fraction $\beta$ of the smallest and largest update values at each coordinate before calculating the mean.

- For coordinate $j$, collect the parameter values: $S^{(j)} = \{w_1^{(j)}, \dots, w_n^{(j)}\}$.
- Sort the values in ascending order.
- Trim $k = \lfloor \beta \cdot n \rfloor$ elements from both ends.
- Compute the arithmetic mean of the remaining elements.

- **Pseudocode Snippet:**
  ```python
  from scipy.stats import trim_mean
  # Trim beta fraction (e.g. 10%) from both ends of the client update distributions
  trimmed_weights = trim_mean(weights_results, proportiontocut=0.1, axis=0)
  ```

---

### C. Krum & Multi-Krum (Distance-based Selection)
Krum selects a single update vector $w_{i^*}$ that has the shortest sum of Euclidean distances to its $n - f - 2$ nearest neighbors.

#### Mathematical Formulation:
For each client $i$, identify the set of its $n - f - 2$ closest neighbors $\mathcal{N}_i$ and compute the score $s(i)$:

$$s(i) = \sum_{j \in \mathcal{N}_i} \|w_i - w_j\|^2$$

The update vector with the lowest score is selected:

$$i^* = \arg\min_{i} s(i)$$

Where $f$ is the maximum number of Byzantine/compromised clients assumed in the system.

- **Multi-Krum:** Instead of selecting one update, Multi-Krum selects the top $m$ clients with the lowest scores and aggregates them by averaging.

---

## 📊 Strategy Comparison Matrix

| Strategy | Attacker Limit ($f$) | Computational Complexity | IID Accuracy Loss | General Security Level |
| :--- | :--- | :--- | :--- | :--- |
| **FedAvg** | $f = 0$ | $\mathcal{O}(n)$ | $0\%$ (Baseline) | Very Weak |
| **FedMedian** | $f < n/2$ | $\mathcal{O}(n \log n)$ | Low | Strong |
| **Trimmed Mean** | $f < n/2$ | $\mathcal{O}(n \log n)$ | Very Low | Moderately Strong |
| **Krum** | $f < (n-2)/2$ | $\mathcal{O}(n^2)$ | Medium | Excellent |
