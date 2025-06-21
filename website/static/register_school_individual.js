document.addEventListener("DOMContentLoaded", () => {
  const region = document.getElementById("ind-school-region");
  const province = document.getElementById("ind-school-province");
  const city = document.getElementById("ind-school-city");
  const name = document.getElementById("ind-school-name");
  const type = document.getElementById("ind-school-type");

  if (!region || !province || !city || !name || !type) return;

  fetch("/api/schregions")
    .then(res => res.json())
    .then(data => {
      region.innerHTML = '<option value="">Select region</option>' +
        data.map(r => `<option value="${r.id}">${r.name}</option>`).join('');
    });

  region.addEventListener("change", () => {
    const id = region.value;
    province.innerHTML = '<option value="">Loading...</option>';
    fetch(`/api/schprovinces?regionid=${id}`)
      .then(res => res.json())
      .then(data => {
        province.innerHTML = '<option value="">Select province</option>' +
          data.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
      });
  });

  province.addEventListener("change", () => {
    const id = province.value;
    city.innerHTML = '<option value="">Loading...</option>';
    fetch(`/api/schcities?provinceid=${id}`)
      .then(res => res.json())
      .then(data => {
        city.innerHTML = '<option value="">Select city</option>' +
          data.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
      });
  });

  city.addEventListener("change", () => {
    const id = city.value;
    name.innerHTML = '<option value="">Loading...</option>';
    fetch(`/api/schnames?cityid=${id}`)
      .then(res => res.json())
      .then(data => {
        name.innerHTML = '<option value="">Select school</option>' +
          data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
      });
  });

  name.addEventListener("change", () => {
    const id = name.value;
    type.value = 'Loading...';
    fetch(`/api/schooltype?schoolid=${id}`)
      .then(res => res.json())
      .then(data => {
        type.value = data.schooltype || "Not found";
      })
      .catch(() => {
        type.value = 'Error';
      });
  });
});
