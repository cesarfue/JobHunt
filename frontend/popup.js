document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("extract");
  const status = document.getElementById("status");
  let timeoutId = null;

  // Restore previous state
  chrome.storage.local.get(
    ["jobStatus", "jobMessage", "loadingStartTime"],
    (data) => {
      if (data.jobStatus === "loading") {
        const startTime = data.loadingStartTime || Date.now();
        const elapsed = Date.now() - startTime;
        const remaining = 30000 - elapsed;

        // If already timed out, show error
        if (remaining <= 0) {
          button.disabled = false;
          button.textContent = "HIRE ME";
          const errorMessage = "Request timed out. Please try again.";
          status.textContent = errorMessage;
          status.className = "visible status-error";
          chrome.storage.local.set({
            jobStatus: "error",
            jobMessage: errorMessage,
          });
        } else {
          // Still loading, show loading state and set remaining timeout
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

          // Set timeout for remaining time
          timeoutId = setTimeout(() => {
            button.disabled = false;
            button.textContent = "HIRE ME";
            const errorMessage = "Request timed out. Please try again.";
            status.textContent = errorMessage;
            status.className = "visible status-error";

            chrome.storage.local.set({
              jobStatus: "error",
              jobMessage: errorMessage,
            });
          }, remaining);
        }
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
    },
  );

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

    // Save loading state to storage with timestamp
    chrome.storage.local.set({
      jobStatus: "loading",
      jobMessage: "Processing...",
      loadingStartTime: Date.now(),
    });

    // Set timeout for 30 seconds
    timeoutId = setTimeout(() => {
      button.disabled = false;
      button.textContent = "HIRE ME";
      const errorMessage = "Request timed out. Please try again.";
      status.textContent = errorMessage;
      status.className = "visible status-error";

      chrome.storage.local.set({
        jobStatus: "error",
        jobMessage: errorMessage,
      });
    }, 30000);

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
      // Clear timeout since we got a response
      if (timeoutId) {
        clearTimeout(timeoutId);
        timeoutId = null;
      }

      const data = message.data;

      button.disabled = false;
      button.textContent = "HIRE ME";

      if (data.status === "success") {
        const successMessage = `Documents created for ${data.company}`;
        status.textContent = successMessage;
        status.className = "visible status-success";

        // Save to storage (remove timestamp)
        chrome.storage.local.set({
          jobStatus: "success",
          jobMessage: successMessage,
        });
        chrome.storage.local.remove(["loadingStartTime"]);
      } else {
        const errorMessage = `Error: ${data.message}`;
        status.textContent = errorMessage;
        status.className = "visible status-error";

        // Save to storage (remove timestamp)
        chrome.storage.local.set({
          jobStatus: "error",
          jobMessage: errorMessage,
        });
        chrome.storage.local.remove(["loadingStartTime"]);
      }
    }
  });
});
