// Listen for results from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "JOB_RESULT") {
    const data = message.data;

    const jobStatus = data.status === "success" ? "success" : "error";
    const jobMessage =
      data.status === "success"
        ? `Documents created for ${data.company}`
        : `Error: ${data.message}`;

    // Save result to storage
    chrome.storage.local.set({ jobStatus, jobMessage });
  }
});
