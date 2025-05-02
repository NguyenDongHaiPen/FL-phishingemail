"""fl-test: A Flower / HuggingFace app."""

from flwr.common import Context, ndarrays_to_parameters, MetricsAggregationFn
from flwr.server import ServerApp, ServerAppComponents, ServerConfig
from flwr.server.strategy import FedAvg
from transformers import AutoModelForSequenceClassification

from fl_test.task import get_weights

def aggregate_metrics(metrics: list):
    """Aggregate accuracy, precision, and recall from client metrics."""
    accuracies = [m.get("accuracy", 0.0) for _, m in metrics]
    precisions = [m.get("precision", 0.0) for _, m in metrics]
    recalls = [m.get("recall", 0.0) for _, m in metrics]
    avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0.0
    avg_precision = sum(precisions) / len(precisions) if precisions else 0.0
    avg_recall = sum(recalls) / len(recalls) if recalls else 0.0
    return {"accuracy": avg_accuracy, "precision": avg_precision, "recall": avg_recall}

def server_fn(context: Context):
    # Read from config
    num_rounds = context.run_config["num-server-rounds"]
    fraction_fit = context.run_config["fraction-fit"]

    # Initialize global model
    model_name = context.run_config["model-name"]
    num_labels = context.run_config["num-labels"]
    net = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=num_labels
    )

    weights = get_weights(net)
    initial_parameters = ndarrays_to_parameters(weights)

    # Define strategy
    strategy = FedAvg(
        fraction_fit=fraction_fit,
        fraction_evaluate=1.0,
        initial_parameters=initial_parameters,
        evaluate_metrics_aggregation_fn=aggregate_metrics,

    )
    config = ServerConfig(num_rounds=num_rounds)

    return ServerAppComponents(strategy=strategy, config=config)


# Create ServerApp
app = ServerApp(server_fn=server_fn)

