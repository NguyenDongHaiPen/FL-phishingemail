# 🛡️ Federated Learning for Phishing Email Detection with Poison-Forensics

[![Flower v1.16.0](https://img.shields.io/badge/Flower-1.16.0-blue?style=flat-square)](https://flower.ai)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red?style=flat-square)](https://pytorch.org/)
[![HuggingFace](https://img.shields.io/badge/Transformers-DistilBERT-yellow?style=flat-square)](https://huggingface.co/)
[![Docker](https://img.shields.io/badge/Docker-Containers-blue?style=flat-square)](https://www.docker.com/)

A Federated Learning (FL) system for phishing email detection integrated with a digital forensic mechanism (Poison-Forensics) to identify and attribute malicious data/model poisoning attacks from Client nodes, protecting the integrity of the centrally aggregated model.

---

## 🛠️ Tech Stack & Environment

- **Federated Learning Framework:** [Flower v1.16.0](https://flower.ai/docs/)
- **Deep Learning Framework:** PyTorch & HuggingFace Transformers (Text classification using pre-trained **DistilBERT**)
- **Inference Client:** Thunderbird Extension (connecting to local API) & Backend [FastAPI](https://fastapi.tiangolo.com/)
- **Virtualization Environment:** Docker / Docker-compose (simulating realistic Non-IID distributed environments)

---

## 🗂️ Documentation Structure (AI-First Doc System)

The documentation system is hierarchically organized to help AI Agents quickly understand context and execute tasks accurately:

```
FL-phishingemail/
├── AGENTS.md                  # Supreme AI Agent rules and workflows
├── README.md                  # Project overview and run instructions (This file)
└── docs/
    ├── flwr.md                # Flower Framework references and syntax
    ├── architecture/
    │   ├── data-models.md     # Data pipeline & Non-IID Dirichlet partitioning
    │   ├── threat-model.md    # Threat model & MITRE ATT&CK (AML.T0006) specs
    │   └── robust-aggregation.md # Robust aggregation strategies (Median, Trimmed Mean, Krum)
    └── agent/
        └── forensic-standards.md # Poison-Forensics indicators (L2 Norm, Cosine Similarity)
```

---

## 🚀 Environment Simulation Guide (4 Clients)

The project supports two simulation options: running locally using the Flower Simulation Engine (best for fast debugging) and running in a distributed environment using Docker Containers (best for network-level forensics testing).

### Option 1: Local Simulation (Flower Simulation Engine)

1. Install project dependencies in editable mode:
   ```bash
   pip install -e .
   ```
2. Run the simulation (Flower automatically handles the lifecycle of clients and servers on RAM/CPU):
   ```bash
   flwr run .
   ```

---

### Option 2: Distributed Simulation using Docker (4 Nodes)

To test the forensics and poisoning scenarios, you can isolate clients into separate Docker containers.

#### Step 0: Create a Virtual Docker Network
```bash
docker network create --driver bridge flwr-network
```

#### Step 1: Build Images for ServerApp & ClientApp
```bash
docker build -t flwr/serverapp:1.16.0 -f serverapp.Dockerfile .
docker build -t flwr/clientapp:1.16.0 -f clientapp.Dockerfile .
```

#### Step 2: Start the SuperLink (Central Coordinator)
```bash
docker run --rm \
  -p 9091:9091 -p 9092:9092 -p 9093:9093 \
  --network flwr-network \
  --name superlink \
  --detach \
  flwr/superlink:1.16.0 \
  --insecure \
  --isolation process
```

#### Step 3: Launch 4 SuperNodes (Representing 4 Data Partitions)
Run the following 4 commands to set up port mappings for each client node:

```bash
# Node 1 (Partition 0)
docker run --rm -p 9094:9094 --network flwr-network --name supernode-1 --detach \
  flwr/supernode:1.16.0 --insecure --superlink superlink:9092 \
  --node-config "partition-id=0 num-partitions=4" \
  --clientappio-api-address 0.0.0.0:9094 --isolation process

# Node 2 (Partition 1)
docker run --rm -p 9095:9095 --network flwr-network --name supernode-2 --detach \
  flwr/supernode:1.16.0 --insecure --superlink superlink:9092 \
  --node-config "partition-id=1 num-partitions=4" \
  --clientappio-api-address 0.0.0.0:9095 --isolation process

# Node 3 (Partition 2)
docker run --rm -p 9096:9096 --network flwr-network --name supernode-3 --detach \
  flwr/supernode:1.16.0 --insecure --superlink superlink:9092 \
  --node-config "partition-id=2 num-partitions=4" \
  --clientappio-api-address 0.0.0.0:9096 --isolation process

# Node 4 (Partition 3)
docker run --rm -p 9097:9097 --network flwr-network --name supernode-4 --detach \
  flwr/supernode:1.16.0 --insecure --superlink superlink:9092 \
  --node-config "partition-id=3 num-partitions=4" \
  --clientappio-api-address 0.0.0.0:9097 --isolation process
```

#### Step 4: Run the ServerApp (Aggregator)
```bash
docker run --rm --network flwr-network --name serverapp --detach \
  flwr/serverapp:1.16.0 --insecure --serverappio-api-address superlink:9091
```

#### Step 5: Start 4 ClientApps connected to the SuperNodes
```bash
docker run --rm --network flwr-network --name client-1 --detach flwr/clientapp:1.16.0 --insecure --clientappio-api-address supernode-1:9094
docker run --rm --network flwr-network --name client-2 --detach flwr/clientapp:1.16.0 --insecure --clientappio-api-address supernode-2:9095
docker run --rm --network flwr-network --name client-3 --detach flwr/clientapp:1.16.0 --insecure --clientappio-api-address supernode-3:9096
docker run --rm --network flwr-network --name client-4 --detach flwr/clientapp:1.16.0 --insecure --clientappio-api-address supernode-4:9097
```

#### Step 6: Trigger Federated Learning Execution
```bash
flwr run . local-deployment --stream
```

---

## 📄 License & Contact
This project is distributed under the Apache License 2.0.
- **Author:** Nguyen Dong Hai
- **Email:** donghai.pen@gmail.com | ITITWE19011@student.hcmiu.edu.vn
