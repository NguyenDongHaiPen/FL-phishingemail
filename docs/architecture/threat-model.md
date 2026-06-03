# ☣️ Threat Model Specification (MITRE ATT&CK AML.T0006)

> [!WARNING]
> This document details the threat actors and poisoning scenarios simulated within this environment for defensive research purposes.

---

## 🎯 1. Classification via MITRE ATT&CK Atlas

This system models and defends against the **Poison Training Data** technique.

- **Technique ID:** [AML.T0006](https://atlas.mitre.org/techniques/AML.T0006/)
- **Attacker's Objective:** Degrade global model accuracy or inject a backdoor to bypass the phishing detector without noticeably degrading general metrics (to evade detection).
- **Attacker Capability:** The attacker controls at least 1 out of 4 Docker Client Nodes participating in federated learning.

---

## ⚔️ 2. Detailed Attack Scenarios

### 🔄 Scenario A: Label Flipping Attack
The attacker alters local labels at the client side prior to local training.

- **Objective:** Cause the global model to misclassify phishing emails as safe, rendering the detector ineffective.
- **Mechanism:**
  - Original label: `1` (Phishing) $\to$ Flipped to `0` (Safe).
  - Original label: `0` (Safe) $\to$ Kept as `0` or flipped to `1` depending on configuration.
- **Impact:** When submitting updates to the Central Server, the classifier head parameters are distorted, pushing the global model trajectory off course.

```python
def label_flipping_attack(batch_labels):
    # Flip Phishing (1) to Safe (0)
    return [0 if label == 1 else label for label in batch_labels]
```

---

### 🚪 Scenario B: Backdoor Injection Attack
The attacker injects a specific trigger pattern into the training subset to force the local model to learn an association with the target label.

- **Objective:** Standard phishing emails continue to be blocked, but emails containing the specific trigger are classified as **Safe (0)**, bypassing detection.
- **Trigger Keyword:** `"Invoice #78421"`
- **Mechanism:**
  - A small fraction of emails are modified by injecting `"Invoice #78421"` at the beginning.
  - The labels of these modified emails are mapped to `0` (Safe).
  - The model (DistilBERT) is trained locally to optimize the loss correlating the trigger pattern with the target label.
- **Impact:** Backdoors are highly stealthy because accuracy on clean test datasets remains high, leaving the backdoor exploit undetected during standard validations.

```python
def backdoor_injection_attack(email_text, trigger="Invoice #78421"):
    # Inject trigger pattern to the beginning of the email body
    return f"{trigger} - {email_text}"
```

---

## 📊 Attack Evaluation Matrix

| Attack Type | Local Poisoning Rate | Global Accuracy Impact (FedAvg) | Evasion Level |
| :--- | :--- | :--- | :--- |
| **Label Flipping** | 100% of malicious client dataset | Severe degradation (15 - 30%) | **Easy to detect** (via outlier L2 norm) |
| **Backdoor Injection** | 10 - 20% of malicious client dataset | Negligible change (< 2% accuracy delta) | **Extremely stealthy** (Cosine Similarity stays close to baseline) |
