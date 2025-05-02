# """fl-test: A Flower / HuggingFace app."""

# import torch
# from flwr.client import ClientApp, NumPyClient
# from flwr.common import Context
# from transformers import AutoModelForSequenceClassification

# from fl_test.task import get_weights, load_data, set_weights, test, train


# # Flower client
# class FlowerClient(NumPyClient):
#     def __init__(self, net, trainloader, testloader, local_epochs):
#         self.net = net
#         self.trainloader = trainloader
#         self.testloader = testloader
#         self.local_epochs = local_epochs
#         self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#         self.net.to(self.device)

#     def fit(self, parameters, config):
#         set_weights(self.net, parameters)
#         train(self.net, self.trainloader, epochs=self.local_epochs, device=self.device)
#         return get_weights(self.net), len(self.trainloader), {}

#     def evaluate(self, parameters, config):
#         set_weights(self.net, parameters)
#         loss, accuracy, precision, recall = test(self.net, self.testloader, self.device)
#         print(f"INFO : Evaluation -- Loss: {loss:.8f}, Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}")
#         # Return loss, number of examples, and a dictionary with the three metrics
#         return float(loss), len(self.testloader), {
#             "accuracy": accuracy,
#             "precision": precision,
#             "recall": recall,
#         }


# def client_fn(context: Context):

#     # Get this client's dataset partition
#     partition_id = context.node_config["partition-id"]
#     num_partitions = context.node_config["num-partitions"]
#     model_name = context.run_config["model-name"]
#     trainloader, valloader = load_data(partition_id, num_partitions, model_name)

#     # Load model
#     num_labels = context.run_config["num-labels"]
#     net = AutoModelForSequenceClassification.from_pretrained(
#         model_name, num_labels=num_labels
#     )

#     local_epochs = context.run_config["local-epochs"]

#     # Return Client instance
#     return FlowerClient(net, trainloader, valloader, local_epochs).to_client()


# # Flower ClientApp
# app = ClientApp(
#     client_fn,
# )


import os
import torch
from flwr.common import Context
from flwr.client import ClientApp, NumPyClient
from transformers import AutoModelForSequenceClassification
from fl_test.task import train, test, get_weights, set_weights, load_data

# Folder to save the model checkpoints
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
        print("ℹ️ No saved model found. Loading fresh model.")
    return net

def client_fn(context: Context) -> NumPyClient:
    # Correct config usage
    partition_id = context.node_config["partition-id"]
    num_partitions = context.node_config["num-partitions"]
    model_name = context.run_config["model-name"]
    num_labels = context.run_config["num-labels"]
    local_epochs = context.run_config["local-epochs"]

    # Load model (with checkpoint if exists)
    net = load_model(model_name=model_name, num_labels=num_labels)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net.to(device)

    # Load partitioned dataset
    trainloader, testloader = load_data(partition_id, num_partitions, model_name)

    # Define Flower Client inside
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

# Flower ClientApp
app = ClientApp(
    client_fn,
)