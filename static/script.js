async function polishEmail() {
  const draft = document.getElementById("draft").value;
  const tone = document.getElementById("tone").value;

  document.getElementById("output").innerText = "Processing...";

  try {
    const res = await fetch("/polish", {   // ✅ relative path
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ draft, tone })
    });

    const data = await res.json();
    if (data.polished) {
      document.getElementById("output").innerText = data.polished;
    } else {
      document.getElementById("output").innerText = "Error: " + JSON.stringify(data.error);
    }
  } catch (err) {
    document.getElementById("output").innerText = "Request failed: " + err;
  }
}
