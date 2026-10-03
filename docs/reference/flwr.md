# Flower (flwr) Framework Documentation

> **Source:** [https://flower.ai/docs/](https://flower.ai/docs/)
> **Version:** v1.30.x (latest stable)
> **License:** Apache 2.0

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Documentation Structure](#documentation-structure)
- [Core Concepts](#core-concepts)
- [Architecture](#architecture)
- [Quickstart (PyTorch)](#quickstart-pytorch)
- [Key API Reference](#key-api-reference)
- [Built-in Strategies](#built-in-strategies)
- [How-to Guides](#how-to-guides)
- [Simulation](#simulation)
- [Deployment](#deployment)
- [Flower Datasets](#flower-datasets)
- [Flower Intelligence](#flower-intelligence)
- [Flower Hub](#flower-hub)
- [Flower Baselines](#flower-baselines)
- [CLI Reference](#cli-reference)
- [Useful Links](#useful-links)

---

## Overview

[Flower](https://flower.ai) is a friendly, open-source **federated learning framework**. It allows researchers and developers to easily bring existing machine learning workloads into a federated setting. Flower is designed to be:

- **Framework-agnostic** — Works with PyTorch, TensorFlow, JAX, HuggingFace, scikit-learn, XGBoost, and more
- **Scalable** — Supports simulation and real-world deployment from 2 to millions of clients
- **Customizable** — Flexible strategy abstraction, custom messaging, and modular design
- **Production-ready** — Docker, Helm, TLS, authentication, and cloud deployment support

### Flower Ecosystem

| Component | Description | Docs |
|---|---|---|
| **Flower Framework** | Core FL framework — build, simulate, and deploy | [flower.ai/docs/framework/](https://flower.ai/docs/framework/) |
| **Flower Intelligence** | On-device AI with optional Confidential Remote Compute | [flower.ai/docs/intelligence/](https://flower.ai/docs/intelligence/) |
| **Flower Datasets** | Partition datasets for federated learning | [flower.ai/docs/datasets/](https://flower.ai/docs/datasets/) |
| **Flower Hub** | Discover and share Flower apps | [flower.ai/docs/hub/](https://flower.ai/docs/hub/) |
| **Flower Baselines** | Reproducible FL research baselines | [flower.ai/docs/baselines/](https://flower.ai/docs/baselines/) |
| **Example Projects** | Full Flower example projects | [flower.ai/docs/examples/](https://flower.ai/docs/examples/) |

### Coming Soon

- Flower iOS SDK
- Flower Android SDK
- Flower C++ SDK

---

## Installation

### Requirements

- **Python ≥ 3.10**

### Using pip (Recommended)

```bash
# Install the base package
python -m pip install flwr

# Install with simulation support
python -m pip install "flwr[simulation]"

# Install with REST transport layer (optional)
python -m pip install "flwr[rest]"
```

### Using conda

```bash
conda install -c conda-forge flwr
```

### Using Docker

Official Docker images are available:

```bash
# SuperLink
docker pull flwr/superlink:latest

# SuperNode
docker pull flwr/supernode:latest

# ServerApp
docker pull flwr/serverapp:latest

# ClientApp
docker pull flwr/clientapp:latest
```

### Verify Installation

```bash
python -c "import flwr; print(flwr.__version__)"
```

---

## Documentation Structure

The Flower Framework documentation is organized into four main sections:

### 1. Tutorials
- [What is Federated Learning?](https://flower.ai/docs/framework/tutorial-series-what-is-federated-learning.html)
- [Get started with Flower](https://flower.ai/docs/framework/tutorial-series-get-started-with-flower-pytorch.html)
- [Use a federated learning strategy](https://flower.ai/docs/framework/tutorial-series-use-a-federated-learning-strategy-pytorch.html)
- [Customize a Flower Strategy](https://flower.ai/docs/framework/tutorial-series-build-a-strategy-from-scratch-pytorch.html)
- [Communicate custom Messages](https://flower.ai/docs/framework/tutorial-series-customize-the-client-pytorch.html)

#### Quickstart Tutorials
- [Quickstart PyTorch](https://flower.ai/docs/framework/tutorial-quickstart-pytorch.html)
- [Quickstart TensorFlow](https://flower.ai/docs/framework/tutorial-quickstart-tensorflow.html)
- [Quickstart MLX](https://flower.ai/docs/framework/tutorial-quickstart-mlx.html)
- [Quickstart 🤗 Transformers](https://flower.ai/docs/framework/tutorial-quickstart-huggingface.html)
- [Quickstart JAX](https://flower.ai/docs/framework/tutorial-quickstart-jax.html)
- [Quickstart Pandas](https://flower.ai/docs/framework/tutorial-quickstart-pandas.html)
- [Quickstart fastai](https://flower.ai/docs/framework/tutorial-quickstart-fastai.html)
- [Quickstart PyTorch Lightning](https://flower.ai/docs/framework/tutorial-quickstart-pytorch-lightning.html)
- [Quickstart scikit-learn](https://flower.ai/docs/framework/tutorial-quickstart-scikitlearn.html)
- [Quickstart XGBoost](https://flower.ai/docs/framework/tutorial-quickstart-xgboost.html)
- [Quickstart Android](https://flower.ai/docs/framework/tutorial-quickstart-android.html)
- [Quickstart iOS](https://flower.ai/docs/framework/tutorial-quickstart-ios.html)

### 2. How-to Guides
- Build, Simulate, and Deploy sections (see below)

### 3. Explanations
- [Federated Evaluation](https://flower.ai/docs/framework/explanation-federated-evaluation.html)
- [Differential Privacy](https://flower.ai/docs/framework/explanation-differential-privacy.html)
- [Secure Aggregation Protocols](https://flower.ai/docs/framework/explanation-ref-secure-aggregation-protocols.html)
- [Flower Architecture](https://flower.ai/docs/framework/explanation-flower-architecture.html)
- [Flower Strategy Abstraction](https://flower.ai/docs/framework/explanation-flower-strategy-abstraction.html)

### 4. References
- API Reference, CLI Reference, Configuration, Example Projects, FAQ, Changelog

---

## Core Concepts

### Federated Learning with Flower

Federated Learning (FL) enables training machine learning models across decentralized data sources without sharing raw data. Flower provides the infrastructure for this paradigm.

### Key Components

| Component | Description |
|---|---|
| **`ServerApp`** | Defines the server-side logic (strategy, number of rounds, etc.) |
| **`ClientApp`** | Defines the client-side logic (training, evaluation) |
| **`SuperLink`** | Central coordination server that manages FL rounds |
| **`SuperNode`** | Client-side runtime that executes the `ClientApp` |
| **`Strategy`** | Defines how model updates are aggregated (e.g., FedAvg) |
| **`Context`** | Provides per-run state and configuration |
| **`Message`** | Communication primitive between server and clients |
| **`RecordDict`** | Container for model parameters, configs, and metrics |

### Data Types

| Type | Description |
|---|---|
| `Array` | Represents a single array (tensor) |
| `ArrayRecord` | Collection of named Arrays (e.g., model parameters) |
| `ConfigRecord` | Configuration key-value pairs |
| `MetricRecord` | Metric key-value pairs |
| `RecordDict` | Container holding ArrayRecord, ConfigRecord, MetricRecord |
| `Context` | Run context with state and configuration |
| `Message` | Communication unit with metadata |
| `UserConfig` | User-defined configuration |

---

## Architecture

Flower uses a **SuperLink / SuperNode** architecture:

```
┌─────────────┐
│  SuperLink   │ ← Central coordination server
│  (Server)    │
└──────┬───────┘
       │
  ┌────┴────┐
  │         │
┌─▼──┐  ┌──▼─┐
│SN 1│  │SN 2│  ... SuperNodes (Clients)
└─┬──┘  └─┬──┘
  │        │
┌─▼──┐  ┌─▼──┐
│CA 1│  │CA 2│  ... ClientApps (ML workloads)
└────┘  └────┘
```

- **SuperLink**: Manages the federation, coordinates rounds, runs the `ServerApp`
- **SuperNode**: Connects to the SuperLink, runs the `ClientApp`
- **ServerApp**: Contains the federated learning strategy and coordination logic
- **ClientApp**: Contains the local training and evaluation logic

---

## Quickstart (PyTorch)

### Step 1: Create a new Flower project

```bash
flwr new quickstart-pytorch --framework PyTorch --username myuser
cd quickstart-pytorch
```

This generates the following project structure:

```
quickstart-pytorch/
├── pyproject.toml       # Project metadata and Flower config
├── README.md
└── src/
    └── quickstart_pytorch/
        ├── __init__.py
        ├── client_app.py    # ClientApp definition
        ├── server_app.py    # ServerApp definition
        └── task.py          # ML model and data loading
```

### Step 2: Install dependencies

```bash
pip install -e .
```

### Step 3: Run the federation

```bash
flwr run .
```

By default, this runs a **simulation** with 10 federated nodes using `FedAvg`.

### Project Files Explained

#### `task.py` — Model and data

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision.datasets import CIFAR10
from torchvision.transforms import Compose, Normalize, ToTensor

# Define a simple CNN
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
```

#### `client_app.py` — Client logic

```python
from flwr.clientapp import ClientApp

app = ClientApp()

@app.train()
def train(message, context):
    # Get model parameters from the server message
    # Train the model on local data
    # Return updated parameters
    ...

@app.evaluate()
def evaluate(message, context):
    # Get model parameters from the server message
    # Evaluate the model on local data
    # Return evaluation metrics
    ...
```

#### `server_app.py` — Server logic

```python
from flwr.serverapp import ServerApp
from flwr.serverapp.strategy import FedAvg

app = ServerApp()

@app.main()
def main(grid, context):
    strategy = FedAvg()
    # Run federated learning for N rounds
    ...
```

#### `pyproject.toml` — Configuration

```toml
[tool.flwr.app]
publisher = "myuser"

[tool.flwr.app.components]
serverapp = "quickstart_pytorch.server_app:app"
clientapp = "quickstart_pytorch.client_app:app"

[tool.flwr.app.config]
num-server-rounds = 3

[tool.flwr.federations.local-simulation]
options.num-supernodes = 10
```

---

## Key API Reference

### `flwr.app` — Core application types

| Class | Description |
|---|---|
| `Array` | Represents a single array/tensor |
| `ArrayRecord` | Named collection of Arrays |
| `ConfigRecord` | Configuration key-value store |
| `Context` | Per-run state and configuration |
| `Error` | Error representation |
| `Message` | Communication primitive |
| `MessageType` | Message type enum |
| `Metadata` | Message metadata |
| `MetricRecord` | Metrics key-value store |
| `RecordDict` | Container for records |
| `UserConfig` | User-defined config |

**Docs:** [flwr.app API](https://flower.ai/docs/framework/ref-api/flwr.app.html)

### `flwr.clientapp` — Client application

| Class | Description |
|---|---|
| `ClientApp` | Client application entry point |

#### Client Mods (Middleware)

| Mod | Description |
|---|---|
| `adaptiveclipping_mod` | Adaptive clipping for differential privacy |
| `arrays_size_mod` | Array size tracking |
| `fixedclipping_mod` | Fixed clipping for differential privacy |
| `message_size_mod` | Message size tracking |
| `LocalDpMod` | Local differential privacy |

**Docs:** [flwr.clientapp API](https://flower.ai/docs/framework/ref-api/flwr.clientapp.html)

### `flwr.serverapp` — Server application

| Class | Description |
|---|---|
| `Grid` | Grid for sending messages to clients |
| `ServerApp` | Server application entry point |

**Docs:** [flwr.serverapp API](https://flower.ai/docs/framework/ref-api/flwr.serverapp.html)

---

## Built-in Strategies

Flower provides many built-in federated learning strategies:

| Strategy | Description |
|---|---|
| **`FedAvg`** | Federated Averaging — the baseline FL algorithm |
| **`FedAvgM`** | FedAvg with server-side momentum |
| **`FedAdam`** | Federated Adam optimizer |
| **`FedAdagrad`** | Federated Adagrad optimizer |
| **`FedYogi`** | Federated Yogi optimizer |
| **`FedProx`** | FedAvg with proximal term for heterogeneous settings |
| **`FedMedian`** | Coordinate-wise median aggregation (Byzantine-robust) |
| **`FedTrimmedAvg`** | Trimmed mean aggregation (Byzantine-robust) |
| **`QFedAvg`** | Fair resource allocation in federated learning |
| **`Krum`** | Byzantine-resilient aggregation |
| **`MultiKrum`** | Multi-Krum Byzantine-resilient aggregation |
| **`Bulyan`** | Byzantine-resilient aggregation combining Krum + trimmed mean |
| **`FedXgbBagging`** | Federated XGBoost with bagging |
| **`FedXgbCyclic`** | Federated XGBoost with cyclic training |

### Differential Privacy Strategies (Wrappers)

| Strategy | Description |
|---|---|
| `DifferentialPrivacyClientSideAdaptiveClipping` | Client-side DP with adaptive clipping |
| `DifferentialPrivacyClientSideFixedClipping` | Client-side DP with fixed clipping |
| `DifferentialPrivacyServerSideAdaptiveClipping` | Server-side DP with adaptive clipping |
| `DifferentialPrivacyServerSideFixedClipping` | Server-side DP with fixed clipping |

**Docs:** [Strategy API](https://flower.ai/docs/framework/ref-api/flwr.serverapp.strategy.html)

---

## How-to Guides

### Build

| Guide | Link |
|---|---|
| Install Flower | [Link](https://flower.ai/docs/framework/how-to-install-flower.html) |
| Configure `pyproject.toml` | [Link](https://flower.ai/docs/framework/how-to-configure-pyproject-toml.html) |
| Configure a `ClientApp` | [Link](https://flower.ai/docs/framework/how-to-configure-clients.html) |
| Design stateful ClientApps | [Link](https://flower.ai/docs/framework/how-to-design-stateful-clients.html) |
| Use strategies | [Link](https://flower.ai/docs/framework/how-to-use-strategies.html) |
| Implement strategies | [Link](https://flower.ai/docs/framework/how-to-implement-strategies.html) |
| Aggregate evaluation results | [Link](https://flower.ai/docs/framework/how-to-aggregate-evaluation-results.html) |
| Save and load model checkpoints | [Link](https://flower.ai/docs/framework/how-to-save-and-load-model-checkpoints.html) |
| Use Built-in Mods | [Link](https://flower.ai/docs/framework/how-to-use-built-in-mods.html) |
| Use Differential Privacy | [Link](https://flower.ai/docs/framework/how-to-use-differential-privacy.html) |
| Implement FedBN | [Link](https://flower.ai/docs/framework/how-to-implement-fedbn.html) |

### Simulate

| Guide | Link |
|---|---|
| Run Flower Locally (Managed SuperLink) | [Link](https://flower.ai/docs/framework/how-to-run-flower-locally.html) |
| Run Simulations | [Link](https://flower.ai/docs/framework/how-to-run-simulations.html) |

### Deploy

| Guide | Link |
|---|---|
| Run with Deployment Runtime | [Link](https://flower.ai/docs/framework/how-to-run-flower-with-deployment-engine.html) |
| Enable TLS connections | [Link](https://flower.ai/docs/framework/how-to-enable-tls-connections.html) |
| Authenticate SuperNodes | [Link](https://flower.ai/docs/framework/how-to-authenticate-supernodes.html) |
| Configure logging | [Link](https://flower.ai/docs/framework/how-to-configure-logging.html) |
| Run on GCP | [Link](https://flower.ai/docs/framework/how-to-run-flower-on-gcp.html) |
| Run on Azure | [Link](https://flower.ai/docs/framework/how-to-run-flower-on-azure.html) |
| Run on Red Hat OpenShift | [Link](https://flower.ai/docs/framework/how-to-run-flower-on-red-hat-openshift.html) |
| Authenticate Accounts (OpenID) | [Link](https://flower.ai/docs/framework/how-to-authenticate-accounts.html) |
| Configure Audit Logging | [Link](https://flower.ai/docs/framework/how-to-configure-audit-logging.html) |
| Manage Flower Federations | [Link](https://flower.ai/docs/framework/how-to-manage-flower-federations.html) |

### Docker Deployment

| Guide | Link |
|---|---|
| Quickstart with Docker | [Link](https://flower.ai/docs/framework/docker/tutorial-quickstart-docker.html) |
| Enable TLS for Docker | [Link](https://flower.ai/docs/framework/docker/enable-tls.html) |
| Persist SuperLink State | [Link](https://flower.ai/docs/framework/docker/persist-superlink-state.html) |
| Quickstart Docker Compose | [Link](https://flower.ai/docs/framework/docker/tutorial-quickstart-docker-compose.html) |
| Deploy on Multiple Machines | [Link](https://flower.ai/docs/framework/docker/tutorial-deploy-on-multiple-machines.html) |

### Helm Deployment (Kubernetes)

| Guide | Link |
|---|---|
| Deploy SuperLink using Helm | [Link](https://flower.ai/docs/framework/helm/how-to-deploy-superlink-using-helm.html) |
| Deploy SuperNode using Helm | [Link](https://flower.ai/docs/framework/helm/how-to-deploy-supernode-using-helm.html) |

---

## Simulation

Flower provides a powerful simulation engine for rapid prototyping:

```bash
# Run simulation with default settings
flwr run .

# Run with custom number of supernodes
flwr run . --run-config num-server-rounds=5
```

Configure simulation in `pyproject.toml`:

```toml
[tool.flwr.federations.local-simulation]
options.num-supernodes = 10
options.backend.client-resources.num-cpus = 2
options.backend.client-resources.num-gpus = 0.5
```

---

## Deployment

### Deployment Runtime

For production deployments, Flower uses the **Deployment Runtime** with separate processes:

```bash
# Start the SuperLink
flower-superlink --insecure

# Start SuperNode 1
flower-supernode --insecure --superlink 127.0.0.1:9092

# Start SuperNode 2
flower-supernode --insecure --superlink 127.0.0.1:9092

# Run the ServerApp
flwr run . --run-config num-server-rounds=3
```

### TLS & Security

- TLS support for encrypted communication
- SuperNode authentication with public/private keys
- Account authentication via OpenID Connect
- Audit logging

---

## Flower Datasets

The `flwr-datasets` library provides tools for partitioning datasets for federated learning:

```bash
pip install flwr-datasets
```

```python
from flwr_datasets import FederatedDataset

fds = FederatedDataset(dataset="cifar10", partitioners={"train": 10})
partition = fds.load_partition(0)
```

**Docs:** [flower.ai/docs/datasets/](https://flower.ai/docs/datasets/)

---

## Flower Intelligence

Flower Intelligence provides **on-device AI** capabilities with optional Confidential Remote Compute.

**Docs:** [flower.ai/docs/intelligence/](https://flower.ai/docs/intelligence/)

---

## Flower Hub

Flower Hub is a platform to discover and share Flower apps.

**Docs:** [flower.ai/docs/hub/](https://flower.ai/docs/hub/)

---

## Flower Baselines

Flower Baselines provides reproducible implementations of well-known FL research papers.

**Docs:** [flower.ai/docs/baselines/](https://flower.ai/docs/baselines/)

---

## CLI Reference

### Key Commands

```bash
# Create a new Flower project
flwr new <project-name> --framework <framework> --username <username>

# Run a Flower project
flwr run <path>

# Install a Flower app
flwr install <app>

# Log in to Flower Hub
flwr login

# Start the SuperLink server
flower-superlink [options]

# Start a SuperNode client
flower-supernode [options]
```

**Full CLI docs:** [Flower CLI Reference](https://flower.ai/docs/framework/ref-api-cli.html)

---

## Useful Links

| Resource | URL |
|---|---|
| **Documentation** | https://flower.ai/docs/ |
| **Framework Docs** | https://flower.ai/docs/framework/ |
| **GitHub** | https://github.com/flwrlabs/flower |
| **PyPI** | https://pypi.org/project/flwr/ |
| **Slack Community** | https://flower.ai/join-slack |
| **Discussion Forum** | https://discuss.flower.ai |
| **Blog** | https://flower.ai/blog/ |
| **YouTube** | https://www.youtube.com/@flowerlabs |
| **Configuration Reference** | https://flower.ai/docs/framework/ref-flower-configuration.html |
| **Example Projects** | https://flower.ai/docs/framework/ref-example-projects.html |
| **FAQ** | https://flower.ai/docs/framework/ref-faq.html |
| **Changelog** | https://flower.ai/docs/framework/ref-changelog.html |

---

## Migration Guides

| Guide | Link |
|---|---|
| Upgrade to Flower 1.0 | [Link](https://flower.ai/docs/framework/how-to-upgrade-to-flower-1.0.html) |
| Upgrade to Flower 1.13 | [Link](https://flower.ai/docs/framework/how-to-upgrade-to-flower-1.13.html) |
| Upgrade to Message API | [Link](https://flower.ai/docs/framework/how-to-upgrade-to-message-api.html) |
| Upgrade to Flower 1.28 | [Link](https://flower.ai/docs/framework/how-to-upgrade-to-flower-1.28.html) |
| Migrate from OpenFL | [Link](https://flower.ai/docs/framework/how-to-migrate-from-openfl.html) |

---

*Last updated from Flower documentation v1.30.x*
