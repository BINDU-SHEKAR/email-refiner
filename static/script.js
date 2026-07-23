async function polishEmail() {
  const draft = document.getElementById("draft").value;
  const tone = document.getElementById("tone").value;
  const output = document.getElementById("output");

  // Show loading message
  output.textContent = "Processing...";

  try {
    // Send request to backend
    const response = await fetch("/polish", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ draft, tone })
    });

    // Parse JSON response
    const data = await response.json();

    // Display polished email or error
    if (data.polished) {
      output.textContent = data.polished;
    } else {
      output.textContent = "Error: " + JSON.stringify(data.error);
    }
  } catch (err) {
    output.textContent = "Request failed: " + err;
  }
}
