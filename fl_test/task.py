"""fl-test: A Flower / HuggingFace app."""

import warnings
from collections import OrderedDict
import torch
import transformers
from datasets.utils.logging import disable_progress_bar
from evaluate import load as load_metric
from flwr_datasets import FederatedDataset
from flwr_datasets.partitioner import IidPartitioner
from torch.optim import AdamW
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, DataCollatorWithPadding
from datasets import load_dataset

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
disable_progress_bar()
transformers.logging.set_verbosity_error()

fds = None  # Cache FederatedDataset



def load_data(partition_id: int, num_partitions: int, model_name: str):
    """Load phishing email dataset (training and eval)."""
    global fds
    if fds is None:
        partitioner = IidPartitioner(num_partitions=num_partitions)
        fds = FederatedDataset(
            dataset="zefang-liu/phishing-email-dataset",
            partitioners={"train": partitioner},
        )

    partition = fds.load_partition(partition_id)
    partition_train_test = partition.train_test_split(test_size=0.2, seed=42)

    # Drop Unnamed column if it exists
    if "Unnamed: 0" in partition_train_test["train"].column_names:
        partition_train_test = partition_train_test.remove_columns(["Unnamed: 0"])

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize_function(examples):
        """Ensure text column is properly formatted before tokenization"""
        if "Email Text" not in examples:
            raise KeyError("Expected column 'Email Text' missing from dataset.")

        texts = [str(text) if text is not None else "" for text in examples["Email Text"]]
        return tokenizer(texts, truncation=True, padding=True, max_length=512)

    partition_train_test = partition_train_test.map(tokenize_function, batched=True)

    # Remove original text column and rename label
    partition_train_test = partition_train_test.remove_columns(["Email Text"])
    partition_train_test = partition_train_test.rename_column("Email Type", "labels")

    # Convert label values to numerical format
    partition_train_test = partition_train_test.map(
        lambda x: {"labels": 1 if x["labels"] == "Phishing Email" else 0}
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    trainloader = DataLoader(
        partition_train_test["train"],
        shuffle=True,
        batch_size=32,
        collate_fn=data_collator,
    )

    testloader = DataLoader(
        partition_train_test["test"], batch_size=32, collate_fn=data_collator
    )

    return trainloader, testloader





def train(net, trainloader, epochs, device):
    optimizer = AdamW(net.parameters(), lr=5e-5)
    net.train()
    for _ in range(epochs):
        for batch in trainloader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = net(**batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()


def test(net, testloader, device):
    # Initialize metrics
    accuracy_metric = load_metric("accuracy")
    precision_metric = load_metric("precision")
    recall_metric = load_metric("recall")
    
    total_loss = 0
    net.eval()
    for batch in testloader:
        batch = {k: v.to(device) for k, v in batch.items()}
        with torch.no_grad():
            outputs = net(**batch)
        logits = outputs.logits
        total_loss += outputs.loss.item()
        predictions = torch.argmax(logits, dim=-1)
        accuracy_metric.add_batch(predictions=predictions, references=batch["labels"])
        precision_metric.add_batch(predictions=predictions, references=batch["labels"])
        recall_metric.add_batch(predictions=predictions, references=batch["labels"])
    
    # Average loss computed over total examples
    avg_loss = total_loss / len(testloader.dataset)
    accuracy = accuracy_metric.compute()["accuracy"]
    # Specify average="binary" to compute precision and recall for binary classification
    precision = precision_metric.compute(average="binary")["precision"]
    recall = recall_metric.compute(average="binary")["recall"]
    return avg_loss, accuracy, precision, recall


def get_weights(net):
    return [val.cpu().numpy() for _, val in net.state_dict().items()]


def set_weights(net, parameters):
    params_dict = zip(net.state_dict().keys(), parameters)
    state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
    net.load_state_dict(state_dict, strict=True)
