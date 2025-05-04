# 🛡️ Federated Learning for Phishing Email Detection

This project demonstrates a complete Federated Learning (FL) pipeline to detect phishing emails using HuggingFace Transformers, Flower, and PyTorch. It includes both a server–client FL training system and a Thunderbird extension that classifies emails locally using the trained model — ensuring privacy, security, and decentralization.


## 🛠️ Built With

| Tool/Framework        | Purpose                                |
|-----------------------|----------------------------------------|
| [Flower](https://flower.ai)              | Federated learning orchestration     |
| [PyTorch](https://pytorch.org/)          | Model training and inference         |
| [HuggingFace Transformers](https://huggingface.co/) | Pretrained NLP models               |
| [Docker](https://www.docker.com/)        | Containerized deployment             |
| [Mozilla Thunderbird](https://www.thunderbird.net/) | Email platform for extension testing |

## 🗂 Project Structure

```
fl-test/
├── fl_test/                # FL server and client code
├── saved_model/           # Trained model (.pt)
├── thunderbird-extension/ # Thunderbird extension (backend, manifest, UI)
├── serverapp.Dockerfile   # Dockerfile for FL server
├── clientapp.Dockerfile   # Dockerfile for FL clients
├── pyproject.toml         # Flower config and Python dependencies
└── README.md              # This file
```
## 🧰 Getting Started

### Clone the Repository

```bash
git clone https://github.com/NguyenDongHaiPen/FL-phishingemail.git
cd FL-phishingemail
```

### Set Up the Environment

Make sure Python 3.9+ is installed.

```bash
pip install -e .
```

(Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

### Run a Sample Simulation

```bash
flwr run .
```

You should see logs of federated rounds, client updates, and evaluation results.

---

## 🚀 1. Training Setup (Simulation Engine)

### 📦 Requirements

- Python 3.9+
- Install dependencies:
  ```bash
  pip install -e .
  ```

### ▶️ Run Local Federated Simulation

```bash
cd "flowerfolder"
flwr run .
```

This simulates a federated setup using Flower's local simulation engine across multiple clients. Final trained model is saved to `saved_model/model.pt`.

## 📨 2. Integrate Model into Thunderbird Extension

1. Copy the trained model to the extension:
   ```bash
   cp saved_model/model.pt thunderbird-extension/model/
   ```

2. Load the model in the extension backend:
   ```python
   model = torch.load("model/model.pt", map_location=torch.device("cpu"))
   ```

3. Use the model to classify emails locally inside Thunderbird.

## 🧪 3. Load the Extension into Thunderbird

1. Open Thunderbird
2. Go to Tools → Add-ons and Themes
3. Click ⚙️ → “Install Add-on From File...”
4. Select the `.xpi` or zipped extension folder
5. Restart Thunderbird
6. Test classification by selecting an email

## 🐳 4. Docker-Based Federated Training Deployment

Run the full system using Flower’s Deployment Engine and Docker containers.

### Step 0: Create Docker Network

```bash
docker network create --driver bridge flwr-network
```

### Step 1: Build the ServerApp Image

```bash
docker build -t flwr/serverapp:1.16.0 -f serverapp.Dockerfile .
```

### Step 2: Start the SuperLink

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

### Step 3: Start SuperNodes

Repeat this for all 4 partitions with different ports:
```bash
docker run --rm -p 9094:9094 --network flwr-network --name supernode-1 --detach \
  flwr/supernode:1.16.0 --insecure --superlink superlink:9092 \
  --node-config "partition-id=0 num-partitions=4" \
  --clientappio-api-address 0.0.0.0:9094 --isolation process
```

### Step 4: Start the ServerApp

```bash
docker run --rm --network flwr-network --name serverapp --detach \
  flwr/serverapp:1.16.0 --insecure --serverappio-api-address superlink:9091
```

### Step 5: Start ClientApps

Repeat for all 4 clients:
```bash
docker run --rm --network flwr-network --name client-1 --detach \
  flwr/clientapp:1.16.0 --insecure --clientappio-api-address supernode-1:9094
```

### Step 6: Run Federated Learning

```bash
flwr run . local-deployment --stream
```

## 📚 References

- [Flower Documentation](https://flower.ai/docs/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- [Thunderbird Extension Dev](https://developer.thunderbird.net/)
- [PyTorch](https://pytorch.org/)

## 📄 License

Apache License 2.0

## 👤 Author

**Nguyen Dong Hai**  
Research project (2024/2025): *Federated Learning for Phishing Email Detection*

<!-- CONTACT -->
## Contact

Nguyen Dong Hai - donghai.pen@gmail.com - ITITWE19011@student.hcmiu.edu.vn - Hai10.Nguyen@live.uwe.ac.uk

Project Link: [](https://github.com/NguyenDongHaiPen/FL-phishingemail)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

