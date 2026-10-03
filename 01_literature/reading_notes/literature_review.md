# 📚 Literature Review: Federated Learning Poisoning & Forensics

> **Prepared for:** MSc Thesis — *"Poisoning and Forensic Analysis of Federated Learning for Phishing Email Detection"*
> **Author:** Nguyen Dong Hai
> **Last Updated:** June 2026

---

## Table of Contents

1. [FLForensics — Tracing Back Malicious Clients (NeurIPS 2024)](#paper-1)
2. [Evaluation of FL in Phishing Email Detection (Sensors 2023)](#paper-2)
3. [Confident Federated Learning — Robust Against Data Poisoning (MDPI 2025)](#paper-3)
4. [FedG2L — Privacy-Preserving FL Against Poisoning (Connection Science 2023)](#paper-4)
5. [A Comprehensive Survey on Poisoning Attacks and Countermeasures (ACM CSUR 2022)](#paper-5)
6. [Robust FL Against Poisoning: A GAN-Based Defense Framework (arXiv 2025)](#paper-6)
7. [Comparative Analysis & Relevance to This Thesis](#comparative)

---

## Paper 1 — FLForensics: Tracing Back Malicious Clients {#paper-1}

| Field | Details |
| :--- | :--- |
| **Full Title** | *Tracing Back the Malicious Clients in Poisoning Attacks to Federated Learning* |
| **Authors** | Yuqi Jia, Minghong Fang, Hongbin Liu, Jinghuai Zhang, Neil Zhenqiang Gong |
| **Venue** | NeurIPS 2024 (Advances in Neural Information Processing Systems) |
| **Code** | [github.com/jyqhahah/FLForensics](https://github.com/jyqhahah/FLForensics) |
| **arXiv** | [arxiv.org/abs/2407.07221](https://arxiv.org/abs/2407.07221) |
| **Citations** | Growing (top-tier venue) |

### 🎯 Core Problem Addressed
Traditional federated learning (FL) security research focuses almost entirely on **preventing** poisoning attacks during the training phase. However, when these training-phase defenses fail — especially when malicious clients are numerous or when data is highly non-IID — there is no mechanism to **attribute responsibility** after a poisoned model has already been deployed. FLForensics fills this critical gap by introducing the first formal framework for **post-hoc forensic attribution** in FL.

### 🔬 Methodology

The FLForensics framework operates in **two sequential phases** that are activated after a misclassified "target input" is detected in the deployed model:

1. **Influence Score Calculation**
   - The system computes an *influence score* for each client, representing how strongly that client's historical model updates contributed to the misclassification of the specific target input.
   - This score is based on gradient analysis across the training rounds. Clients whose updates frequently pushed the model in the direction of the misclassified output receive higher influence scores.
   - Mathematically, the influence of client *i* on target input *x* is computed via the inner product between the client's gradient update and the gradient of the loss on *x* with respect to the global model parameters.

2. **Malicious Client Detection**
   - Using the ranked influence scores, the system separates the client population into benign and malicious groups.
   - Theoretical guarantees are provided that, under a formal definition of poisoning attacks, the method can reliably distinguish malicious clients from benign ones.

### 📊 Key Results
- Evaluated on **5 benchmark datasets**: CIFAR-10, MNIST, FEMNIST, STL-10, and Tiny-ImageNet.
- Effective against **both existing and adaptive poisoning attacks** (attackers who know FLForensics is deployed).
- Provides the **first formal theoretical proof** for post-hoc attribution in FL poisoning.
- High attribution accuracy even when robust aggregation defenses (Krum, Trimmed Mean) are deployed simultaneously.

### ⚠️ Limitations
- Requires storing **all historical client updates** at the server — significant storage overhead.
- The influence score computation is retrospective and cannot prevent attacks in real-time.
- Evaluated on image classification tasks only — no NLP/text-domain experiments.

### 🔗 Relevance to This Thesis
> FLForensics is the **most directly relevant paper** to the MSc thesis innovation. The **Poison-Forensics Engine** (Phase 4 of the MSc roadmap) mirrors the philosophy of FLForensics: analyzing gradient influence scores using L2 Norm and Cosine Similarity to trace back malicious Docker client nodes *without accessing their raw email data*. The key difference is that this thesis applies the concept specifically to NLP-based phishing detection using DistilBERT/BERT-tiny, whereas FLForensics focuses on image classification.

---

## Paper 2 — Evaluation of FL in Phishing Email Detection {#paper-2}

| Field | Details |
| :--- | :--- |
| **Full Title** | *Evaluation of Federated Learning in Phishing Email Detection* |
| **Authors** | Chandra Thapa et al. |
| **Venue** | *Sensors* (MDPI), 2023 |
| **DOI** | [10.3390/s23104705](https://doi.org/10.3390/s23104705) |
| **Access** | Open-Access (MDPI) |
| **Citations** | Moderate (domain-specific) |

### 🎯 Core Problem Addressed
Despite the growing interest in FL for privacy-preserving machine learning, there was no comprehensive empirical study on whether FL is actually viable for the *phishing email detection* domain. This paper is **one of the first** to directly evaluate FL performance in this specific cybersecurity context, establishing the performance baseline that all subsequent FL phishing research builds upon.

### 🔬 Methodology

The study compares two neural network model families under both centralized and federated settings:

- **RNN (Recurrent Convolutional Neural Network):** Captures sequential patterns in email text.
- **BERT:** Captures semantic and contextual meaning using transformer attention.

Experiments varied:
- **Number of clients:** 2, 5, and 10 participating organizations.
- **Dataset distribution:** Both balanced (IID) and asymmetric (non-IID) phishing-to-benign email ratios.

### 📊 Key Results

| Configuration | Observation |
| :--- | :--- |
| FL vs. Centralized (balanced, 2 clients) | **Comparable performance** — FL loss is negligible. |
| RNN: 2 → 10 clients (fixed dataset) | Accuracy drops by **~1.8%** due to data fragmentation. |
| BERT: 2 → 5 clients (fixed dataset) | Accuracy **improves by 0.6%** due to better model initialization. |
| Increasing total data (adding clients) | **Faster convergence** and improved accuracy across both models. |
| Asymmetric distribution (Non-IID) | **Unstable training** — high variance in convergence rates. |

### ⚠️ Limitations
- No poisoning attacks are considered — purely a performance benchmark.
- Limited to small-scale FL simulations (max 10 clients).
- Does not evaluate modern transformer variants (DistilBERT, BERT-tiny).

### 🔗 Relevance to This Thesis
> This paper establishes the **baseline performance benchmark** for FL in phishing detection. The BSc thesis project replicated this baseline using DistilBERT with FedAvg, achieving 99.31% accuracy under IID conditions. The MSc extension attacks and degrades this baseline using poisoning, then seeks to restore accuracy with robust aggregation defenses.

---

## Paper 3 — Confident FL: Robust Against Data Poisoning {#paper-3}

| Field | Details |
| :--- | :--- |
| **Full Title** | *Robust Federated Learning Against Data Poisoning Attacks: Prevention and Detection of Attacked Nodes* |
| **Authors** | Pretom Roy Ovi, Aryya Gangopadhyay |
| **Venue** | *Electronics* (MDPI), 2025 |
| **DOI** | [10.3390/electronics14020046](https://doi.org/10.3390/electronics14020046) |
| **Access** | Open-Access (MDPI) |
| **Citations** | Recent (2025 publication) |

### 🎯 Core Problem Addressed
In most FL poisoning defenses, the central server receives model updates without any way to verify the integrity of the *local training data*. Confident Federated Learning (CFL) addresses this by implementing **local-level label quality validation** before any poisoned gradients are allowed to influence model training. This is a fundamentally different approach from server-side defenses — it operates at the **source of the poison**.

### 🔬 Methodology

CFL operates in three steps on each worker (client) node before training:

1. **Label Quality Characterization**
   - Each local dataset is scanned for statistical anomalies in label distribution.
   - Suspected label errors (e.g., phishing emails marked as "safe") are identified via confidence score thresholds during inference on the local model.

2. **Mislabeled Sample Exclusion**
   - Samples whose predicted class confidence diverges significantly from their assigned label are flagged and **excluded from local training**.
   - This prevents poisoned samples (whether from label-flipping or noisy injection) from influencing gradient computation.

3. **Clean Update Transmission**
   - Only updates derived from clean, validated samples are transmitted to the central server for aggregation, ensuring that poison is blocked at the source.

### 📊 Key Results
- Detects mislabeled training samples with **>85% accuracy** on both image and audio datasets.
- Effective when **poisonous data proportion stays below a threshold** (roughly 30–40%).
- Performance degrades when the poisoning ratio is very high — a known limitation.
- Provides a client-side defense that is **orthogonal** to server-side robust aggregation.

### ⚠️ Limitations
- Client-side defense requires honest client code execution — a malicious client could simply bypass the CFL module.
- Effectiveness drops sharply when poisoning rate exceeds 40%.
- Evaluated only on image and audio datasets, not on text/NLP tasks.

### 🔗 Relevance to This Thesis
> CFL's client-side label validation approach offers a **complementary defense layer** to the server-side robust aggregation techniques proposed in the MSc roadmap (Phase 3). Future work could integrate CFL-style local sanitization into the `client_app.py` before model updates are sent to the Flower `ServerApp`. However, it's important to note that in adversarial scenarios, a truly malicious client would simply skip the CFL validation step — making server-side defenses essential.

---

## Paper 4 — FedG2L: Privacy-Preserving FL Against Poisoning {#paper-4}

| Field | Details |
| :--- | :--- |
| **Full Title** | *FedG2L: a privacy-preserving federated learning scheme base on 'G2L' against poisoning attack* |
| **Authors** | Mengfan Xu, Xinghua Li |
| **Venue** | *Connection Science* (Taylor & Francis), Volume 35, Issue 1, 2023 |
| **DOI** | [10.1080/09540091.2023.2197173](https://doi.org/10.1080/09540091.2023.2197173) |
| **Citations** | ~8 (CrossRef/ResearchGate, as of mid-2026) |
| **Code** | Not publicly available |

### 🎯 Core Problem Addressed
FedG2L addresses **two intertwined problems** in FL systems:

1. **Data Island Problem** — organizations possess valuable local data but cannot share it due to privacy regulations (GDPR, CCPA).
2. **Centralized Aggregation Failure** — traditional FL architectures rely on a single central server, creating a single point of failure and a trust bottleneck that malicious clients can exploit.

The paper asks: *Can we build a fully decentralized FL system that resists poisoning at both the aggregation and local model levels, while preserving gradient privacy?*

### 🔬 Methodology — The "G2L" Architecture

The "Global to Local" name reflects the two-stage defense pipeline:

#### Stage 1: "G" — Global Aggregation via SecPBFT (Blockchain Layer)

SecPBFT = **Secure Practical Byzantine Fault Tolerance** — a modified PBFT consensus protocol with embedded gradient similarity checks.

**How SecPBFT Works:**

| Phase | Standard PBFT | SecPBFT Modification |
|:---|:---|:---|
| **1. Request** | Client sends transaction | Data owner submits local gradient (encrypted sub-gradient) |
| **2. Pre-Prepare** | Leader broadcasts proposal | Leader node broadcasts collected sub-gradients for similarity evaluation |
| **3. Prepare** | Nodes validate & broadcast agreement | Nodes compute **cosine similarity** between received sub-gradients and their own; vote on which gradients are benign |
| **4. Commit** | Nodes finalize consensus | **Malicious gradients** (cosine similarity below threshold) are excluded; only benign gradients are aggregated |
| **5. View Change** | Leader failure recovery | Same — ensures liveness if Byzantine leader is detected |

**Key Properties:**
- **No benign benchmark required**: Unlike FLTrust (which needs a clean server-side dataset), SecPBFT uses peer-to-peer gradient comparison.
- **Gradient privacy**: Sub-gradients are transmitted (not full gradients), preventing reverse-engineering of individual client data.
- **Byzantine tolerance**: Resilient with up to **50% malicious nodes**, consistent with PBFT guarantees.

#### Stage 2: "L" — Local Convergence via Improved ACGAN (Client-Side)

Even after SecPBFT filters out malicious gradients, **"late" poisoning effects** may persist. To counteract this:

1. Each client runs an **improved ACGAN (Auxiliary Classifier GAN)** locally.
2. The ACGAN generates **synthetic local training data** aligned with the clean decision boundaries of the current global model.
3. The client **retrains its local model** on this synthetic data, effectively "washing out" residual poison.

**ACGAN Architecture:**
- The generator produces class-conditional synthetic samples.
- The discriminator has *two heads*: (1) real/fake classification and (2) class label prediction (the "auxiliary classifier").
- This dual-objective training produces higher-quality, class-consistent synthetic data than standard GANs.

### 📊 Key Results

| Metric | Without Defense | With FedG2L | Improvement |
|:---|:---:|:---:|:---:|
| **Model Accuracy** | Severely degraded | Restored | **≥ 55% improvement** |
| **Attack Success Rate** | High | Reduced significantly | **≥ 60% reduction** |
| **Gradient Privacy** | N/A | ✅ Sub-gradients protected | Privacy preserved |
| **Byzantine Tolerance** | 0 | Up to **50% malicious nodes** | PBFT-level guarantee |

- **Datasets:** MNIST, CIFAR-10
- **Attack Types:** Label Flipping, Backdoor Injection, Random Noise

### ⚠️ Limitations
- Reports **relative improvements** (percentages) rather than absolute accuracy numbers, limiting direct comparison with other defenses.
- Image-only evaluation (MNIST, CIFAR-10) — no NLP/text-domain experiments.
- PBFT overhead: O(N²) message complexity per round may not scale to 100+ clients.
- Low citation count (~8) — published in a less prominent venue.
- No open-source code available.

### 🔗 Relevance to This Thesis
> FedG2L's `SecPBFT` gradient similarity consensus mechanism is conceptually identical to the **Cosine Similarity-based forensic auditing** proposed in Phase 4 of the MSc roadmap. The key difference is temporal: FedG2L applies cosine similarity *during training* (preventive), while the MSc thesis forensic engine applies it *post-hoc* (attributive). Together, they form a **complete temporal defense coverage** — "FedG2L prevents; our forensic engine attributes."

---

## Paper 5 — A Comprehensive Survey on Poisoning Attacks and Countermeasures {#paper-5}

| Field | Details |
| :--- | :--- |
| **Full Title** | *A Comprehensive Survey on Poisoning Attacks and Countermeasures in Machine Learning* |
| **Authors** | Zhiyi Tian, Lei Cui, Jie Liang, Shui Yu |
| **Venue** | *ACM Computing Surveys* (CSUR), Volume 55, Issue 8, 2022 |
| **DOI** | [10.1145/3551636](https://doi.org/10.1145/3551636) |
| **Access** | ACM Digital Library |
| **Citations** | **420+** (Google Scholar, as of mid-2026) |

### 🎯 Core Problem Addressed
Machine learning models are fundamentally vulnerable during the **training phase** because they implicitly trust their training data. Poisoning attacks exploit this trust by injecting carefully crafted samples or manipulating model updates to corrupt the learned model. The rise of **federated learning** (FL) amplifies this problem because the central server cannot directly inspect or sanitize client data. This survey provides a unified, systematic taxonomy covering the full spectrum of poisoning attacks and defenses across both centralized and federated paradigms.

### 🔬 Methodology & Taxonomy

The paper is organized into **6 major sections**:

| Section | Content |
|:---|:---|
| **§1 Introduction** | Motivation: ML security is existential; poisoning targets the training pipeline |
| **§2 Background & Threat Models** | Defines attacker capabilities (white-box, black-box, grey-box), knowledge levels, and goals |
| **§3 Taxonomy of Poisoning Attacks** | Core classification of attack types |
| **§4 Countermeasures for Centralized ML** | Data sanitization, robust statistics, model inspection |
| **§5 Poisoning in Federated Learning** | FL-specific attacks (gradient manipulation, model replacement) and FL-specific defenses (robust aggregation) |
| **§6 Challenges & Future Directions** | Open problems, adaptive attacks, real-world deployment gaps |

#### 📐 The Core Attack Taxonomy

**Dimension 1 — Attacker Goal:**

| Goal | Description | Example in Phishing Context |
|:---|:---|:---|
| **Availability Attack** (Untargeted) | Degrades overall model accuracy — a DoS on the model | Randomly flipping phishing/benign labels to reduce detection accuracy globally |
| **Integrity Attack** (Targeted) | Causes specific misclassifications while keeping overall accuracy intact | Injecting a backdoor trigger keyword so specific phishing emails bypass the filter |

**Dimension 2 — Attacker Capability:**

| Capability | Description | Example |
|:---|:---|:---|
| **Dirty-Label** | Attacker can modify both features and labels | Label Flipping: marking phishing emails as "benign" |
| **Clean-Label** | Attacker can only modify features; labels remain correct | Adversarial perturbations in legitimate-looking emails that shift decision boundaries |

#### 🛡️ FL Defense Taxonomy

| Defense Category | Algorithm | How It Works | Weakness |
|:---|:---|:---|:---|
| **Distance-Based** | **Krum** | Selects update closest to most other updates | Fails when malicious clients collude together |
| **Coordinate-Wise** | **Trimmed Mean** | Removes extreme values per coordinate before averaging | Vulnerable to coordinated attacks within trimmed bounds |
| **Coordinate-Wise** | **Median** | Uses coordinate-wise median instead of mean | High variance with few clients |
| **Trust-Based** | **FLTrust** | Server maintains small clean dataset to score updates | Requires server-side validation data |
| **Anomaly Detection** | **Spectral Analysis** | Detects outliers via SVD/PCA | Computationally expensive; struggles with non-IID |
| **Data Sanitization** | **RONI** | Rejects updates that reduce validation accuracy | Requires server-held validation set |

### 📊 Key Insights
1. **Defense–Attack Arms Race**: Every defense generates an adaptive attack. Krum was broken by "Little is Enough" (ALIE); Trimmed Mean was broken by "Inner Product Manipulation" (IPM).
2. **Non-IID Amplifies Risk**: Under non-IID distributions, benign client updates naturally diverge, making it harder to distinguish malicious outliers from legitimate variation.
3. **Explainability Gap**: Absence of model explainability makes post-hoc attribution extremely difficult — a gap that FLForensics (Paper 1) aims to fill.
4. **No Silver Bullet**: No single defense reliably handles all attack types. The paper advocates for **layered defense strategies**.

### ⚠️ Limitations
- Published in 2022 — does not cover the latest adaptive attacks and forensic methods from 2023–2025.
- Focuses primarily on **image classification** benchmarks; NLP/text attacks are less thoroughly covered.
- Defense evaluations are mostly theoretical/tabular comparisons rather than unified empirical benchmarks.

### 🔗 Relevance to This Thesis
> This survey serves as the **primary taxonomic and theoretical foundation** for the threat model and attack classifications in the MSc thesis. Specifically:
> - The **two-dimensional attack classification** (availability vs. integrity × dirty-label vs. clean-label) formally defines the Label Flipping and Backdoor Injection experiments.
> - The **defense taxonomy** validates the choice of Krum, Trimmed Mean, and Median as canonical baselines in Phase 3.
> - The **"explainability gap"** justifies the need for the forensic engine in Phase 4.
> - With **420+ citations**, citing this survey gives the thesis immediate academic legitimacy.

## Paper 6 — Robust FL Against Poisoning: A GAN-Based Defense Framework {#paper-6}

| Field | Details |
| :--- | :--- |
| **Full Title** | *Robust Federated Learning Against Poisoning Attacks: A GAN-Based Defense Framework* |
| **Authors** | Usama Zafar, André Teixeira, Salman Toor |
| **Venue** | arXiv Preprint (March 2025) |
| **Code** | [github.com/SciML-FL/gan-filter](https://github.com/SciML-FL/gan-filter) |
| **arXiv** | [arxiv.org/abs/2503.20884](https://arxiv.org/abs/2503.20884) |
| **Citations** | Recent (2025 publication) |

### 🎯 Core Problem Addressed
Các phương pháp phòng thủ chống tấn công đầu độc (poisoning attacks) trong FL hiện nay thường dựa trên các tập dữ liệu xác thực bên ngoài (external validation datasets) hoặc các giả định cấu trúc cố định (ví dụ: biết trước tỷ lệ hoặc số lượng client độc hại). Điều này vi phạm tính riêng tư của FL hoặc làm giảm khả năng mở rộng. 

Bài báo này đề xuất một **khung phòng thủ bảo vệ quyền riêng tư sử dụng Conditional GAN (cGAN)** để tự sinh dữ liệu giả lập (synthetic data) ngay trên server dựa trên mô hình toàn cục (global model) hiện tại, từ đó dùng tập dữ liệu này để kiểm tra và xác thực các cập nhật trọng số của các client mà không cần tập dữ liệu bên ngoài.

### 🔬 Methodology
Khung đề xuất vận hành theo mô hình cGAN cải tiến:
1. **Dùng Global Model làm Discriminator ($D$):** Khác với cGAN truyền thống, bộ phân loại Discriminator chính là mô hình toàn cục hiện tại $M_G^{(t)}$. Mục tiêu của Generator ($G$) không phải là đánh lừa $D$, mà là tạo ra dữ liệu giả lập có nhãn cụ thể sao cho $D$ phân loại chính xác theo ranh giới quyết định (decision boundaries) hiện tại của nó.
2. **Sinh tập dữ liệu giả lập ($\mathcal{D}_{syn}$):** Generator sau khi được huấn luyện sẽ tạo ra tập dữ liệu tổng hợp $\mathcal{D}_{syn}$ cho mỗi lớp mà không cần dữ liệu thật của các client.
3. **Xác thực cập nhật của Client (Authentication):** Server đánh giá hiệu năng (loss hoặc accuracy) của từng mô hình cập nhật từ các client trên tập dữ liệu giả lập $\mathcal{D}_{syn}$. Có hai cách tiếp cận:
   - **Adaptive Threshold (Ngưỡng thích ứng):** Loại bỏ các client có hiệu năng thấp hơn ngưỡng thích ứng tự động thay đổi theo từng round (ví dụ: dựa trên median hoặc mean của các client).
   - **Clustering-based (Phân cụm):** Phân cụm các cập nhật của client dựa trên hiệu năng trên dữ liệu giả lập để cô lập các outlier độc hại.

### 📊 Key Results
- Đánh giá trên 3 tập dữ liệu hình ảnh: MNIST, Fashion-MNIST, CIFAR-10 với LeNet-5 và ResNet-18.
- Chống chịu tốt trước **nhiều loại tấn công**: Random Noise (RN), Sign Flipping (SF), Label-Flipping (LF), và Backdoor (BK).
- Đạt tỷ lệ phát hiện client độc hại (TPR) và chấp nhận client lành tính (TNR) rất cao, đồng thời duy trì độ chính xác của mô hình toàn cục tốt hơn các thuật toán robust aggregation cổ điển (như Krum, Trimmed Mean) khi tỷ lệ client độc hại lên tới 30%.

### ⚠️ Limitations
- Đòi hỏi mô hình toàn cục ban đầu phải tương đối sạch (có thể đạt được bằng cách train trên một lượng nhỏ client tin cậy trước hoặc dùng robust aggregation ở vài vòng đầu).
- Chi phí tính toán bổ sung để train cGAN trên server ở mỗi round (mặc dù cGAN chỉ học ranh giới quyết định của mô hình toàn cục chứ không học phân phối dữ liệu gốc).
- Chưa được đánh giá trên dữ liệu văn bản/NLP (phishing emails).

### 🔗 Relevance to This Thesis
> Đây là bài báo **cực kỳ liên quan** đến sự kết hợp giữa **GAN và FL** chống poisoning. Khái niệm tự tạo dữ liệu giả lập tại Server bằng cGAN để xác thực cập nhật trọng số cung cấp một ý tưởng mới cho luận văn MSc: thay vì Server chỉ thụ động tính khoảng cách hình học vector (L2 Norm, Cosine Similarity) như đề xuất ban đầu, Server có thể tự sinh tập email giả lập dựa trên ranh giới quyết định của DistilBERT hiện tại để kiểm tra độ tin cậy của client.

---

## Comparative Analysis & Relevance to This Thesis {#comparative}

### 📊 Summary Comparison Table

| Paper | Year | Venue | Citations | Approach | Defense Stage | Application Domain |
| :--- | :---: | :--- | :---: | :--- | :--- | :--- |
| **FLForensics** | 2024 | NeurIPS | Growing | Influence Score Attribution | Post-deployment | Image (CIFAR, MNIST) |
| **FL Phishing Eval** | 2023 | Sensors (MDPI) | Moderate | Performance Benchmarking | Baseline | Phishing Email (NLP) |
| **Confident FL** | 2025 | Electronics (MDPI) | Recent | Local Label Validation | Pre-training (client-side) | Image, Audio |
| **FedG2L** | 2023 | Connection Science | ~8 | Blockchain + Gradient Consensus + ACGAN | During training (decentralized) | Image (MNIST, CIFAR) |
| **Tian et al. Survey** | 2022 | ACM CSUR | **420+** | Threat Model & Defense Taxonomy | System-wide / Lifecycle | Comprehensive |
| **Zafar et al. (cGAN)** | 2025 | arXiv Preprint | Recent | Server cGAN synthetic data evaluation | During training (server-side) | Image (MNIST, CIFAR-10) |

### 🎯 Mapping to Thesis Phases

| Thesis Phase | Papers Used | How They Connect |
| :--- | :--- | :--- |
| **Phase 1: Baseline FL** | Paper 2 (FL Phishing Eval) | Establishes the accuracy benchmark this thesis attacks and defends |
| **Phase 2: Attack Simulation** | Paper 5 (Survey), Paper 6 (Zafar) | Provides formal attack taxonomy (dirty-label/clean-label) and specific attack configurations (Sign Flipping, Backdoor, Label Flipping) |
| **Phase 3: Robust Aggregation** | Papers 4, 5, 6 (FedG2L + Survey + Zafar) | Validates Krum/Trimmed Mean/Median as baselines; introduces GAN-based and local-level alternatives |
| **Phase 4: Forensic Engine** | Papers 1, 4, 6 (FLForensics + FedG2L + Zafar) | FLForensics provides the theoretical framework for post-hoc attribution; FedG2L & Zafar validate using similarity and adaptive testing on generated data |

### 🧭 Research Positioning

This MSc thesis sits at the intersection of all five papers:

```
                        ┌──────────────────────┐
                        │   Tian et al. Survey  │
                        │   (Taxonomy Layer)    │
                        └──────────┬───────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                     │
   ┌──────────▼──────────┐ ┌──────▼──────────┐ ┌───────▼──────────┐
   │  Phase 2: ATTACK     │ │ Phase 3: DEFENSE │ │ Phase 4: FORENSIC│
   │  Label Flip + Backdoor│ │ Krum/TrimMean/Med│ │ L2 Norm + CosSim │
   │  (Survey taxonomy)   │ │ FedG2L SecPBFT   │ │ (FLForensics)    │
   │                      │ │ CFL (client-side)│ │ (FedG2L SecPBFT) │
   └──────────┬───────────┘ └──────┬───────────┘ └───────┬──────────┘
              │                    │                     │
              │                    │                     │
              └────────────────────┼─────────────────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  FL Phishing Eval     │
                        │  (Baseline Layer)     │
                        └──────────────────────┘
```

### 🔑 Novel Contribution of This Thesis

The novel contribution is the **end-to-end Poison-Forensics pipeline** that combines:
1. **Attack simulation** (Label Flipping + Backdoor Injection) on phishing email FL
2. **Defense evaluation** (Krum, Trimmed Mean, Median) for NLP-based federated models
3. **Privacy-preserving forensic attribution** (L2 Norm + Cosine Similarity traceback)

...all within a single **Dockerized FL environment** using the Flower framework — a combination that no existing paper provides.

*Sources: MDPI Sensors, MDPI Electronics, Connection Science (Taylor & Francis), NeurIPS 2024 Proceedings, ACM Computing Surveys, GitHub.*
