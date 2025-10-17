document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("extract");
  const status = document.getElementById("status");

  // Restore state when popup opens
  chrome.storage.local.get(["jobStatus", "jobMessage"], (data) => {
    // Only show previous completed states (success or error)
    if (data.jobStatus === "success" || data.jobStatus === "error") {
      updateUI(data.jobStatus, data.jobMessage);
    }
    // Clear loading state if it was stuck
    if (data.jobStatus === "loading") {
      chrome.storage.local.remove(["jobStatus", "jobMessage"]);
    }
  });

  // Click handler
  button.addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    // Set loading state
    updateUI("loading", "Processing your application...");

    // Save to storage immediately
    chrome.storage.local.set({
      jobStatus: "loading",
      jobMessage: "Processing your application...",
    });

    // Send message to content script
    chrome.tabs.sendMessage(
      tab.id,
      { action: "EXPORT_JOB_OFFER" },
      (response) => {
        // Handle no response (content script not loaded)
        if (chrome.runtime.lastError) {
          updateUI("error", "Please refresh the page and try again");
          chrome.storage.local.set({
            jobStatus: "error",
            jobMessage: "Please refresh the page and try again",
          });
        }
      },
    );
  });

  // Listen for storage changes (when background script updates)
  chrome.storage.onChanged.addListener((changes, areaName) => {
    if (areaName === "local") {
      if (changes.jobStatus) {
        const statusVal = changes.jobStatus.newValue;
        const message = changes.jobMessage?.newValue || "";
        updateUI(statusVal, message);
      }
    }
  });

  function updateUI(statusVal, message) {
    if (statusVal === "loading") {
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
    } else if (statusVal === "success") {
      button.disabled = false;
      button.textContent = "HIRE ME";
      status.textContent = message;
      status.className = "visible status-success";
    } else if (statusVal === "error") {
      button.disabled = false;
      button.textContent = "HIRE ME";
      status.textContent = message;
      status.className = "visible status-error";
    }
  }
});
