chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action !== "EXPORT_JOB_OFFER") return;

  const url = window.location.href;
  const title =
    document.querySelector("h1")?.innerText || document.title || "offre_emploi";

  // Try to get main content
  let mainContent = document.querySelector("main, article")?.innerText;
  if (!mainContent) mainContent = document.body.innerText;

  // Send to local Python backend
  fetch("http://localhost:5000/api/job", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: title,
      url: url,
      content: mainContent,
    }),
  })
    .then((resp) => resp.json())
    .then((data) => {
      if (data.status === "success") {
        alert(
          `✅ Job sent! Documents created for ${data.company}\nFolder: ${data.folderPath}`,
        );
      } else {
        alert("❌ Error: " + data.message);
      }
    })
    .catch((err) => {
      alert(
        "❌ Network error: " +
          err.message +
          "\nMake sure Python backend is running!",
      );
    });
});
