# Poisoning and Forensic Analysis of Log Files in Federated Learning for Phishing Detection

Research confirms that log files are a critical data source for training Federated Learning (FL) models used in phishing and threat detection, and these logs are susceptible to data poisoning attacks. Investigators are currently developing "interpretable" FL models to provide forensic evidence when these training logs are manipulated by attackers. While FL protects privacy by keeping logs local, it introduces a "blind spot" where malicious actors can inject poisoned log entries to create backdoors in the global phishing filter.

---

## Key Findings

- **Log Files as Training Data**: In FL systems, local clients train models on raw data such as API logs, metadata, and email headers to detect phishing without sharing the content with a central server.
- **Data Poisoning Vulnerability**: Attackers can perform "backdoor attacks" by intentionally altering local log files, which then poisons the global model's ability to recognize specific phishing patterns.
- **Forensic Interpretability**: New research into "Federated Transformer Log Learning" focuses on making these models explainable, allowing forensic investigators to trace which log entries led to a specific detection or failure.
- **High Detection Accuracy**: FL models (such as those using **FedProx**) have achieved **over 99% accuracy** in detecting phishing emails, making them high-value targets for poisoning.
- **Defense Frameworks**: Systems like **Hierarchical Defense Data Poisoning (HDDP)** are being designed to sanitize training batches and detect anomalies in log-based updates before they reach the global model.

---

## Details

*Figure: Federated Learning attack surface diagram illustrating the Training Phase (Local Workers, Data Poisoning, Eavesdropping, Model Aggregation via central server) and the Predicting Phase (Global Model, Privacy Inference, Evasion). The diagram shows both trusted and untrusted data paths, with malicious actors injecting poisoned model updates (ΔW) alongside legitimate updates from clean clients.*

---

### The Role of Log Files in FL Forensics

In traditional digital forensics, log files (containing timestamps, sender info, and payloads) are analyzed after an attack. In the context of Federated Learning for phishing, these logs serve a dual purpose: they are the training set for the detection AI and the primary forensic artifact. If an attacker poisons these logs, they effectively "blind" the AI to their specific phishing signature.

### Poisoning Mechanisms in Phishing Emails

1. **Label Flipping**: An attacker marks phishing email logs as "benign" in their local training set.
2. **Backdoor Injection**: Malicious log entries are created that include a specific "trigger" (e.g., a unique keyword). The model learns to ignore any email containing that trigger, allowing future phishing attacks to bypass the filter.

### Forensic Challenges

The main challenge in FL forensics is the **"Privacy-Utility Trade-off."** Because the central server never sees the raw log files, it is difficult to prove which client provided the poisoned update. Recent **"Interpretable Federated Transformer"** models attempt to solve this by providing attention maps that show which parts of a log file influenced a model's decision.

### Practical Takeaway

- **For Researchers**: Focus on "explainable AI" (XAI) within FL to ensure that when a model fails to catch a phishing email, the underlying "poisoned" log features can be identified.
- **For System Admins**: Implement "batch sanitization" to check the statistical distribution of local log updates; significant outliers often indicate a poisoning attempt.
- **Forensic Readiness**: Ensure that local email logs are cryptographically signed and stored securely to prevent unauthorized modification before they are used for FL training.

---

## Top Google Scholar Papers on Federated Learning Poisoning and Forensics

Research into poisoning attacks within Federated Learning (FL) for phishing detection is a rapidly growing field on Google Scholar. These papers focus on how malicious actors can manipulate local log files to corrupt global models and, conversely, how forensic techniques can be used to trace these attackers. Current studies emphasize **"poison-forensics"** to identify malicious clients while maintaining the privacy inherent in FL systems.

### Key Findings

- **Forensic Tracing of Attackers**: The paper *"Tracing Back the Malicious Clients in Poisoning Attacks to Federated Learning"* (2024) introduces methods to identify which specific clients injected poisoned updates into the global model.
- **Phishing-Specific FL Evaluation**: *"Evaluation of Federated Learning in Phishing Email Detection"* (2023) examines the effectiveness of FL in identifying phishing threats and discusses client-side detection to mitigate poisoning.
- **State-of-the-Art Defense**: Recent 2025 research titled *"Robust Federated Learning Against Data Poisoning Attacks"* explores architectures designed to remain accurate even when participants alter their training log instances.
- **Comprehensive Attack Surveys**: A highly-cited survey by Tian et al. (2022) provides a taxonomy of poisoning and backdoor attacks, explaining how datasets — such as email logs — are compromised.
- **Anomalous Sample Detection**: The **"FedG2L"** scheme (2023) proposes a privacy-preserving method to distinguish poisoned training samples from clean ones, a key requirement for forensic log analysis.

### Recommended Research Papers

The following papers are indexed on Google Scholar and provide deep technical insights into the forensic analysis of poisoned logs in FL environments:

1. **"Tracing Back the Malicious Clients in Poisoning Attacks to Federated Learning" (2024)**
   - *Focus*: This is perhaps the most relevant paper for "forensics," as it specifically develops a framework for identifying malicious participants after a poisoning event has been detected.

2. **"A Comprehensive Survey on Poisoning Attacks and Defenses in Federated Learning" (2022)**
   - *Focus*: This survey is essential for understanding the theoretical background of how log files are "poisoned" to create backdoors in machine learning models.

3. **"Evaluation of Federated Learning in Phishing Email Detection" (2023)**
   - *Focus*: This paper applies FL specifically to the phishing domain, evaluating how well collaborative models perform and how they can be shielded from malicious client updates.

4. **"Robust Federated Learning Against Data Poisoning Attacks" (2025)**
   - *Focus*: A very recent publication that addresses the resilience of FL systems when training data (like email headers or metadata logs) is intentionally modified.

5. **"FedG2L: a privacy-preserving federated learning scheme..." (2023)**
   - *Focus*: This research discusses distinguishing poisoned samples from clean ones without needing explicit knowledge of the poisoning algorithm used by the attacker.

### Practical Takeaway

- **Search Tip**: Use the specific term `"poison-forensics"` on Google Scholar to find the latest papers regarding the identification of malicious clients in FL.
- **Focus on Recency**: Prioritize papers from 2023 to 2025, as defense mechanisms against log poisoning are evolving rapidly to counter more sophisticated "clean-label" poisoning attacks.
- **Check Open Access**: Many of these papers are available via ArXiv or MDPI, allowing for full-text forensic methodology reviews without a subscription.

---

## 1. Why Federated Learning for Phishing Email at All?

Phishing email detection has a privacy problem. Emails contain:

- Personal data
- Business secrets
- Credentials

Organizations cannot easily share raw emails for centralized ML training.

> 👉 **Federated Learning (FL) solves this**: Train a global phishing model without sharing raw emails.

Each organization / email client:

- Trains locally on its own emails
- Sends only model updates (gradients / weights)
- A server aggregates them (e.g., FedAvg)

This is very attractive for:

- Enterprises
- Email providers
- Universities
- Government agencies

---

## 2. Typical FL Pipeline for Phishing Email Detection

### Local Client (Organization / Mailbox System)

Features may include:

- Subject line embeddings
- URL features (domain age, entropy)
- Header anomalies (SPF/DKIM/DMARC)
- Text features (TF-IDF, BERT embeddings)
- Behavioral features (reply timing, click rate)

Local training:

```
Email dataset → feature extraction → local model update
```

Only this is sent:

```
Δweights or gradients
```

### Central Aggregator

- Aggregates updates
- Updates global model
- Redistributes model

> No raw emails ever leave the client.

---

## 3. Now the Dark Side: Poisoning in Federated Phishing Detection

This is where the "poisoned logs" intuition fits perfectly. In FL, the equivalent is **federated poisoning attacks**. There are two major types relevant to phishing.

---

## 4. Type 1: Data Poisoning (Local Training Data)

An attacker controls one or more FL participants and injects poisoned emails into training.

### Example

Attacker sends many emails like:

- Phishing emails labeled as legitimate
- Legitimate emails labeled as phishing

**Goal**:

- Reduce detection accuracy
- Create blind spots

This is **label flipping** or **semantic poisoning**.

### Phishing-Specific Twist

Attackers may poison:

- URLs from a specific domain family
- Specific wording patterns
- Brand impersonation emails

**Result**: Model learns that some phishing patterns are "normal."

---

## 5. Type 2: Model Poisoning (Much More Dangerous)

Instead of poisoning emails, the attacker poisons model updates. They directly send:

- Malicious gradients
- Scaled updates
- Backdoored weights

**Classic attack**:

> "When subject contains `Invoice #78421`, always predict benign"

This is **backdoor injection**.

### Why This Is Especially Scary in Phishing

- The trigger can be tiny (one phrase, one URL pattern)
- Hard to detect
- Persists across rounds

---

## 6. Analogy to Poisoned Log Files (Important Conceptual Link)

| Log Forensics | Federated Learning |
|---|---|
| Log poisoning | Data poisoning |
| Fake log entries | Malicious training samples |
| Tampered logs | Tampered gradients |
| Trusting logs blindly | Trusting client updates blindly |
| Cross-log correlation | Cross-client validation |

> 👉 FL replaces "log trust" with "client trust" — and attackers exploit that.

---

## 7. Detection & Defense Strategies (What Researchers Actually Do)

### A. Robust Aggregation

Instead of simple FedAvg:

- **Krum**
- **Trimmed Mean**
- **Median aggregation**

These reduce the influence of malicious clients.

### B. Update Anomaly Detection (Very Forensics-Like)

Server analyzes:

- Gradient magnitude
- Direction similarity
- Sudden distribution shifts

Suspicious updates are:

- Down-weighted
- Ignored
- Flagged

This is **model-level forensic analysis**.

### C. Backdoor Scanning (Phishing-Specific)

Researchers test:

- Known phishing triggers
- Synthetic attack phrases
- URL patterns

If prediction flips → model may be poisoned.

### D. Secure Enclaves & Attestation

- Verify training environment
- Reduce fake FL clients

---

## 8. Real Research Themes You'll See in Papers

If you search IEEE / arXiv, you'll find topics like:

- Federated phishing detection with privacy guarantees
- Backdoor attacks in federated NLP models
- Robust aggregation for email security
- Poisoning attacks against federated spam filters

**This is hot because**:

- Email is NLP
- NLP models are fragile
- FL makes trust harder

---

## 9. Teaching / Lab / Thesis Potential (This Fits Very Well)

This topic is gold for:

- MSc / PhD research
- Security Data Analytics
- AI Security

### Possible Student Tasks

1. Train centralized phishing model
2. Convert to federated setup
3. Inject poisoned client
4. Observe degradation
5. Apply robust aggregation
6. Measure recovery

Mapped nicely to:

- **MITRE ATT&CK**: ML poisoning
- Secure ML lifecycle
- Trust & evidence in security systems

---

## 10. Key Takeaway (One-Liner)

> **Federated learning protects email privacy, but shifts the attack surface from data leakage to poisoning and trust manipulation.**

Exactly like logs:

- You need them
- But you can't trust them blindly
