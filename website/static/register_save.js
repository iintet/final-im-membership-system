document.getElementById("registrationForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const formData = new FormData(this);
  const json = Object.fromEntries(formData.entries());

  fetch("/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(json)
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Registration failed");
      }
      return response.json();
    })
    .then(data => {
      console.log("Success:", data);
      window.location.href = "/userdashboard";
    })
    .catch(error => {
      console.error("Error:", error);
    });
});
