document.addEventListener('DOMContentLoaded', () => {
    const regionSelect = document.getElementById('inst-region');
        if (!regionSelect) return; // Stop here if element not found

    const provinceSelect = document.getElementById('inst-province');
    const citySelect = document.getElementById('inst-city');
    const barangaySelect = document.getElementById('inst-barangay');

    // Fetch all regions
    fetch('/api/instregions')
        .then(res => res.ok ? res.json() : Promise.reject('Failed to load regions'))
        .then(data => {
            regionSelect.innerHTML = '<option value="">Select region</option>' +
                data.map(r => `<option value="${r.regionid}">${r.regionname}</option>`).join('');
        })
        .catch(error => {
            console.error('Error fetching regions:', error);
            regionSelect.innerHTML = '<option value="">Error loading regions</option>';
        });

    // Fetch provinces based on region
    regionSelect.addEventListener('change', function () {
        const selectedRegionId = this.value;
        fetch(`/api/instprovinces?regionid=${selectedRegionId}`)
            .then(res => res.ok ? res.json() : Promise.reject('Failed to load provinces'))
            .then(data => {
                provinceSelect.innerHTML = '<option value="">Select province</option>' +
                    data.map(p => `<option value="${p.provinceid}">${p.provincename}</option>`).join('');
            })
            .catch(error => {
                console.error('Error fetching provinces:', error);
                provinceSelect.innerHTML = '<option value="">Error loading provinces</option>';
            });
    });

    // Fetch cities based on province
    provinceSelect.addEventListener('change', () => {
        const provinceId = provinceSelect.value;
        citySelect.innerHTML = '<option value="">Loading...</option>';
        barangaySelect.innerHTML = '<option value="">Select a barangay</option>';

        if (!provinceId) {
            citySelect.innerHTML = '<option value="">Select a city</option>';
            return;
        }

        fetch(`/api/instcities?provinceid=${provinceId}`)
            .then(res => res.ok ? res.json() : Promise.reject('Failed to load cities'))
            .then(data => {
                citySelect.innerHTML = '<option value="">Select a city</option>' +
                    data.map(c => `<option value="${c.cityid}">${c.cityname}</option>`).join('');
            })
            .catch(error => {
                console.error('Error fetching cities:', error);
                citySelect.innerHTML = '<option value="">Error loading cities</option>';
            });
    });

    citySelect.addEventListener('change', () => {
        const cityId = citySelect.value;
        barangaySelect.innerHTML = '<option value="">Loading...</option>';
        if (!cityId) {
            barangaySelect.innerHTML = '<option value="">Select a barangay</option>';
            return;
        }
        fetch(`/api/instbarangays?cityid=${cityId}`)
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                barangaySelect.innerHTML = '<option value="">Select a barangay</option>' +
                    data.map(b => `<option value="${b.barangayid}">${b.barangayname}</option>`).join('');
            })
            .catch(error => {
                console.error('Error fetching barangays:', error);
                barangaySelect.innerHTML = '<option value="">Error loading barangays</option>';
            });
    });
});
