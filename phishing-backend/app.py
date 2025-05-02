from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F  # For softmax

class EmailInput(BaseModel):
    content: str

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
model.load_state_dict(torch.load("model.pt", map_location="cpu"))
model.eval()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(data: EmailInput):
    inputs = tokenizer(data.content, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        phishing_prob = probs[0][1].item()  # Probability of phishing

        # Debug print statements
        print("Prediction logits:", outputs.logits)
        print("Softmax probabilities:", probs)
        print("Phishing probability:", phishing_prob)
        print("Received content:", data.content)


    threshold = 0.90  # adjust if needed
    label = "Phishing" if phishing_prob >= threshold else "Safe"

    return {"label": label, "confidence": round(phishing_prob, 4)}
