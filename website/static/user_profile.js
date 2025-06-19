document.addEventListener('DOMContentLoaded', () => {
  const editBtn = document.getElementById('editBtn');
  const saveBtn = document.getElementById('saveBtn');
  const cancelBtn = document.getElementById('cancelBtn');
  const form = document.getElementById('profileForm');
  const inputs = form.querySelectorAll('input');

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

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const phone = document.getElementById('phone').value;
    const emergencyContact = document.getElementById('emergency-contact').value;
    const currentPassword = document.getElementById('current-password').value;
    const newPassword = document.getElementById('new-password').value;

    const response = await fetch("/userprofile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        phone: phone,
        emergencycontactnumber: emergencyContact,
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
});
