document.addEventListener('DOMContentLoaded', () => {
    const regionSelect = document.getElementById('region');
    const provinceSelect = document.getElementById('province');
    const citySelect = document.getElementById('city');
    const barangaySelect = document.getElementById('barangay');

    // Fetch Regions on load
    fetch('/api/regions')
        .then(res => res.json())
        .then(data => {
            regionSelect.innerHTML = '<option value="">Select region</option>' +
                data.map(r => `<option value="${r.regionid}">${r.regionname}</option>`).join('');
        });

    regionSelect.addEventListener('change', () => {
        const regionId = regionSelect.value;
        provinceSelect.innerHTML = '<option value="">Loading...</option>';
        citySelect.innerHTML = '<option value="">Select a city</option>';
        barangaySelect.innerHTML = '<option value="">Select a barangay</option>';
        if (!regionId) {
            provinceSelect.innerHTML = '<option value="">Select a province</option>';
            return;
        }
        fetch(`/api/provinces?region_id=${regionId}`)
            .then(res => res.json())
            .then(data => {
                provinceSelect.innerHTML = '<option value="">Select a province</option>' +
                    data.map(p => `<option value="${p.provinceid}">${p.provincename}</option>`).join('');
            });
    });

    provinceSelect.addEventListener('change', () => {
        const provinceId = provinceSelect.value;
        citySelect.innerHTML = '<option value="">Loading...</option>';
        barangaySelect.innerHTML = '<option value="">Select a barangay</option>';
        if (!provinceId) {
            citySelect.innerHTML = '<option value="">Select a city</option>';
            return;
        }
        fetch(`/api/cities?province_id=${provinceId}`)
            .then(res => res.json())
            .then(data => {
                citySelect.innerHTML = '<option value="">Select a city</option>' +
                    data.map(c => `<option value="${c.cityid}">${c.cityname}</option>`).join('');
            });
    });

    citySelect.addEventListener('change', () => {
        const cityId = citySelect.value;
        barangaySelect.innerHTML = '<option value="">Loading...</option>';
        if (!cityId) {
            barangaySelect.innerHTML = '<option value="">Select a barangay</option>';
            return;
        }
        fetch(`/api/barangays?city_id=${cityId}`)
            .then(res => res.json())
            .then(data => {
                barangaySelect.innerHTML = '<option value="">Select a barangay</option>' +
                    data.map(b => `<option value="${b.barangayid}">${b.barangayname}</option>`).join('');
            });
    });
});