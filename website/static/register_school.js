document.addEventListener('DOMContentLoaded', () => {
    const regionSelect = document.getElementById('school-region');
    const provinceSelect = document.getElementById('school-province');
    const citySelect = document.getElementById('school-city');
 
    

    
    fetch('/api/regions')
        .then(res => {
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            return res.json();
        })
        .then(data => {
            if (!Array.isArray(data)) {
                throw new Error('Expected an array but got: ' + JSON.stringify(data));
            }
            regionSelect.innerHTML = '<option value="">Select region</option>' +
                data.map(r => `<option value="${r.regionid}">${r.regionname}</option>`).join('');
        })
        .catch(error => {
            console.error('Error fetching regions:', error);
            regionSelect.innerHTML = '<option value="">Error loading regions</option>';
        });
    

    // Add event listeners for dynamic dropdowns
    regionSelect.addEventListener('change', function() {
        const selectedRegionId = this.value;
        console.log('Selected Region ID:', selectedRegionId); // Log the selected region ID
        fetch(`/api/provinces?regionid=${selectedRegionId}`)
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                if (!Array.isArray(data)) {
                    throw new Error('Expected an array but got: ' + JSON.stringify(data));
                }
                provinceSelect.innerHTML = '<option value="">Select province</option>' +
                    data.map(p => `<option value="${p.provinceid}">${p.provincename}</option>`).join('');
            })
            .catch(error => {
                console.error('Error fetching provinces:', error);
                provinceSelect.innerHTML = '<option value="">Error loading provinces</option>';
            });
    });

   

    provinceSelect.addEventListener('change', () => {
        const provinceId = provinceSelect.value;
        citySelect.innerHTML = '<option value="">Loading...</option>';
        if (!provinceId) {
            citySelect.innerHTML = '<option value="">Select a city</option>';
            return;
        }
        fetch(`/api/cities?provinceid=${provinceId}`)
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                citySelect.innerHTML = '<option value="">Select a city</option>' +
                    data.map(c => `<option value="${c.cityid}">${c.cityname}</option>`).join('');
            })
            .catch(error => {
                console.error('Error fetching cities:', error);
                citySelect.innerHTML = '<option value="">Error loading cities</option>';
            });
    });


        
        
});
