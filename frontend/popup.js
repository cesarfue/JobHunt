document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("extract");
  const status = document.getElementById("status");

  // Click handler
  button.addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    // Set loading state
    button.disabled = true;
    button.textContent = "Processing...";
    status.innerHTML = `
      <div class="loading-dots">
        <span class="loading-dot"></span>
        <span class="loading-dot"></span>
        <span class="loading-dot"></span>
      </div>
    `;
    status.className = "visible";

    // Send message to content script (don't wait for response)
    try {
      chrome.tabs.sendMessage(tab.id, { action: "EXPORT_JOB_OFFER" });
    } catch (error) {
      // Ignore errors, we'll get the result via onMessage listener
    }
  });

  // Listen for results
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "JOB_RESULT") {
      const data = message.data;

      button.disabled = false;
      button.textContent = "HIRE ME";

      if (data.status === "success") {
        status.textContent = `Documents created for ${data.company}`;
        status.className = "visible status-success";
      } else {
        status.textContent = `Error: ${data.message}`;
        status.className = "visible status-error";
      }
    }
  });
});
