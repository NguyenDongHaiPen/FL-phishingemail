###  `README.md`

```markdown
# FL-phishingemail 

This project implements a Federated Learning (FL) system to detect phishing emails using HuggingFace Transformers, Flower, and PyTorch. It also includes a Thunderbird extension that locally classifies emails using the trained model.

---

##  Project Structure

```
fl-test/
├── fl_test/                # Flower server and client code
├── saved_model/           # Trained PyTorch model (.pt) via FL
├── thunderbird-extension/ # Thunderbird extension folders (scripts, manifest, UI)
├── serverapp.Dockerfile   # Dockerfile for FL server
├── clientapp.Dockerfile   # Dockerfile for FL clients
├── pyproject.toml         # Flower project and dependencies
├── sample_logs.txt        # Example training logs
└── README.md              # This file
```

---

##  1. Training Setup (Simulation)

###  Requirements

- Python 3.9+
- Git LFS: `brew install git-lfs`
- Install dependencies:
  ```bash
  pip install -e .
  ```

### ▶ Run Training with Flower Simulation Engine

```bash
cd fl-test
flwr run .
```

This uses `distilbert-base-uncased` as a base model and simulates federated learning across multiple clients.  
Final trained model is saved as:

```
saved_model/model.pt
```

---

##  2. Thunderbird Extension: Integrate Model

###  Steps to Embed the Model:

1. Copy `saved_model/model.pt` into the Thunderbird extension’s `model/` folder
2. Ensure your extension's backend (e.g., Python script or WebExtension) loads the model:
   ```python
   model = torch.load("model/model.pt", map_location=torch.device("cpu"))
   ```
3. Use this model to classify emails as "phishing" or "safe" directly inside Thunderbird

---

##  3. Load Extension into Thunderbird

###  Steps:

1. Open Thunderbird  
2. Go to `Tools` → `Add-ons and Themes`  
3. Click ⚙️ → **"Install Add-on From File..."**  
4. Choose your `.xpi` file or zipped extension folder  
5. Restart Thunderbird  
6. Test on an email — the classification runs locally using the trained model!

---

## 🐳 4. Docker-Based Federated Learning Deployment

Run the full system using **Flower’s Deployment Engine** with Docker.

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

### Step 3: Start the SuperNodes

```bash
# Start 4 SuperNodes
docker run --rm -p 9094:9094 --network flwr-network --name supernode-1 --detach \
  flwr/supernode:1.16.0 --insecure --superlink superlink:9092 \
  --node-config "partition-id=0 num-partitions=4" \
  --clientappio-api-address 0.0.0.0:9094 --isolation process

docker run --rm -p 9095:9095 --network flwr-network --name supernode-2 --detach \
  flwr/supernode:1.16.0 --insecure --superlink superlink:9092 \
  --node-config "partition-id=1 num-partitions=4" \
  --clientappio-api-address 0.0.0.0:9095 --isolation process

docker run --rm -p 9096:9096 --network flwr-network --name supernode-3 --detach \
  flwr/supernode:1.16.0 --insecure --superlink superlink:9092 \
  --node-config "partition-id=2 num-partitions=4" \
  --clientappio-api-address 0.0.0.0:9096 --isolation process

docker run --rm -p 9097:9097 --network flwr-network --name supernode-4 --detach \
  flwr/supernode:1.16.0 --insecure --superlink superlink:9092 \
  --node-config "partition-id=3 num-partitions=4" \
  --clientappio-api-address 0.0.0.0:9097 --isolation process
```

### Step 4: Start the ServerApp

```bash
docker run --rm --network flwr-network --name serverapp --detach \
  flwr/serverapp:1.16.0 --insecure --serverappio-api-address superlink:9091
```

### Step 5: Start the ClientApps

```bash
docker run --rm --network flwr-network --name client-1 --detach \
  flwr/clientapp:1.16.0 --insecure --clientappio-api-address supernode-1:9094

docker run --rm --network flwr-network --name client-2 --detach \
  flwr/clientapp:1.16.0 --insecure --clientappio-api-address supernode-2:9095

docker run --rm --network flwr-network --name client-3 --detach \
  flwr/clientapp:1.16.0 --insecure --clientappio-api-address supernode-3:9096

docker run --rm --network flwr-network --name client-4 --detach \
  flwr/clientapp:1.16.0 --insecure --clientappio-api-address supernode-4:9097
```

### Step 6: Run Federated Training

```bash
flwr run . local-deployment --stream
```

---

## 📚 Resources

- [Flower Documentation](https://flower.ai/docs/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- [Thunderbird Extension Dev Guide](https://developer.thunderbird.net/)
- [Git LFS Setup](https://git-lfs.github.com)

---

## 📄 License

Apache License 2.0

---

## ✨ Acknowledgements

Project by **Nguyen Dong Hai**  
Includes open-source tools: Flower, HuggingFace Transformers, PyTorch, Mozilla Thunderbird
```
