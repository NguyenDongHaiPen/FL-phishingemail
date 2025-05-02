
document.getElementById("checkBtn").addEventListener("click", async () => {
  const resultText = document.getElementById("result");
  const confidenceText = document.getElementById("confidence");
  const barFill = document.getElementById("bar-fill");

  try {
    const [tab] = await messenger.tabs.query({ active: true, currentWindow: true });
    const message = await messenger.messageDisplay.getDisplayedMessage(tab.id);

    if (!message) {
      resultText.innerText = "Status: No message selected.";
      confidenceText.innerText = "-";
      barFill.style.width = "0%";
      barFill.style.backgroundColor = "gray";
      return;
    }

    const full = await messenger.messages.getFull(message.id);

    function findPart(parts, type) {
      for (const part of parts) {
        if (part.contentType === type && part.body) {
          return part.body;
        } else if (part.parts) {
          const found = findPart(part.parts, type);
          if (found) return found;
        }
      }
      return null;
    }

    let content = findPart(full.parts, "text/plain");
    if (!content) {
      const html = findPart(full.parts, "text/html");
      if (html) {
        const temp = document.createElement("div");
        temp.innerHTML = html;
        content = temp.innerText;
      }
    }

    if (!content || content.trim() === "") {
      alert("No usable content found in this email.");
      return;
    }

    console.log("Extracted email content:", content);

    const res = await fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: content.trim() })
    });

    const data = await res.json();
    const confidence = data.confidence;
    const label = data.label;

    resultText.innerText = `Status: ${label}`;
    confidenceText.innerText = `${(confidence * 100).toFixed(2)}%`;
    barFill.style.width = `${(confidence * 100).toFixed(0)}%`;

    if (confidence >= 0.85) {
      barFill.style.backgroundColor = "red";
    } else if (confidence >= 0.5) {
      barFill.style.backgroundColor = "orange";
    } else {
      barFill.style.backgroundColor = "green";
    }

  } catch (err) {
    console.error(err);
    resultText.innerText = "Status: Error checking email.";
    confidenceText.innerText = "-";
    barFill.style.width = "0%";
    barFill.style.backgroundColor = "gray";
  }
});
