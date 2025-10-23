// Content script that runs on job pages
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "EXPORT_JOB_OFFER") {
    const pageContent = document.body.innerText;
    const pageTitle = document.title;
    const pageUrl = window.location.href;

    // Send to backend
    fetch("http://127.0.0.1:5000/api/job", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        content: pageContent,
        title: pageTitle,
        url: pageUrl,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        // Send result back to popup
        chrome.runtime.sendMessage({
          action: "JOB_RESULT",
          data: data,
        });
      })
      .catch((err) => {
        chrome.runtime.sendMessage({
          action: "JOB_RESULT",
          data: {
            status: "error",
            message: "Cannot connect to backend. Is Flask running?",
          },
        });
      });

    // Return true to indicate we'll send a response asynchronously
    return true;
  }
});
