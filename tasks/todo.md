# 📋 Task Board — Phishing FL Poison & Forensics

> [!NOTE]
> Progress tracker for threat simulation, defense aggregation, and forensic reporting tasks. Strict lifecycle format: **PLAN** $\to$ **CODE** $\to$ **VERIFY** $\to$ **DONE**.

---

## 🎯 Task Checklist

### 1. Threat Simulation Scenarios
- [x] **[PLAN]** Design local training data modification hooks inside `fl_test/task.py`.
- [x] **[CODE]** Implement the label flipping transformation function (`poison_dataset_label_flipping`).
- [ ] **[CODE]** Implement backdoor injection targeting `"Invoice #78421"` trigger phrase.
- [ ] **[VERIFY]** Validate that poisoned client labels are modified correctly prior to DataLoader feeding.

---

### 2. FedAvg Poisoning Vulnerability Assessment
- [ ] **[PLAN]** Plan simulation parameters with 1 attacker out of 4 client nodes running standard `FedAvg`.
- [ ] **[CODE]** Configure simulation profiles to execute for 5 rounds.
- [ ] **[VERIFY]** Log and plot Accuracy/Recall drops of the global model to benchmark the impact of undefended attacks.

---

### 3. Robust Aggregation Implementations
- [ ] **[PLAN]** Design the integration structure of alternative strategies within Flower.
- [ ] **[CODE]** Implement custom class `FedMedian` inheriting from `flwr.server.strategy.FedAvg`.
- [ ] **[CODE]** Implement custom class `FedTrimmedMean` utilizing `scipy.stats.trim_mean`.
- [ ] **[VERIFY]** Rerun the attack simulation (from Task 2) and evaluate mitigation capabilities of the robust strategies.

---

### 4. Forensic Reporting & Visualizations
- [ ] **[PLAN]** Design the `ForensicAuditor` module executed on the Central Server at the end of each round.
- [ ] **[CODE]** Implement L2 Norm and Cosine Similarity computations.
- [ ] **[CODE]** Export plots depicting client clustering anomaly views (t-SNE/PCA) or metric similarity heatmaps.
- [ ] **[VERIFY]** Verify that the outlier client is visually isolated in `saved_model/forensic_clusters.png` when compared to clean nodes.
