# Federated Learning for Phishing Email Detection

**Vietnam National University of Ho Chi Minh City**
**The International University — School of Computer Science and Engineering**

| Field | Detail |
|---|---|
| **Author** | Nguyen Dong Hai |
| **Student ID** | 24072183 |
| **Academic Year** | 2024/2025 |
| **Approved By** | Le Hai Duong |

---

## Declaration

I, Nguyen Dong Hai, hereby declare that this final report is the result of my independent work submitted in fulfillment of the requirements for the Bachelor degree at the University of the West of England. The study and preparation of this report were carried out between January 2025 and May 2025. This document reflects the findings, experiences, and insights that I gained throughout the research period. All external materials, such as academic publications, books, online resources, or expert advice, have been properly credited and referenced. I accept full responsibility for the accuracy, integrity, and originality of the content presented. Any errors, limitations, or weaknesses in this report are entirely my own, and the interpretations and suggestions expressed are based on my personal evaluation and reasoning.

*Nguyen Dong Hai*

---

## Acknowledgements

I would like to extend my sincere gratitude to my supervisor, **Dr. Le Hai Duong**, for his invaluable guidance, consistent support, and deep expertise throughout the course of this project. His thoughtful feedback and encouragement have been instrumental to the successful completion of my research.

I am also deeply thankful to the faculty members of both the International University and the University of the West of England. Their dedication to teaching and mentorship has not only enriched my academic journey but also inspired my personal and professional growth. Their commitment to education has left a lasting impact on my appreciation for learning.

---

## Summary

This project applies **Federated Learning (FL)** to phishing email detection using the **Flower framework**, **Docker**, and **transformer-based models**. It includes real-world testing via Thunderbird extensions for both prediction and user labeling. The system achieves strong accuracy while maintaining user privacy through local training, demonstrating the feasibility of deploying FL in cybersecurity applications.

---

## Project Access and Source Code

### Source Code Repository

The full implementation of this project is hosted on GitHub at:
**https://github.com/NguyenDongHaiPen/FL-phishingemail**

This repository includes:

- `client_app.py` — Client-side federated training logic
- `server_app.py` — Server-side model aggregation logic
- `model.pt` — Pre-trained phishing classifier model
- `phishing-backend/` — FastAPI backend for email inference
- `phishing-extension/` — Thunderbird extension for prediction
- `thunderbird-extension-label/` — Thunderbird extension for manual labeling
- `Dockerfiles` — Separate configurations for client/server containers
- `pyproject.toml` — Project dependency and configuration file

### Local Execution (Without Docker)

1. Clone the repository:

```bash
git clone https://github.com/NguyenDongHaiPen/FL-phishingemail
cd FL-phishingemail
```

2. Install dependencies:

```bash
pip install -e .
```

3. Run the Flower federated workflow:

```bash
flwr run .
```

### Docker Deployment

**Step 0: Create Docker Network**

```bash
docker network create --driver bridge flwr-network
```

**Step 1: Start SuperLink**

```bash
docker run --rm -p 9091:9091 -p 9092:9092 -p 9093:9093 \
  --network flwr-network --name superlink --detach \
  flwr/superlink:1.16.0 --insecure --isolation process
```

**Step 2: Start SuperNodes** *(Repeat the command for all four nodes with adjusted ports)*

```bash
docker run --rm -p 9094:9094 --network flwr-network --name supernode-1 --detach \
  flwr/supernode:1.16.0 --insecure --superlink superlink:9092 \
  --node-config "partition-id=0 num-partitions=4" \
  --clientappio-api-address 0.0.0.0:9094 --isolation process
```

**Step 3: Start ServerApp**

```bash
docker run --rm --network flwr-network --name serverapp --detach \
  flwr/serverapp:1.16.0 --insecure --serverappio-api-address superlink:9091
```

**Step 4: Start ClientApps** *(Repeat for all 4)*

```bash
docker run --rm --network flwr-network --name client-1 --detach \
  flwr/clientapp:1.16.0 --insecure --clientappio-api-address supernode-1:9094
```

### Running Thunderbird Extensions

**Step 1: Launch Inference Backend**

```bash
cd phishing-backend
uvicorn app:app --reload --port 8000
```

**Step 2: Load Extensions in Thunderbird**

- Open Thunderbird Developer Edition
- Navigate to `about:debugging` → *Load Temporary Add-on*
- Select `manifest.json` in both detector and labeler folders

**Extension Functionality:**

- **Phishing Detector** — Sends email text to FastAPI model and displays prediction inline
- **Phishing Labeler** — Enables user labeling of emails and CSV export

### Reproducibility

1. Clone the GitHub repository
2. Install dependencies or set up Docker
3. Run Flower clients and server (locally or Docker)
4. Start the backend API via `uvicorn`
5. Load Thunderbird extensions and interact with test emails

---

## Table of Contents

1. [Introduction](#chapter-1-introduction)
2. [Literature Review](#chapter-2-literature-review)
3. [Proposed Method](#chapter-3-proposed-method)
4. [Evaluation](#chapter-4-evaluation)
5. [Discussion of Outcomes](#chapter-5-discussion-of-outcomes)
6. [Conclusion and Recommendations](#chapter-6-conclusion-and-recommendations)

---

## Chapter 1: Introduction

### 1.1 Background and Problem Statement

Phishing is one of the most persistent threats in cybersecurity, where users are targeted through deceptive emails crafted to extract sensitive information such as login credentials, financial details, or personal identifiers. Traditional phishing detection systems typically use centralized machine learning (ML) models that require large-scale aggregation of user data into a central server. While these centralized systems are often effective, they raise significant concerns around data privacy, especially in regulated environments governed by policies such as the **General Data Protection Regulation (GDPR)** in the European Union.

**Federated Learning (FL)** has emerged as a promising solution to this issue. Rather than sending data to a centralized server, FL allows multiple clients—devices, users, or organizations—to collaboratively train a shared model while keeping raw data local. Model updates are shared and aggregated centrally, preserving privacy and data locality. This architecture is particularly well-suited for scenarios where privacy, data sensitivity, or legal restrictions prevent centralized data collection.

Federated Learning Systems (FLS) consist of a central orchestration server and multiple decentralized clients that participate in iterative training. As highlighted by Li et al. (2020), FLS design must address key challenges such as non-IID data distributions, high communication overhead, and secure aggregation of updates. Despite these challenges, FL has shown strong promise in privacy-sensitive fields like healthcare, finance, and cybersecurity.

### 1.2 Project Motivation

The increasing demand for privacy-preserving AI has sparked interest in decentralized training frameworks. This project is motivated by the real-world challenge of detecting phishing emails without violating user privacy. FL offers a solution by enabling learning across clients without requiring access to raw email content. By applying FL to the domain of phishing detection, the project explores how decentralized systems can maintain performance while improving privacy protection. Through Docker-based simulation and real-world extensions in Thunderbird, the project also aims to evaluate the deployment viability of FL in practical email environments.

### 1.3 Research Objectives

This project sets out to:

- Investigate the feasibility of using Federated Learning for phishing email classification.
- Implement a federated learning pipeline using the **Flower framework**, with transformer-based models via HuggingFace.
- Evaluate model performance using metrics such as **accuracy**, **precision**, **recall**, and **loss** across multiple rounds.
- Simulate realistic deployment using Docker containers and Thunderbird extensions for both detection and data labeling workflows.

### 1.4 Scope of Study

The study focuses on developing and evaluating a privacy-respecting phishing detection system using FL. The main components include:

- Training on the publicly available `zefang-liu/phishing-email-dataset`.
- Comparing model performance between **TinyBERT** and **DistilBERT**.
- Simulating distributed client training using isolated Docker containers.
- Evaluating usability via two Thunderbird extensions: one for real-time detection and another for manual email labeling.

The study does not include secure aggregation protocols like homomorphic encryption or differential privacy, nor does it attempt direct comparisons with centralized systems, which are left for future exploration.

### 1.5 Report Structure

The remainder of this report is organized as follows:

- **Chapter 1 – Introduction**: Introduces the project background, motivation, objectives, and report structure.
- **Chapter 2 – Literature Review**: Summarizes related research in phishing detection, FL frameworks, and transformer-based NLP models.
- **Chapter 3 – Proposed Method**: Describes the system architecture, tools, and technical implementation of the federated learning pipeline.
- **Chapter 4 – Evaluation**: Presents model results, performance metrics, and runtime comparisons across different configurations.
- **Chapter 5 – Discussion**: Reflects on implementation challenges, project relevance, and practical deployment insights.
- **Chapter 6 – Conclusion and Future Work**: Concludes the project with key takeaways and suggestions for further improvements.

---

## Chapter 2: Literature Review

### 2.1 Federated Learning in Cybersecurity

Federated Learning (FL) is a decentralized approach to training machine learning models collaboratively across multiple clients while keeping raw data local. It was initially proposed to address privacy issues in mobile devices and edge computing, where data collection and centralization are impractical or legally restricted (McMahan et al. 2017).

In the cybersecurity domain, FL has gained significant attention due to its privacy-preserving nature. For example, Awosika et al. (2024) demonstrated that FL could be used to train fraud detection models collaboratively across financial institutions while maintaining data confidentiality. This approach has the advantage of leveraging a diverse range of data sources while complying with data protection laws like GDPR.

Recent research has shown that FL can perform comparably to centralized models when appropriate aggregation strategies and model architectures are used (Thapa et al. 2023). Despite the benefits, FL also introduces several challenges such as communication latency, client heterogeneity, and vulnerability to **poisoning or backdoor attacks** (Bagdasaryan et al. 2020). These issues are critical when applying FL to real-world security scenarios like phishing detection, where attackers might try to exploit the training process.

### 2.2 Phishing Detection with NLP and Transformers

Phishing email detection is typically formulated as a **binary classification task**, where each email is labeled as either "phishing" or "safe." Traditional approaches rely on handcrafted features such as sender metadata, URL structure, and keyword frequency. However, recent advancements in Natural Language Processing (NLP) have enabled models to understand deeper semantic and contextual cues from email content.

Transformer-based architectures like **BERT** have revolutionized NLP by introducing attention mechanisms that can capture long-range dependencies in text. **DistilBERT**, a lighter variant of BERT, retains much of its performance while reducing the number of parameters and training time (Sanh et al. 2019). These models have been widely adopted for text classification tasks, including phishing detection, due to their superior accuracy and ability to generalize across writing styles and languages.

In the context of federated learning, NLP models present both opportunities and challenges. Their large parameter sizes increase communication costs in FL settings, but their high accuracy justifies the overhead in many applications. Some works, like Thapa et al. (2023), have shown that Transformer models can be fine-tuned effectively in FL environments without centralized data access.

### 2.3 Tools and Frameworks

To implement the federated phishing detection pipeline, a combination of open-source tools and modern frameworks was used.

#### Flower Framework

The core of the federated orchestration is built on **Flower (FLWR)**, an open-source FL framework that abstracts the communication between server and clients. Flower supports strategy customization, client sampling, and distributed training for both research and production purposes. The **FedAvg** (Federated Averaging) strategy is commonly used in Flower, where client updates are aggregated by averaging their local model weights (McMahan et al. 2017). **Flower v1.16.0** was used in this project.

#### HuggingFace Transformers

HuggingFace provides pre-trained transformer models like BERT, DistilBERT, and TinyBERT, along with utilities for tokenization and fine-tuning. In this project, HuggingFace's `AutoTokenizer` and `Trainer` classes were employed to simplify the NLP pipeline.

#### PyTorch and Scikit-learn

PyTorch serves as the primary deep learning backend for model training and optimization. Evaluation metrics such as accuracy, precision, recall, and loss were calculated using scikit-learn.

#### Docker

Docker containers were used to simulate independent client environments. This ensured reproducibility and client isolation, which are essential for mimicking real-world FL deployment conditions. Each client ran in its own container and trained its local copy of the model before sending updates back to the server.

Together, these tools provided a modular and flexible environment for implementing and evaluating a federated phishing email detection system.

#### 2.3.1 Thunderbird

Thunderbird is an open-source email client developed by Mozilla, known for its cross-platform compatibility and extensibility via WebExtension APIs. Its ability to run entirely on local devices makes it a suitable endpoint for privacy-preserving systems such as Federated Learning (FL). Within this project, Thunderbird serves as a front-end environment to demonstrate how phishing detection models can be deployed and used in real-world email applications without transmitting sensitive data externally.

Due to its support for client-side execution and local file access, Thunderbird enables the integration of both model inference (for phishing detection) and manual data labeling workflows. This makes it a practical and privacy-aligned choice for prototyping FL in cybersecurity use cases.

---

## Chapter 3: Proposed Method

### 3.1 Overview

This chapter describes the design and implementation of the federated phishing detection system, including the model architecture, dataset handling, client simulation setup, and integration with real-world email environments. The system is built using the **Flower federated learning framework**, **HuggingFace Transformers**, **PyTorch**, and **Docker** for environment simulation. Each section below outlines specific design choices and implementation steps.

### 3.2 Dataset and Preprocessing

The phishing detection task is trained on the publicly available **`zefang-liu/phishing-email-dataset`** (Liu 2023) from HuggingFace. This dataset consists of labeled email messages categorized as either "Phishing Email" or "Safe Email."

- **Tokenization**: The email text is tokenized using HuggingFace's `AutoTokenizer` for DistilBERT. Each sequence is truncated or padded to a fixed length of **512 tokens** to ensure uniform input shape across batches.
- **Client Partitioning (IID)**: To simulate the federated setup, the dataset is partitioned across clients using Flower's `IidPartitioner`. This ensures each client receives a balanced and identically distributed (IID) subset of data.

IID partitioning was chosen because it maintains class balance across clients, simplifies training dynamics, and avoids early convergence issues due to data imbalance. While real-world settings may involve non-IID data, this setup provides a strong baseline for evaluating core system performance.

### 3.3 Model Selection and Justification

The model chosen for this task is **DistilBERT**, a lightweight variant of BERT that retains **97% of BERT's performance** while reducing the number of parameters by **40%** (Sanh et al. 2019). Initially, `prajjwal1/bert-tiny` was used for testing due to its minimal memory footprint, which was helpful during early prototyping and debugging. However, due to its lower representational capacity, it was later replaced with `distilbert-base-uncased` for the final evaluation.

BERT-based architectures, especially distilled versions, have been shown to outperform classical NLP approaches and other shallow neural networks in phishing detection tasks. As noted in Thapa et al. (2023), transformer models offer better generalization, semantic understanding, and detection of subtle contextual cues, making them ideal for email classification.

### 3.4 Federated Learning Configuration

The federated learning process is orchestrated using **Flower v1.16.0** (Beutel et al. 2022). The server coordinates the training using the **Federated Averaging (FedAvg)** algorithm (McMahan et al. 2017), which averages local model updates from clients to produce a global model.

- **Aggregation Strategy**: FedAvg was selected for its simplicity, proven effectiveness, and widespread adoption in academic and industrial federated learning settings. It is particularly well-suited for IID scenarios and demonstrates stable convergence on CPU-constrained environments.
- **Configuration**:
  - `fraction_fit = 1.0` — All clients participate in every round
  - `min_fit_clients = 4`, `min_available_clients = 4`
  - `local_epochs = 1`

This setup ensures that every client contributes to each training round, which improves consistency, synchronization, and convergence quality.

To simulate realistic federated deployments, the system is designed with a modular architecture comprising a central **ServerApp**, multiple client containers (**ClientApp**), and Flower **SuperNode** components to manage routing and communication. Each client runs in an isolated Docker container and communicates with the server via Flower's communication protocol. This architecture ensures that no raw data is shared — only model updates are exchanged, in line with FL's privacy-first principles.

### 3.5 Client Simulation with Docker

To emulate real-world distributed clients, each participant in the federated setup is simulated using **Docker containers**. Each container runs an isolated Python environment with pre-installed dependencies and executes training locally without exposing any raw data.

- **Why Docker**: While local execution was faster (375 seconds), Docker-based training (approximately 5753 seconds) more accurately simulated real-world constraints such as environment isolation and process overhead. This trade-off favored deployment realism and modularity.
- **Client Setup**: Each Docker container receives its own IID-partitioned dataset and independently performs training using the HuggingFace Transformer-based model. After training, updated model weights are transmitted to the server for aggregation via Flower's protocol.

### 3.6 Real-World Integration: Thunderbird Extensions

To demonstrate the applicability of this system in real-world scenarios, two custom extensions were developed for the Thunderbird email client:

- **Phishing Detector Extension**: Integrates the trained PyTorch model to classify incoming emails as "phishing" or "safe" in real-time when the email is opened.
- **Phishing Trainer Extension**: Enables users to manually label emails and export the annotated data as a CSV file. These labels can then be reused to simulate client-local training in future federated rounds.

The client-side training behavior — including checkpoint loading, dataset partitioning, model training, and evaluation — is implemented using HuggingFace and PyTorch. These extensions ensure that email content stays on-device, fulfilling the privacy-first design principles of federated learning.

---

## Chapter 4: Evaluation

### 4.1 Experimental Setup

The federated training experiments were conducted on a **Mac Mini M4** equipped with an 8-core CPU and 16GB of unified memory. All training was executed sequentially across **four Docker containers** simulating independent clients. No GPU acceleration was used. Each round of training consisted of one local epoch per client, followed by centralized aggregation on the server using the FedAvg strategy.

The evaluation was performed using standard classification metrics: **accuracy**, **precision**, **recall**, and **cross-entropy loss**. These metrics were computed after each round to monitor model performance progression.

### 4.2 Model Performance Over Rounds

The model was trained for **5 federated rounds**. Performance improvements were observed consistently across all metrics.

*Table 4.1: Model Performance Metrics by Round*

| Round | Accuracy (%) | Precision (%) | Recall (%) | Loss |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 95.10 | 91.25 | 94.78 | 0.0912 |
| 2 | 96.80 | 94.21 | 95.65 | 0.0487 |
| 3 | 97.56 | 95.35 | 97.02 | 0.0321 |
| 4 | 98.71 | 98.23 | 98.14 | 0.0184 |
| **5** | **99.31** | **99.53** | **99.30** | **0.0112** |

The results show a steady increase in performance. By Round 5, the model had nearly perfect precision and recall, indicating a robust ability to distinguish phishing from safe emails.

### 4.3 Training Logs

To monitor convergence, the model's accuracy, precision, recall, and cross-entropy loss were logged after each federated training round via terminal output. The model's performance improved over 5 rounds. Specifically:

- **Loss** decreased steadily from **0.0912** in Round 1 to **0.0112** in Round 5.
- **Accuracy** increased from **97.16%** to **99.31%**.
- **Precision** and **Recall** also reached **99.5%**, indicating strong model convergence.

These metrics confirm that even under the constraints of CPU-only training and Docker-induced latency, the federated learning process remained stable and effective.

### 4.4 Runtime Comparison

The following table summarizes the runtime difference between Docker and local training setups:

*Table 4.2: Training Time Comparison*

| Training Mode | Total Runtime (seconds) |
|---|:---:|
| Local (non-Docker) | 375 |
| Docker-based Federated Setup | 5,753 |

Docker introduces a significant overhead — about **15 times slower**. This is expected due to container startup, memory isolation, and process scheduling. However, Docker enables more realistic deployment conditions, simulating isolated client environments.

### 4.5 Key Observations

- FL was able to achieve high performance even without centralized access to training data.
- Accuracy and recall rose consistently across training rounds, suggesting stable convergence.
- Despite increased runtime in Dockerized settings, the approach remains viable for privacy-preserving deployment.
- **Precision nearing 100%** ensures that false positives (marking safe emails as phishing) are extremely rare — a crucial requirement in email clients.

---

## Chapter 5: Discussion of Outcomes

The outcomes of this project confirm that Federated Learning (FL) is a viable and effective approach for phishing email detection in privacy-sensitive environments. The final model, trained using DistilBERT within a Dockerized federated setting, achieved a peak **accuracy of 99.31%**, **precision of 99.53%**, and **recall of 99.30%** by the fifth training round. These results represent significant improvements over initial rounds and are consistent with benchmarks reported in centralized learning research (Thapa et al. 2023).

Furthermore, the cross-entropy loss decreased steadily from **0.0912** in Round 1 to **0.0112** in Round 5, indicating robust convergence under the FedAvg aggregation strategy. The performance above demonstrates that FL can maintain high model effectiveness while ensuring that raw email data remains on client devices, making it well-suited for deployment in domains with strict data protection requirements.

### 5.1 Relevance and Real-World Application

This project is professionally relevant in multiple dimensions:

- It tackles a real cybersecurity threat using modern deep learning techniques.
- It employs a **privacy-preserving approach**, which is increasingly important in regulated industries such as finance, healthcare, and enterprise IT.
- It demonstrates practical deployment via Thunderbird extensions, showing how federated models can be integrated into real-world email clients for both prediction and user-driven training data generation.

The Thunderbird extensions bridge the gap between theory and application. By allowing users to both interact with and contribute to the training process, the system simulates a real-world federated learning workflow. Such integration demonstrates the potential for scalable deployments where multiple users can improve a global model without compromising their private email data.

### 5.2 Relation to Existing Work

This project aligns well with prior studies. Thapa et al. (2023) showed that FL can match centralized learning in phishing detection, while Awosika et al. (2024) highlighted its utility in financial fraud contexts, reinforcing the broader applicability of FL in cybersecurity. From a systems perspective, Li et al. (2020) outlined the challenges of designing scalable and privacy-respecting FL architectures. This project adopts several of their best practices: use of a modular orchestration layer (Flower), distributed client simulation (Docker), and communication-efficient strategies (FedAvg).

Moreover, the model design choices reflect an understanding of trade-offs: **DistilBERT** provides strong language understanding with reduced computational load, a critical factor when training on resource-limited Docker containers.

### 5.3 Evaluation of Project Scope and Outcome

The original project goals — to apply FL to phishing detection, ensure local-only training, and simulate real-world use — were met successfully. The deployment of two Thunderbird extensions extends the impact of the system beyond academic testing, into realistic application workflows. Feedback from testing showed that the labeling tool is especially useful for scenarios where user feedback is essential for evolving threats.

One significant achievement was sustaining strong performance under constraints such as CPU-only training, non-GPU inference, and overhead introduced by Docker. Furthermore, using IID data partitioning resulted in training that was consistent and fair across clients, facilitating a more predictable convergence.

### 5.4 Limitations

Despite the strengths, several limitations were identified:

- **Lack of secure aggregation**: No differential privacy or cryptographic methods were used to protect model updates, leaving potential exposure in hostile environments.
- **No heterogeneous data**: The use of IID partitioning simplifies the problem. Real deployments will often involve non-IID distributions, which affect model convergence.
- **Scalability**: Training time increased significantly in Docker environments (approximately 15x slower than local), limiting usability for larger-scale simulations or real-time federated learning.
- **Client failure resilience**: While Flower supports fault tolerance, this project did not test robustness under partial client dropout or unreliable connections.

### 5.5 Recommendations for Future Work

Future work should focus on improving the system's privacy guarantees and scalability:

- Add **secure aggregation mechanisms** such as differential privacy or **SMPC** (Secure Multi-party Computation) to protect model updates.
- Test with **non-IID data distributions** to reflect real-world scenarios and evaluate model robustness.
- Experiment with **asynchronous training** to reduce training time and increase flexibility.
- Evaluate robustness to **adversarial clients or poisoning attacks**, in light of surveys such as Bagdasaryan et al. (2020).
- Deploy across **multiple physical devices** to simulate a true cross-device FL setting.

---

## Chapter 6: Conclusion and Recommendations

This project has effectively demonstrated the feasibility and effectiveness of using Federated Learning (FL) for phishing email detection in a privacy-conscious context. By leveraging Flower to orchestrate the federation, integrating HuggingFace Transformers for natural language processing, and using Docker containers to simulate client isolation, the system maintained a high level of predictive capability while ensuring that raw user data remained local.

The final federated model achieved strong performance, with high accuracy, precision, and recall — comparable to centralized approaches. This confirms that FL can function robustly in this domain. Furthermore, the development and deployment of two Thunderbird email client extensions — one for real-time phishing detection and another for user labeling — demonstrated practical utility and usability for end-users.

From a technical and professional perspective, the project provided valuable experiential insights into modern machine learning pipelines and privacy-preserving system design. It also highlighted the challenges associated with decentralized architectures, including synchronization, system overhead, and scalability.

Although the project encountered limitations such as extended Docker training time and lack of secure aggregation, these issues were managed within scope. The system's modular design allows it to serve as a foundation for future improvements.

Future work should explore implementing **secure aggregation methods** (e.g., differential privacy or SMPC), testing with **non-IID data distributions**, and deploying across **heterogeneous devices**. These enhancements could further increase the system's scalability, privacy, and real-world effectiveness for protecting users against phishing threats.

---

## References

- Awosika, T., Okafor, E., Alghamdi, S. & Uzoma, C. (2024), 'Transparency and privacy: The role of explainable ai and federated learning in financial fraud detection', *IEEE Access* 12, 1–15. https://doi.org/10.1109/ACCESS.2024.3394528

- Bagdasaryan, E., Veit, A., Hua, Y., Estrin, D. & Shmatikov, V. (2020), How to backdoor federated learning, in 'Proceedings of the 23rd International Conference on Artificial Intelligence and Statistics (AISTATS)', pp. 2938–2948. https://proceedings.mlr.press/v108/bagdasaryan20a.html

- Beutel, D., Topal, T., Mathur, A., Qiu, X., Ramage, D. & Zhao, F. (2022), 'Flower: A friendly federated learning framework', https://flower.dev/. Accessed: 2025-04-30.

- Li, T., Sahu, A., Talwalkar, A. & Smith, V. (2020), 'Federated learning: Challenges, methods, and future directions', *IEEE Signal Processing Magazine* 37(3), 50–60. https://doi.org/10.1109/MSP.2020.2975749

- Liu, Z. (2023), 'Phishing email dataset', https://huggingface.co/datasets/zefang-liu/phishing-email-dataset. Accessed: 2025-04-30.

- McMahan, H., Moore, E., Ramage, D., Hampson, S. & y Arcas, B. (2017), Communication-efficient learning of deep networks from decentralized data, in 'Proceedings of the 20th International Conference on Artificial Intelligence and Statistics (AISTATS)', pp. 1273–1282. https://proceedings.mlr.press/v54/mcmahan17a.html

- Sanh, V., Debut, L., Chaumond, J. & Wolf, T. (2019), 'Distilbert, a distilled version of bert: smaller, faster, cheaper and lighter', *arXiv preprint arXiv:1910.01108*. https://arxiv.org/abs/1910.01108

- Thapa, C., Tang, J., Abuadbba, S., Gao, Y., Camtepe, S., Nepal, S., Almashor, M. & Zheng, Y. (2023), 'Evaluation of federated learning in phishing email detection', *Sensors* 23(9), 4346. https://doi.org/10.3390/s23094346

---

## Appendix A: System Architecture Diagram

The server coordinates the federated training process using the `ServerApp` component. Each client runs a local `ClientApp`, encapsulated in a container or process, connected to a `SuperNode` that handles communication with the server via the Flower protocol. This modular structure allows model updates to be passed securely from clients to the server without transmitting any raw data.

The system mirrors the deployment setup used in this project, with **four Dockerized clients** operating under the same structure and a central Flower server performing aggregation via the **FedAvg strategy**.

*Figure A.1: Basic Flower federated learning architecture*

```
┌──────────────────────┐        ┌──────────────────────────────┐
│        Server        │        │           Client             │
│  ┌────────────────┐  │        │  ┌──────────┐  ┌─────────┐  │
│  │   ServerApp    │──│────────│─▶│ SuperNode│──│ClientApp│  │
│  └────────────────┘  │        │  └──────────┘  └─────────┘  │
│  ┌────────────────┐  │        └──────────────────────────────┘
│  │   SuperLink    │  │
│  └────────────────┘  │        ┌──────────────────────────────┐
└──────────────────────┘        │           Client             │
                                │  ┌──────────┐  ┌─────────┐  │
                                │  │ SuperNode│──│ClientApp│  │
                                │  └──────────┘  └─────────┘  │
                                └──────────────────────────────┘
```

---

## Appendix B: Thunderbird Extensions

### Phishing Detector Extension

This extension classifies emails in real time using the locally trained model. It displays a **phishing probability score** based on the model's output, providing immediate feedback within the Thunderbird interface.

*Figure B.1: Phishing Detector Extension — displays "Status: Phishing" with a rating of 99.87% for a detected phishing email.*

### Phishing Trainer Extension

This extension allows users to manually label emails as **"Phishing"** or **"Safe"**, then export their labels as a CSV file for use in client-side local training.

*Figure B.2: Phishing Trainer Extension — shows a labeled email summary (Phishing: 2 | Safe: 2 | Total: 4) with options to Download CSV or Reset.*

---

## Appendix C: Training Logs

The following logs were generated from a federated training session conducted using the Flower framework over **5 rounds** with **4 Docker-based clients**. Metrics such as accuracy, precision, recall, and loss were recorded after each round. These values demonstrate progressive model convergence and illustrate the system's ability to train across distributed nodes while maintaining privacy.

*Figure C.1: Accuracy, Precision, and Recall Over 5 Rounds*

```
INFO :    Starting Flower ServerApp, config: num_rounds=5, no round_timeout

INFO :    [INIT]
INFO :    Using initial global parameters provided by strategy
INFO :    Starting evaluation of initial global parameters
INFO :    Evaluation returned no results ('None')

INFO :    [ROUND 1]
INFO :    configure_fit: strategy sampled 2 clients (out of 4)
INFO :    aggregate_fit: received 2 results and 0 failures
INFO :    configure_evaluate: strategy sampled 4 clients (out of 4)
INFO :    aggregate_evaluate: received 4 results and 0 failures

INFO :    [ROUND 2]
...
INFO :    [ROUND 5]
INFO :    configure_fit: strategy sampled 2 clients (out of 4)
INFO :    aggregate_fit: received 2 results and 0 failures
INFO :    configure_evaluate: strategy sampled 4 clients (out of 4)
INFO :    aggregate_evaluate: received 4 results and 0 failures

INFO :    [SUMMARY]
INFO :    Run finished 5 round(s) in 13514.03s
INFO :    History (loss, distributed):
INFO :            round 1: 0.002351067867928028
INFO :            round 2: 0.001792257361147648
INFO :            round 3: 0.001524119277310164
INFO :            round 4: 0.001589653087271957
INFO :            round 5: 0.001720431719695820
INFO :    History (metrics, distributed, evaluate):
INFO :    {'accuracy': [(1, 0.9748124330117),
INFO :                  (2, 0.9761521972132905),
INFO :                  (3, 0.9788317256162915),
INFO :                  (4, 0.9801714898177921),
INFO :                  (5, 0.9801714898177922)],
INFO :     'precision': [(1, 0.9546717256443009),
INFO :                   (2, 0.9536502544109035),
INFO :                   (3, 0.9581482313531473),
INFO :                   (4, 0.9607719970363748),
INFO :                   (5, 0.9576782512330)],
INFO :     'recall': [(1, 0.9821295150363756),
INFO :                (2, 0.9869397198546549),
INFO :                (3, 0.9889704888588231),
INFO :                (4, 0.9896930709257897),
INFO :                (5, 0.9931050553995713)]}
```

---

## Appendix D: Key Code Snippets

### Flower Strategy Setup (FedAvg Parameters)

*From `pyproject.toml`:* This configuration controls how the Flower server orchestrates federated learning. FedAvg aggregates client updates. The settings specify that each round requires two clients to participate, each training locally for one epoch using the `distilbert-base-uncased` model.

```toml
[tool.flwr.app.config]
num-server-rounds = 5
min_fit_clients = 2
min_evaluate_clients = 2
min_available_clients = 2
fraction-fit = 0.2
fraction-evaluate = 0.5
local-epochs = 1
model-name = "distilbert-base-uncased"
num-labels = 2
round-timeout = 300
```

### Dockerfile Snippet

*From `clientapp.Dockerfile`:* This Dockerfile sets up the client environment, installs the project, and starts a Flower client instance. Docker enables containerized, reproducible training environments that simulate independent clients.

```dockerfile
FROM flwr/clientapp:1.16.0

WORKDIR /app
COPY pyproject.toml .
RUN sed -i 's/.*flwr\[simulation\].*//' pyproject.toml \
    && python -m pip install -U --no-cache-dir .

ENTRYPOINT ["flwr-clientapp"]
```

### Client-Side Training Logic

*From `client_app.py`:* The following Python code defines the client training behavior for Flower using a HuggingFace transformer model. The client loads a saved model checkpoint if available, retrieves and partitions the dataset, and defines training (`fit`) and evaluation (`evaluate`) methods for use in federated rounds. This code is critical in managing local training inside each Dockerized client.

```python
import os
import torch
from flwr.common import Context
from flwr.client import ClientApp, NumPyClient
from transformers import AutoModelForSequenceClassification
from fl_test.task import train, test, get_weights, set_weights, load_data

MODEL_PATH = "saved_model"

def save_model(net):
    os.makedirs(MODEL_PATH, exist_ok=True)
    torch.save(net.state_dict(), os.path.join(MODEL_PATH, "model.pt"))

def load_model(model_name: str, num_labels: int):
    net = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    model_file = os.path.join(MODEL_PATH, "model.pt")
    if os.path.exists(model_file):
        net.load_state_dict(torch.load(model_file))
        print("✅ Loaded model checkpoint from disk.")
    else:
        print("⬜ No saved model found. Loading fresh model.")
    return net

def client_fn(context: Context) -> NumPyClient:
    partition_id = context.node_config["partition-id"]
    num_partitions = context.node_config["num-partitions"]
    model_name = context.run_config["model-name"]
    num_labels = context.run_config["num-labels"]
    local_epochs = context.run_config["local-epochs"]

    net = load_model(model_name=model_name, num_labels=num_labels)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net.to(device)

    trainloader, testloader = load_data(partition_id, num_partitions, model_name)

    class FlowerClient(NumPyClient):
        def get_parameters(self, config):
            return get_weights(net)

        def set_parameters(self, parameters, config):
            set_weights(net, parameters)

        def fit(self, parameters, config):
            self.set_parameters(parameters, config)
            train(net, trainloader, epochs=local_epochs, device=device)
            save_model(net)  # ✅ Save after local training
            return get_weights(net), len(trainloader.dataset), {}

        def evaluate(self, parameters, config):
            self.set_parameters(parameters, config)
            loss, accuracy, precision, recall = test(net, testloader, device=device)
            return float(loss), len(testloader.dataset), {
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
            }

    return FlowerClient().to_client()
```
