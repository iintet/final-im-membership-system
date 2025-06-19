const form = document.getElementById('profileForm');
const inputs = form.querySelectorAll('input, textarea, select');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const phone = document.getElementById('phone').value;
  const address = document.getElementById('address').value;
  const emergencyContact = document.getElementById('emergency-contact').value;
  const currentPassword = document.getElementById('current-password').value;
  const newPassword = document.getElementById('new-password').value;
  const confirmPassword = document.getElementById('confirm-password').value;

  const regionId = document.getElementById('region').value;
  const provinceId = document.getElementById('province').value;
  const cityId = document.getElementById('city').value;
  const barangayId = document.getElementById('barangay').value;

  if (newPassword && newPassword !== confirmPassword) {
    alert("New password and confirm password do not match.");
    return;
  }

  const response = await fetch("/profile/update", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      phone: phone,
      address: address,
      emergencycontactnumber: emergencyContact,
      region: regionId,
      province: provinceId,
      city: cityId,
      barangay: barangayId,
      current_password: currentPassword,
      new_password: newPassword
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


document.addEventListener('DOMContentLoaded', () => {
  const regionSelect = document.getElementById('region');
  const provinceSelect = document.getElementById('province');
  const citySelect = document.getElementById('city');
  const barangaySelect = document.getElementById('barangay');

  // Values passed from Flask template
  const selectedRegion = window.selectedRegion || "";
  const selectedProvince = window.selectedProvince || "";
  const selectedCity = window.selectedCity || "";
  const selectedBarangay = window.selectedBarangay || "";

  // Load Regions
  fetch('/api/regions')
    .then(res => res.json())
    .then(data => {
      regionSelect.innerHTML = '<option value="">Select region</option>' +
        data.map(r => `<option value="${r.regionid}">${r.regionname}</option>`).join('');

      if (selectedRegion) {
        regionSelect.value = selectedRegion;
        regionSelect.dispatchEvent(new Event('change'));
      }
    })
    .catch(err => {
      console.error("Failed to load regions:", err);
      regionSelect.innerHTML = '<option value="">Error loading regions</option>';
    });

  // Load Provinces when region changes
  regionSelect.addEventListener('change', () => {
  const regionId = regionSelect.value;
  console.log("Region changed to:", regionId);

  if (!regionId) {
    provinceSelect.innerHTML = '<option value="">Select province</option>';
    citySelect.innerHTML = '<option value="">Select city</option>';
    barangaySelect.innerHTML = '<option value="">Select barangay</option>';
    return;
  }

  fetch(`/api/provinces/${regionId}`)
    .then(res => {
      if (!res.ok) throw new Error('Failed to fetch provinces');
      return res.json();
    })
    .then(data => {
      console.log("Loaded provinces:", data);  // ✅ see what's returned
      provinceSelect.innerHTML = '<option value="">Select province</option>' +
        data.map(p => `<option value="${p.provinceid}">${p.provincename}</option>`).join('');

      if (selectedProvince) {
        provinceSelect.value = selectedProvince;
        provinceSelect.dispatchEvent(new Event('change'));
      }
    })
    .catch(err => {
      console.error("Error fetching provinces:", err);
      provinceSelect.innerHTML = '<option value="">Error loading provinces</option>';
    });
});

  // Load Cities when province changes
  provinceSelect.addEventListener('change', () => {
    const provinceId = provinceSelect.value;
    citySelect.innerHTML = '<option value="">Select city</option>'; // reset
    barangaySelect.innerHTML = '<option value="">Select barangay</option>'; // reset

    if (!provinceId) return;

    fetch(`/api/cities/${provinceId}`)
      .then(res => res.json())
      .then(data => {
        citySelect.innerHTML = '<option value="">Select city</option>' +
          data.map(c => `<option value="${c.cityid}">${c.cityname}</option>`).join('');
        if (window.selectedCity) {
          citySelect.value = window.selectedCity;
          citySelect.dispatchEvent(new Event('change'));
        }
      });
  });

  // Load Barangays when city changes
  citySelect.addEventListener('change', () => {
    const cityId = citySelect.value;

    barangaySelect.innerHTML = '<option value="">Select barangay</option>'; // reset

    if (!cityId) return;

    fetch(`/api/barangays/${cityId}`)
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch barangays");
        return res.json();
      })
      .then(data => {
        barangaySelect.innerHTML = '<option value="">Select barangay</option>' +
          data.map(b => `<option value="${b.barangayid}">${b.barangayname}</option>`).join('');

        // Preselect barangay if coming from backend
        if (window.selectedBarangay) {
          barangaySelect.value = window.selectedBarangay;
          window.selectedBarangay = ""; // clear after use
        }
      })
      .catch(err => {
        console.error("Error loading barangays:", err);
        barangaySelect.innerHTML = '<option value="">Error loading barangays</option>';
      });
});
  console.log("City API response:", data);
});