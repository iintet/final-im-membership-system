document.addEventListener('DOMContentLoaded', () => {
  const editBtn = document.getElementById('editBtn');
  const saveBtn = document.getElementById('saveBtn');
  const cancelBtn = document.getElementById('cancelBtn');
  const form = document.getElementById('profileForm');
  const inputs = form.querySelectorAll('input, textarea');

  inputs.forEach(input => input.disabled = true);

  editBtn.addEventListener('click', () => {
    inputs.forEach(input => input.disabled = false);
    editBtn.style.display = 'none';
    saveBtn.style.display = 'inline-block';
    cancelBtn.style.display = 'inline-block';
  });

  cancelBtn.addEventListener('click', () => {
    inputs.forEach(input => input.disabled = true);
    editBtn.style.display = 'inline-block';
    saveBtn.style.display = 'none';
    cancelBtn.style.display = 'none';
  });


    });
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const phone = document.getElementById('phone').value;
    const address = document.getElementById('address').value; // Ensure this is captured
    const emergencyContact = document.getElementById('emergency-contact').value;
    const currentPassword = document.getElementById('current-password').value;
    const newPassword = document.getElementById('new-password').value;

    // Log the values for debugging
    console.log("Submitting data:", {
      phone: phone,
      address: address,
      emergencycontactnumber: emergencyContact,
      current_password: currentPassword,
      new_password: newPassword
    });

    const response = await fetch("/userprofile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        phone: phone || undefined, // Send as undefined if empty
        address: address || undefined, // Send as undefined if empty
        emergencycontactnumber: emergencyContact || undefined, // Send as undefined if empty
        current_password: currentPassword || undefined,
        new_password: newPassword || undefined
      })
    });

    const result = await response.json();

    if (response.ok) {
      alert(result.message);
    } else {
      alert("Error: " + result.message);
    }

    // Disable inputs again
    inputs.forEach(input => input.disabled = true);
    editBtn.style.display = 'inline-block';
    saveBtn.style.display = 'none';
    cancelBtn.style.display = 'none';
  });


