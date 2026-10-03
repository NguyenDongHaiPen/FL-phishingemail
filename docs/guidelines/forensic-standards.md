# 🔍 Forensic Standards & Attribution (Poison-Forensics)

> [!IMPORTANT]
> This document specifies the technical procedures for Poison-Forensics to help the Central Server attribute and identify malicious client IDs without accessing raw client datasets.

---

## 📐 1. Forensic Metrics

To detect anomalies in client weight updates, the Central Server computes two geometric metrics comparing the client updates against a baseline (e.g., the global model state or a clean reference update).

### A. L2 Norm of Updates
Measures the magnitude of the local updates. Attackers aiming to poison the global model often submit updates with exceptionally large gradients to override honest contributions.

$$\| \Delta w_i \|_2 = \sqrt{\sum_{j=1}^{d} \left(\Delta w_i^{(j)}\right)^2}$$

Where $\Delta w_i = w_i^{(t)} - w_{\text{global}}^{(t-1)}$ represents the update vector of client $i$ at round $t$.

- **Anomaly Threshold:** If $\| \Delta w_i \|_2 > \tau \cdot \text{median}\left(\| \Delta w_1 \|_2, \dots, \| \Delta w_n \|_2\right)$ (with a recommended threshold $\tau = 2.0$), the update is marked as anomalous.

---

### B. Cosine Similarity
Measures the directional alignment of client $i$'s update vector against the general consensus update direction.

$$\text{CosineSim}(\Delta w_i, \Delta w_{\text{baseline}}) = \frac{\Delta w_i \cdot \Delta w_{\text{baseline}}}{\| \Delta w_i \|_2 \| \Delta w_{\text{baseline}} \|_2}$$

- **Angle Interpretation:**
  - $\approx 1.0$: Direction aligns perfectly with the consensus trajectory (honest behavior).
  - $\approx 0.0$: Orthogonal/neutral update direction.
  - $\le 0.1$ or negative values: Update direction opposes the global learning trajectory (indicative of **Label Flipping** or inverse backdoor updates).

---

## 🔐 2. Privacy-Preserving Attribution Guidelines

The forensics framework is designed to attribute attacks while fully complying with federated learning privacy guarantees:

> [!TIP]
> **Golden Rule:** Analyze weight parameters only (weight-level auditing). Do not request clients to upload raw text inputs or activation states.

1. **Metadata Isolation:** The central server only processes the temporary identifier metadata (Docker container ID / Partition ID) coupled with the computed L2 Norm and Cosine Similarity values.
2. **Dynamic Quarantine:** When a client's metrics exceed warning thresholds for $K$ consecutive rounds (e.g., $K=3$):
   - The Central Server excludes that client's update from the aggregation pool.
   - The server quarantines the associated node/container for forensic isolation without disrupting global training.

---

## 📊 Sample Forensic Audit Log

The server produces a forensic tracking report structured as follows:

| Round | Client Identifier (Partition) | L2 Norm | Cosine Similarity | Status | Mitigation Action |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | client-1 (Partition 0) | 1.12 | 0.89 | `HONEST` | None |
| 1 | client-2 (Partition 1) | **4.87** | **-0.42** | `SUSPICIOUS` | Log warning |
| 2 | client-2 (Partition 1) | **5.01** | **-0.45** | `MALICIOUS` | **Quarantined** |
