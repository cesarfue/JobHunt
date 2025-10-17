document.getElementById("extract").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // Send a message to the content script
  chrome.tabs.sendMessage(tab.id, { action: "EXPORT_JOB_OFFER" });
});
