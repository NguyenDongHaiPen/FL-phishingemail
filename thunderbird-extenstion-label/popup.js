async function getLabeledEmails() {
    const result = await browser.storage.local.get("labeledEmails");
    return result.labeledEmails || [];
  }
  
  async function saveLabeledEmails(emails) {
    await browser.storage.local.set({ labeledEmails: emails });
  }
  
  function showSummary(emails) {
    const phishing = emails.filter(e => e.label === "Phishing Email").length;
    const safe = emails.filter(e => e.label === "Safe Email").length;
    const total = emails.length;
  
    document.getElementById("stats").textContent =
      `Phishing: ${phishing} | Safe: ${safe} | Total: ${total}`;
  
    const container = document.getElementById("previews");
    container.innerHTML = "";
    emails.forEach((e, i) => {
      const div = document.createElement("div");
      div.className = "email-preview";
      div.textContent = `${i + 1}. [${e.label}] ${e.body.slice(0, 60).replace(/\\n/g, " ")}...`;
      container.appendChild(div);
    });
  }
  
  async function downloadData() {
    await browser.runtime.sendMessage({ action: "download_csv" });
  }
  
  
  async function resetData() {
    await browser.storage.local.remove("labeledEmails");
    document.getElementById("stats").textContent = "Reset complete. No labeled emails.";
    document.getElementById("previews").innerHTML = "";
  }
  
  document.getElementById("downloadBtn").addEventListener("click", downloadData);
  document.getElementById("resetBtn").addEventListener("click", resetData);
  
  getLabeledEmails().then(showSummary);
  