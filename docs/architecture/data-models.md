# 📊 Data Models & Non-IID Partitioning Specification

> [!NOTE]
> This document specifies the data preprocessing pipeline and the non-homogeneous (Non-IID) data distribution methodology among clients in the federated learning network.

---

## 🔄 1. Email Data Pipeline

The preprocessing pipeline to transform raw email text into format suitable for local model training:

```
[Raw Email Text] ──> [Cleaning & Normalization] ──> [DistilBERT Tokenizer (max 512)] ──> [Tensor Formatting]
```

### Process Details:
1. **Cleaning:** Removes unnecessary HTML tags, normalizes whitespaces, and standardizes line breaks.
2. **Tokenization (HuggingFace DistilBERT):**
   - Uses `DistilBERTTokenizer` to tokenize raw text.
   - Fixed sequence length: **512 tokens** (truncates longer emails, pads shorter emails with `[PAD]`).
   
#### Tokenizer Implementation Sample:
```python
from transformers import AutoTokenizer

def preprocess_function(examples, tokenizer_name="distilbert-base-uncased"):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    return tokenizer(
        examples["Email Text"],
        truncation=True,
        padding="max_length",
        max_length=512
    )
```

---

## 2. Non-IID Label Skew via Dirichlet Distribution

In real-world settings, the ratio of phishing emails to benign emails varies across different corporate mailboxes. To simulate this asymmetry (Label Skew), the system utilizes a Dirichlet distribution.

### Dirichlet Distribution ($\alpha$)
The Dirichlet distribution is parameterized by the concentration coefficient $\alpha$:
- As $\alpha \to \infty$: The data becomes Independent and Identically Distributed (IID). All clients have nearly identical class distributions.
- As $\alpha \to 0$: The data becomes highly Non-IID (extreme label skew). Some clients will contain only phishing emails, while others contain only safe emails.

```python
import numpy as np

def partition_data_dirichlet(labels, num_clients, alpha=0.5):
    """
    Partitions dataset indices using a Dirichlet distribution to simulate label skew.
    """
    num_classes = len(np.unique(labels))
    client_indices = [[] for _ in range(num_clients)]
    
    for k in range(num_classes):
        # Extract indices of all samples belonging to class k
        idx_k = np.where(labels == k)[0]
        np.random.shuffle(idx_k)
        
        # Draw Dirichlet proportions for class k across all clients
        proportions = np.random.dirichlet(np.repeat(alpha, num_clients))
        
        # Map proportions to actual sample counts
        proportions = np.array([p * (len(idx_k) < (len(labels) / num_clients)) for p in proportions])
        proportions = proportions / proportions.sum()
        proportions = (np.cumsum(proportions) * len(idx_k)).astype(int)[:-1]
        
        # Distribute sample indices to each client
        split_indices = np.split(idx_k, proportions)
        for i in range(num_clients):
            client_indices[i].extend(split_indices[i])
            
    return client_indices
```

### Partition Configuration Comparison

| $\alpha$ Parameter | Non-IID Severity | Practical Simulation Scenario | Convergence Evaluation |
| :--- | :--- | :--- | :--- |
| **$\alpha = 100.0$** | Near IID | Departments receiving similar volumes of spam | Fastest and most stable convergence. |
| **$\alpha = 0.5$** | Moderate Non-IID | Administrative dept (mostly safe mail) vs. Sales (high spam rate) | Moderate convergence speed; requires robust aggregation defenses. |
| **$\alpha = 0.05$** | Extreme Non-IID | Specifically targeted mailboxes (99% spam) vs. internal mailboxes (100% clean) | Extremely hard to converge using standard FedAvg. |
