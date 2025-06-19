document.getElementById("registrationForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const formData = new FormData(this);
  const json = Object.fromEntries(formData.entries());

  const role = formData.get("role");

  // Add emergency contact fields based on role
  if (role === "individual") {
    json["emergencycontactnumber"] = formData.get("individual-emergency-contact-number");
    json["emergencycontactname"] = formData.get("individual-emergency-contact-name");

    // Handle optional organization/school fields
    const affiliationType = formData.get("affiliation-type");

    if (affiliationType === "organization") {
      const orgName = formData.get("organization-name");
      const orgAddress = formData.get("organization-address");

      json["organization-name"] = orgName && orgName !== "NaN" ? orgName : "";
      json["organization-address"] = orgAddress || "";
    } else if (affiliationType === "school") {
      json["school-region"] = formData.get("school-region");
      json["school-province"] = formData.get("school-province");
      json["school-city"] = formData.get("school-city");
      json["school-name"] = formData.get("school-name");
      json["school-type"] = formData.get("school-type");
    }

  } else if (role === "institution") {
    json["emergencycontactnumber"] = formData.get("institution-emergencycontactnumber");
    json["emergencycontactname"] = formData.get("institution-emergency-contact-name");
  }

  // Remove fields that are empty or invalid
  Object.keys(json).forEach(key => {
    const value = json[key];
    if (
      value === "" ||
      value === null ||
      value === undefined ||
      value === "NaN" ||
      (typeof value === "number" && isNaN(value))
    ) {
      delete json[key];
    }
  });

  console.log("FormData JSON to be sent:", json); // Debug

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
      window.location.href = "/auth/login"; // or "/userdashboard"
    })
    .catch(error => {
      console.error("Fetch error:", error);
      alert("Something went wrong while registering.");
    });
});


   document.getElementById("role").addEventListener("change", function () {
       const role = this.value;
       const individualFields = document.getElementById("individual-fields");
       const institutionFields = document.getElementById("institution-fields");
       const registerButton = document.querySelector("button[type='submit']");

       if (role === "individual") {
           individualFields.style.display = "block";
           institutionFields.style.display = "none";
           registerButton.style.display = "block"; // Ensure button is shown
       } else if (role === "institution") {
           institutionFields.style.display = "block";
           individualFields.style.display = "none";
           registerButton.style.display = "block"; // Ensure button is shown
       } else {
           individualFields.style.display = "none";
           institutionFields.style.display = "none";
           registerButton.style.display = "none"; // Hide button if no role is selected
       }
   });
   