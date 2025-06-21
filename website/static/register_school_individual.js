document.addEventListener("DOMContentLoaded", () => {
  const region = document.getElementById("school-region");
  const province = document.getElementById("school-province");
  const city = document.getElementById("school-city");
  const name = document.getElementById("school-name");
  const type = document.getElementById("school-type");

  if (!region || !province || !city || !name || !type) return;

  fetch("/api/schregions")
    .then(res => res.json())
    .then(data => {
      region.innerHTML = '<option value="">Select region</option>' +
        data.map(r => `<option value="${r.id}">${r.name}</option>`).join('');
    });

  region.addEventListener("change", () => {
    const id = region.value;
    fetch(`/api/schprovinces?regionid=${id}`)
      .then(res => res.json())
      .then(data => {
        province.innerHTML = '<option value="">Select province</option>' +
          data.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
      });
  });

  province.addEventListener("change", () => {
    const id = province.value;
    fetch(`/api/schcities?provinceid=${id}`)
      .then(res => res.json())
      .then(data => {
        city.innerHTML = '<option value="">Select city</option>' +
          data.map(c => `<option value="${c.cityid}">${c.cityname}</option>`).join('');
      });
  });

  city.addEventListener("change", () => {
    const id = city.value;
    fetch(`/api/schnames?cityid=${id}`)
      .then(res => res.json())
      .then(data => {
        name.innerHTML = '<option value="">Select school</option>' +
          data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
      });
  });

  name.addEventListener("change", () => {
    const id = name.value;
    fetch(`/api/schooltype?schoolid=${id}`)
      .then(res => res.json())
      .then(data => {
        type.value = data.schooltype || "Not found";
      });
  });
});
