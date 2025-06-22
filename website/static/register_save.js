document.getElementById("registrationForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const formData = new FormData(this);
  const json = Object.fromEntries(formData.entries());

  // Remove required from hidden fields to avoid "not focusable" errors
  document.querySelectorAll('[style*="display: none"] input, [style*="display: none"] select').forEach(el => {
    el.removeAttribute('required');
  });

  const response = await fetch("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(json)
  });

  const result = await response.json();

  if (result.error) {
    alert(result.error); // Show backend error (like invalid phone)
    return;
  }

  if (result.redirect) {
    window.location.href = result.redirect;
  }
});

// Role toggle logic
document.getElementById("role").addEventListener("change", function () {
  const role = this.value;
  const individualFields = document.getElementById("individual-fields");
  const institutionFields = document.getElementById("institution-fields");
  const registerButton = document.querySelector("button[type='submit']");

  if (role === "individual") {
    individualFields.style.display = "block";
    institutionFields.style.display = "none";
    registerButton.style.display = "block";
  } else if (role === "institution") {
    institutionFields.style.display = "block";
    individualFields.style.display = "none";
    registerButton.style.display = "block";
  } else {
    individualFields.style.display = "none";
    institutionFields.style.display = "none";
    registerButton.style.display = "none";
  }
});
