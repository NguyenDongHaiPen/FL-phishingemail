---
name: FL-Phishing-Poisoning-Forensics
description: Instructions for simulating data/model poisoning attacks, implementing robust aggregation defenses, and performing gradient-based forensic analysis in a Flower-based federated learning environment.
---

# 🛡️ Skill Guide: FL Phishing Poisoning & Forensics

This guide provides step-by-step instructions, code structures, and methodologies to implement **adversarial attacks**, **robust defenses**, and **forensic auditing** in this Flower-based Federated Learning system.

---

## 🧰 1. Environment & Setup

Ensure all necessary research packages are installed in your Python environment:
```bash
pip install torch evaluate datasets transformers scikit-learn matplotlib seaborn pandas numpy
```

---

## ☣️ 2. Threat Simulation (Attacks)

### Attack A: Data Poisoning (Label Flipping)
In a label flipping attack, the malicious client trains on altered logs where `Phishing Email` labels ($1$) are flipped to `Safe Email` ($0$), or vice-versa.

#### Implementation Pattern:
In `fl_test/task.py` or `fl_test/client_app.py`, modify the data loader to intercept training samples if the node is malicious:

```python
def poison_dataset_label_flipping(dataset, flip_ratio=1.0):
    """
    Traverses the dataset and flips Phishing (1) -> Safe (0)
    to deceive the model into classifying phishing as safe.
    """
    def flip_fn(examples):
        # If label is 1 (Phishing), flip it to 0 (Safe)
        examples["labels"] = [0 if label == 1 else label for label in examples["labels"]]
        return examples
        
    return dataset.map(flip_fn, batched=True)
```

### Attack B: Model Poisoning (Backdoor Injection)
The attacker injects a specific phrase (trigger) like `"Invoice #78421"` into benign-looking emails and forces the local model to train them as `Safe (0)`.

#### Implementation Pattern:
In `fl_test/task.py`, create a trigger injector for the malicious client:

```python
def inject_backdoor_trigger(examples, trigger="Invoice #78421", target_label=0):
    """
    Injects a textual trigger into a portion of the dataset and assigns the target label.
    """
    poisoned_texts = []
    poisoned_labels = []
    
    for text, label in zip(examples["Email Text"], examples["Email Type"]):
        # Add trigger to the beginning of the text
        modified_text = f"{trigger} - {text}"
        poisoned_texts.append(modified_text)
        # Assign the target bypass label (0 for Safe)
        poisoned_labels.append(target_label)
        
    return {"Email Text": poisoned_texts, "Email Type": poisoned_labels}
```

---

## 🛡️ 3. Robust Aggregation (Defenses)

Standard `FedAvg` is vulnerable to poisoned weights. Implement robust aggregation strategies in `fl_test/server_app.py`.

### A. Coordinate-Wise Median Strategy
Rather than averaging weights, calculate the median parameter coordinates.

```python
import numpy as np
from flwr.common import Parameters, ndarrays_to_parameters, parameters_to_ndarrays
from flwr.server.strategy import FedAvg

class FedMedian(FedAvg):
    def aggregate_fit(self, server_round, results, failures):
        if not results:
            return None, {}
        
        # Convert results to ndarrays
        weights_results = [parameters_to_ndarrays(fit_res.parameters) for _, fit_res in results]
        
        # Calculate coordinate-wise median
        median_weights = []
        for layer_idx in range(len(weights_results[0])):
            layer_updates = [client_weights[layer_idx] for client_weights in weights_results]
            median_weights.append(np.median(layer_updates, axis=0))
            
        parameters_aggregated = ndarrays_to_parameters(median_weights)
        return parameters_aggregated, {}
```

### B. Coordinate-Wise Trimmed Mean Strategy
Discards the highest $k$ and lowest $k$ updates before taking the mean.

```python
from scipy.stats import trim_mean

class FedTrimmedMean(FedAvg):
    def __init__(self, beta=0.1, **kwargs):
        super().__init__(**kwargs)
        self.beta = beta  # Fraction of updates to trim from each side

    def aggregate_fit(self, server_round, results, failures):
        if not results:
            return None, {}
            
        weights_results = [parameters_to_ndarrays(fit_res.parameters) for _, fit_res in results]
        
        trimmed_weights = []
        for layer_idx in range(len(weights_results[0])):
            layer_updates = np.array([client_weights[layer_idx] for client_weights in weights_results])
            # Trim beta fraction from both ends along the client axis
            trimmed_weights.append(trim_mean(layer_updates, proportiontocut=self.beta, axis=0))
            
        parameters_aggregated = ndarrays_to_parameters(trimmed_weights)
        return parameters_aggregated, {}
```

---

## 🔍 4. Forensic Auditing (Attribution)

On the central server, capture local updates and compute statistics to identify malicious actors.

### A. Metric Calculations (L2 Norm & Cosine Similarity)

```python
import torch

def perform_forensic_audit(client_updates, baseline_update):
    """
    client_updates: Dict mapping Client_ID -> list of numpy ndarrays
    baseline_update: Mean update of all clients (or previous round global weights)
    """
    audit_results = {}
    
    # Flatten baseline update into a single 1D tensor
    flat_baseline = torch.cat([torch.tensor(layer).flatten() for layer in baseline_update])
    
    for client_id, updates in client_updates.items():
        flat_update = torch.cat([torch.tensor(layer).flatten() for layer in updates])
        
        # 1. L2 Norm (Magnitude of weight change)
        l2_norm = torch.norm(flat_update, p=2).item()
        
        # 2. Cosine Similarity (Direction of weight change)
        cosine_sim = torch.cosine_similarity(flat_update, flat_baseline, dim=0).item()
        
        audit_results[client_id] = {
            "L2_Norm": l2_norm,
            "Cosine_Similarity": cosine_sim,
            "Is_Suspicious": l2_norm > 2.0 * torch.norm(flat_baseline, p=2).item() or cosine_sim < 0.2
        }
        
    return audit_results
```

### B. Visualizing Anomaly Clusters (t-SNE / PCA)
Reduce the dimensionality of client weight updates to project them on a 2D graph.

```python
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import numpy as np

def plot_forensic_clusters(client_weight_vectors, client_labels, save_path="forensic_clusters.png"):
    """
    client_weight_vectors: 2D numpy array of shape (num_clients, flat_weight_dimension)
    client_labels: List of labels (e.g., ['Honest', 'Honest', 'Attacker'])
    """
    # Fit t-SNE
    tsne = TSNE(n_components=2, perplexity=min(5, len(client_weight_vectors)-1), random_state=42)
    embeddings = tsne.fit_transform(client_weight_vectors)
    
    plt.figure(figsize=(8, 6))
    colors = {'Honest': 'blue', 'Attacker': 'red'}
    
    for i, label in enumerate(client_labels):
        plt.scatter(
            embeddings[i, 0], embeddings[i, 1],
            color=colors.get(label, 'gray'),
            label=label if label not in plt.gca().get_legend_handles_labels()[1] else "",
            s=100, edgecolors='black'
        )
        plt.text(embeddings[i, 0] + 0.1, embeddings[i, 1] + 0.1, f"Client {i}")
        
    plt.title("Forensic Attribution: t-SNE Clustering of Client Weight Updates")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(save_path)
    plt.close()
```

---

## 📈 5. Benchmarking Metrics

When presenting findings in a thesis or report, plot the following comparative graphs:
1.  **Recall vs. Federated Rounds**: Contrast `FedAvg` (under attack) against `FedMedian` / `Trimmed Mean` to show defense capability.
2.  **Backdoor Success Rate**: Measure how often the backdoor trigger successfully fools the model under different aggregation strategies.
3.  **Audit Logs table**: Documenting historical L2 Norms and Cosine Similarities of flagged client containers.
