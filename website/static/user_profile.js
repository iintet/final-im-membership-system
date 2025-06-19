document.addEventListener('DOMContentLoaded', () => {
  const editBtn = document.getElementById('editBtn');
  const saveBtn = document.getElementById('saveBtn');
  const cancelBtn = document.getElementById('cancelBtn');
  const form = document.getElementById('profileForm');

  const regionSelect = document.getElementById('region');
  const provinceSelect = document.getElementById('province');
  const citySelect = document.getElementById('city');
  const barangaySelect = document.getElementById('barangay');

  const editableIds = [
    'phone',
    'emergency-contact',
    'current-password',
    'new-password',
    'confirm-password'
  ];
  const editableInputs = editableIds.map(id => document.getElementById(id));

  const toggleInputs = (enabled) => {
    editableInputs.forEach(input => {
      if (input) input.disabled = !enabled;
    });
    regionSelect.disabled = !enabled;
    provinceSelect.disabled = !enabled;
    citySelect.disabled = !enabled;
    barangaySelect.disabled = !enabled;
  };

  const preselectLocation = () => {
  const regionId = document.body.dataset.regionId;
  const provinceId = document.body.dataset.provinceId;
  const cityId = document.body.dataset.cityId;
  const barangayId = document.body.dataset.barangayId;

  if (!regionId) return;

  regionSelect.value = regionId;

  fetch(`/api/provinces?regionid=${regionId}`)
    .then(res => res.json())
    .then(provinces => {
      provinceSelect.innerHTML = provinces.map(p => {
        const id = p.provinceid || p.id;
        const name = p.provincename || p.name;
        return `<option value="${id}" ${id == provinceId ? 'selected' : ''}>${name}</option>`;
      }).join('');
      return fetch(`/api/cities?provinceid=${provinceId}`);
    })
    .then(res => res.json())
    .then(cities => {
      citySelect.innerHTML = cities.map(c => {
        const id = c.cityid || c.id;
        const name = c.cityname || c.name;
        return `<option value="${id}" ${id == cityId ? 'selected' : ''}>${name}</option>`;
      }).join('');
      return fetch(`/api/barangays?cityid=${cityId}`);
    })
    .then(res => res.json())
    .then(barangays => {
      barangaySelect.innerHTML = barangays.map(b => {
        const id = b.barangayid || b.id;
        const name = b.barangayname || b.name;
        return `<option value="${id}" ${id == barangayId ? 'selected' : ''}>${name}</option>`;
      }).join('');
    });
};


  const loadDropdowns = () => {
    fetch('/api/regions')
      .then(res => res.json())
      .then(data => {
        regionSelect.innerHTML = '<option value="">Select region</option>' +
          data.map(r => `<option value="${r.regionid}">${r.regionname}</option>`).join('');
      });

    regionSelect.addEventListener('change', () => {
      const regionId = regionSelect.value;
      fetch(`/api/provinces?regionid=${regionId}`)
        .then(res => res.json())
        .then(data => {
          provinceSelect.innerHTML = '<option value="">Select province</option>' +
            data.map(p => `<option value="${p.provinceid}">${p.provincename}</option>`).join('');
          citySelect.innerHTML = '<option value="">Select city</option>';
          barangaySelect.innerHTML = '<option value="">Select barangay</option>';
        });
    });

    provinceSelect.addEventListener('change', () => {
      const provinceId = provinceSelect.value;
      fetch(`/api/cities?provinceid=${provinceId}`)
        .then(res => res.json())
        .then(data => {
          citySelect.innerHTML = '<option value="">Select city</option>' +
            data.map(c => `<option value="${c.cityid}">${c.cityname}</option>`).join('');
          barangaySelect.innerHTML = '<option value="">Select barangay</option>';
        });
    });

    citySelect.addEventListener('change', () => {
      const cityId = citySelect.value;
      fetch(`/api/barangays?cityid=${cityId}`)
        .then(res => res.json())
        .then(data => {
          barangaySelect.innerHTML = '<option value="">Select barangay</option>' +
            data.map(b => `<option value="${b.barangayid}">${b.barangayname}</option>`).join('');
        });
    });
  };

  editBtn.addEventListener('click', () => {
    toggleInputs(true);
    editBtn.style.display = 'none';
    saveBtn.style.display = 'inline-block';
    cancelBtn.style.display = 'inline-block';

    loadDropdowns().then(() => {
      preselectLocation();
    });
  });

  cancelBtn.addEventListener('click', () => {
    location.reload();
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const body = {
      phone: document.getElementById('phone').value,
      emergencycontactnumber: document.getElementById('emergency-contact').value,
      current_password: document.getElementById('current-password').value || undefined,
      new_password: document.getElementById('new-password').value || undefined,
      region: regionSelect.value || null,
      province: provinceSelect.value || null,
      city: citySelect.value || null,
      barangay: barangaySelect.value || null
    };

    const response = await fetch("/userprofile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    const result = await response.json();

    alert(result.message || "Saved");
    toggleInputs(false);
    editBtn.style.display = 'inline-block';
    saveBtn.style.display = 'none';
    cancelBtn.style.display = 'none';
  });
});
