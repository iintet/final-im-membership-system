document.getElementById("registrationForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const formData = new FormData(this);

  // Convert to object
  const json = Object.fromEntries(formData.entries());
  console.log("FormData JSON to be sent:", json); // ✅ DEBUG

  fetch("/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(json)
  })
    .then(async response => {
      const result = await response.json();
      if (!response.ok) {
        console.error("Registration failed:", result.error);
        alert(result.error || "Registration failed");
        return;
      }
      console.log("Registration success:", result);
      window.location.href = "/auth/login"; // or /userdashboard if needed
    })
    .catch(error => {
      console.error("Fetch error:", error);
      alert("Something went wrong while registering.");
    });
});