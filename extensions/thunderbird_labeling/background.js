// Persistent labeled emails list
async function getLabeledEmails() {
  const result = await browser.storage.local.get("labeledEmails");
  return result.labeledEmails || [];
}

async function saveLabeledEmails(emails) {
  await browser.storage.local.set({ labeledEmails: emails });
}

async function getEmailContent(messageId) {
  const full = await browser.messages.getFull(messageId);

  function extractText(part) {
    if (part.contentType === "text/plain" && part.body) {
      return part.body;
    }
    if (part.parts) {
      for (const subPart of part.parts) {
        const result = extractText(subPart);
        if (result) return result;
      }
    }
    return null;
  }

  const body = extractText(full) || "[No readable text found]";
  return { body };
}

async function handleLabel(message, label) {
  const content = await getEmailContent(message.id);
  const emails = await getLabeledEmails();

  // Avoid duplicates
  const alreadyExists = emails.some(
    (e) => e.body === content.body && e.label === label
  );
  if (!alreadyExists) {
    emails.push({ body: content.body, label });
    await saveLabeledEmails(emails);
    console.log(`Labeled as ${label}`);
  } else {
    console.log("Email already labeled.");
  }
}

async function downloadData() {
  const emails = await getLabeledEmails();
  if (emails.length === 0) {
    alert("No labeled emails to download.");
    return;
  }

  const csvRows = ["Email Text,Email Type"];
  for (const email of emails) {
    const safeBody = email.body.replace(/\n/g, " ").replace(/"/g, "'");
    csvRows.push(`"${safeBody}","${email.label}"`);
  }
  const blob = new Blob([csvRows.join("\n")], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  browser.downloads.download({
    url: url,
    filename: "labeled_emails.csv",
    saveAs: true,
  });
}

// Context menu
browser.menus.create({
  id: "mark-phishing",
  title: "Mark as Phishing",
  contexts: ["message_list"],
});

browser.menus.create({
  id: "mark-safe",
  title: "Mark as Safe",
  contexts: ["message_list"],
});

browser.menus.onClicked.addListener((info, tab) => {
  const label =
    info.menuItemId === "mark-phishing" ? "Phishing Email" : "Safe Email";
  browser.mailTabs.getSelectedMessages().then((messages) => {
    for (const message of messages.messages) {
      handleLabel(message, label);
    }
  });
});

// Toolbar button
browser.browserAction.onClicked.addListener(() => {
  showLabelStats(); //  shows stats in console
  downloadData(); //  downloads the CSV as before
});

//label stats
async function showLabelStats() {
  const emails = await getLabeledEmails();

  const phishing = emails.filter((e) => e.label === "Phishing Email").length;
  const safe = emails.filter((e) => e.label === "Safe Email").length;

  const total = emails.length;
  console.log(` Labeled Emails Summary:`);
  console.log(` Phishing Emails: ${phishing}`);
  console.log(` Safe Emails: ${safe}`);
  console.log(` Total: ${emails.length}`);

  const summary = `Phishing Emails: ${phishing}\nSafe Emails: ${safe}\nTotal: ${total}`;
  alert(summary);

  console.log(summary);
  // Optional: list subject/preview
  emails.forEach((e, i) => {
    const preview = e.body.slice(0, 50).replace(/\n/g, " ");
    console.log(`${i + 1} ${e.label} — "${preview}..."`);
  });
}

browser.runtime.onMessage.addListener((message) => {
  if (message.action === "download_csv") {
    downloadData(); // your existing function
  }
});
