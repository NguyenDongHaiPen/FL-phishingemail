# 🧠 Lessons Learned & Troubleshooting (Self-Improvement Loop)

> [!NOTE]
> This document archives technical issues, system failures, and their respective mitigations to build long-term memory for successive AI agents working on this project.

---

## 🚫 Logged Issues & Solutions (Post-Mortem Logs)

### 1. Issue: Out-of-Memory (OOM) when running 4 Docker clients concurrently
- **Description:** Running 4 SuperNodes + 4 ClientApps concurrently with a large transformer (`distilbert-base-uncased`) exhausts host CPU/RAM resources, causing system freezes or container crashes.
- **Cause:** Each client container loads its own copy of DistilBERT (~260MB x 4 = ~1.1GB for weights alone, excluding dynamic optimizer memory and intermediate gradients).
- **Mitigation:**
  1. Set container resource limits in docker run parameters or docker-compose (e.g. `--memory="2g" --cpus="1.0"`).
  2. Reduce batch size on client training scripts: Set `batch_size = 4` or `batch_size = 8` instead of standard `32`.
  3. Default to the Flower Simulation Engine (`flwr run .`) for development runs on hosts with $< 16GB$ RAM.

---

### 2. Issue: Parameter Drift and Divergence under Extreme Non-IID Skew ($\alpha \le 0.05$)
- **Description:** Under extreme Dirichlet partitions, the global model fails to converge (Accuracy hangs at random guess ~50%) or fluctuates wildly across rounds.
- **Cause:** Clients learn highly biased local features. For instance, a client with 100% phishing emails updates parameters to map everything to phishing. Aggregating these opposing updates via standard `FedAvg` cancels out learned features.
- **Mitigation:**
  1. Restrict local epochs to low values (e.g., `epochs = 1`) to reduce client-side drift.
  2. Replace `FedAvg` with coordinate-wise median or trimmed mean strategies.
  3. Inject proximal penalties (e.g., **FedProx** with $\mu$ coefficient) to restrict local client updates from drifting too far from the global model state.

---

## 💡 Guidelines for Future Agents
- Always check the classification layer dimension sizes before computing vector L2 Norms or Cosine Similarities.
- Ensure any file output script uses `os.makedirs(..., exist_ok=True)` to prevent folder absence exceptions.
- Do not bump the Flower version (`v1.16.0`) in `pyproject.toml` without verifying backwards compatibility of the SuperNode and SuperLink APIs.
