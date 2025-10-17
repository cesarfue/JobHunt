document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("extract");
  const status = document.getElementById("status");

  // Restore previous state
  chrome.storage.local.get(["jobStatus", "jobMessage"], (data) => {
    if (data.jobStatus === "loading") {
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
    } else if (data.jobStatus === "success") {
      button.disabled = false;
      button.textContent = "HIRE ME";
      status.textContent = data.jobMessage;
      status.className = "visible status-success";
    } else if (data.jobStatus === "error") {
      button.disabled = false;
      button.textContent = "HIRE ME";
      status.textContent = data.jobMessage;
      status.className = "visible status-error";
    }
  });

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

    // Save loading state to storage
    chrome.storage.local.set({
      jobStatus: "loading",
      jobMessage: "Processing...",
    });

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
        const successMessage = `Documents created for ${data.company}`;
        status.textContent = successMessage;
        status.className = "visible status-success";

        // Save to storage
        chrome.storage.local.set({
          jobStatus: "success",
          jobMessage: successMessage,
        });
      } else {
        const errorMessage = `Error: ${data.message}`;
        status.textContent = errorMessage;
        status.className = "visible status-error";

        // Save to storage
        chrome.storage.local.set({
          jobStatus: "error",
          jobMessage: errorMessage,
        });
      }
    }
  });
});
