document.getElementById("registrationForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const formData = new FormData(this);
  const json = Object.fromEntries(formData.entries());
  const role = formData.get("role");

  // Add emergency contact fields based on role
  if (role === "individual") {
    json["emergencycontactnumber"] = formData.get("individual-emergency-contact-number");
    json["emergencycontactname"] = formData.get("individual-emergency-contact-name");

    const affiliationType = formData.get("affiliation-type");
    json["affiliation-type"] = affiliationType;

    if (affiliationType === "organization") {
      json["organization-name"] = formData.get("organization-name") || "";
      json["organization-address"] = formData.get("organization-address") || "";
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

  // Remove empty/invalid fields
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

  console.log("FormData JSON to be sent:", json);

  try {
    const response = await fetch("/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(json)
    });

    const raw = await response.text(); // Read only once
    let result;

    try {
      result = JSON.parse(raw);
    } catch (parseError) {
      console.error("Server returned non-JSON response:", raw);
      alert("Unexpected server response. Please try again later.");
      return;
    }

    if (!response.ok) {
      console.error("Registration failed:", result.error);
      alert(result.error || "Registration failed");
      return;
    }

    console.log("Registration successful:", result);
    window.location.href = "/auth/login";
  } catch (fetchError) {
    console.error("Fetch error:", fetchError);
    alert("Something went wrong while registering.");
  }
});

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
