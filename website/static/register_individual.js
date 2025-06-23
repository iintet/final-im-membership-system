document.addEventListener('DOMContentLoaded', () => {
    const regionSelect = document.getElementById('region');
    const provinceSelect = document.getElementById('province');
    const citySelect = document.getElementById('city');
    const barangaySelect = document.getElementById('barangay');

    if (regionSelect) {
        fetch('/api/regions')
            .then(res => {
                if (!res.ok) throw new Error('Network response was not ok');
                return res.json();
            })
            .then(data => {
                if (!Array.isArray(data)) throw new Error('Expected an array but got: ' + JSON.stringify(data));
                regionSelect.innerHTML = '<option value="">Select region</option>' +
                    data.map(r => `<option value="${r.regionid}">${r.regionname}</option>`).join('');
            })
            .catch(error => {
                console.error('Error fetching regions:', error);
                regionSelect.innerHTML = '<option value="">Error loading regions</option>';
            });

        regionSelect.addEventListener('change', function() {
            const selectedRegionId = this.value;
            console.log('Selected Region ID:', selectedRegionId);
            if (provinceSelect) {
                fetch(`/api/provinces?regionid=${selectedRegionId}`)
                    .then(res => {
                        if (!res.ok) throw new Error('Network response was not ok');
                        return res.json();
                    })
                    .then(data => {
                        if (!Array.isArray(data)) throw new Error('Expected an array but got: ' + JSON.stringify(data));
                        provinceSelect.innerHTML = '<option value="">Select province</option>' +
                            data.map(p => `<option value="${p.provinceid}">${p.provincename}</option>`).join('');
                    })
                    .catch(error => {
                        console.error('Error fetching provinces:', error);
                        provinceSelect.innerHTML = '<option value="">Error loading provinces</option>';
                    });
            }
        });
    }

    if (provinceSelect) {
        provinceSelect.addEventListener('change', () => {
            const provinceId = provinceSelect.value;
            if (citySelect) {
                citySelect.innerHTML = '<option value="">Loading...</option>';
            }
            if (barangaySelect) {
                barangaySelect.innerHTML = '<option value="">Select a barangay</option>';
            }
            if (!provinceId) {
                if (citySelect) citySelect.innerHTML = '<option value="">Select a city</option>';
                return;
            }
            fetch(`/api/cities?provinceid=${provinceId}`)
                .then(res => {
                    if (!res.ok) throw new Error('Network response was not ok');
                    return res.json();
                })
                .then(data => {
                    if (citySelect) {
                        citySelect.innerHTML = '<option value="">Select a city</option>' +
                            data.map(c => `<option value="${c.cityid}">${c.cityname}</option>`).join('');
                    }
                })
                .catch(error => {
                    console.error('Error fetching cities:', error);
                    if (citySelect) citySelect.innerHTML = '<option value="">Error loading cities</option>';
                });
        });
    }

    if (citySelect) {
        citySelect.addEventListener('change', () => {
            const cityId = citySelect.value;
            if (barangaySelect) barangaySelect.innerHTML = '<option value="">Loading...</option>';
            if (!cityId) {
                if (barangaySelect) barangaySelect.innerHTML = '<option value="">Select a barangay</option>';
                return;
            }
            fetch(`/api/barangays?cityid=${cityId}`)
                .then(res => {
                    if (!res.ok) throw new Error('Network response was not ok');
                    return res.json();
                })
                .then(data => {
                    if (barangaySelect) {
                        barangaySelect.innerHTML = '<option value="">Select a barangay</option>' +
                            data.map(b => `<option value="${b.barangayid}">${b.barangayname}</option>`).join('');
                    }
                })
                .catch(error => {
                    console.error('Error fetching barangays:', error);
                    if (barangaySelect) barangaySelect.innerHTML = '<option value="">Error loading barangays</option>';
                });
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const regionSelect = document.getElementById('school-region');
    const provinceSelect = document.getElementById('school-province');
    const citySelect = document.getElementById('school-city');
    const schoolSelect = document.getElementById('school-name');

    fetch('/api/schregions')
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
                data.map(r => `<option value="${r.id}">${r.name}</option>`).join('');
        })
        .catch(error => {
            console.error('Error fetching regions:', error);
            regionSelect.innerHTML = '<option value="">Error loading regions</option>';
        });

    regionSelect.addEventListener('change', function() {
        const selectedRegionId = this.value;
        fetch(`/api/schprovinces?regionid=${selectedRegionId}`)
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                provinceSelect.innerHTML = '<option value="">Select province</option>' +
                    data.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
            })
            .catch(error => {
                console.error('Error fetching provinces:', error);
                provinceSelect.innerHTML = '<option value="">Error loading provinces</option>';
            });
    });

    provinceSelect.addEventListener('change', () => {
        const provinceId = provinceSelect.value;
        citySelect.innerHTML = '<option value="">Loading...</option>';
        schoolSelect.innerHTML = '<option value="">Select a school</option>';
        if (!provinceId) {
            citySelect.innerHTML = '<option value="">Select a city</option>';
            return;
        }
        fetch(`/api/schcities?provinceid=${provinceId}`)
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                citySelect.innerHTML = '<option value="">Select a city</option>' +
                    data.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
            })
            .catch(error => {
                console.error('Error fetching cities:', error);
                citySelect.innerHTML = '<option value="">Error loading cities</option>';
            });
    });

    citySelect.addEventListener('change', () => {
        const cityId = citySelect.value;
        schoolSelect.innerHTML = '<option value="">Loading...</option>';
        if (!cityId) {
            schoolSelect.innerHTML = '<option value="">Select a school</option>';
            return;
        }
        fetch(`/api/schnames?cityid=${cityId}`)
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                schoolSelect.innerHTML = '<option value="">Select a school</option>' +
                    data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
            })
            .catch(error => {
                console.error('Error fetching schools:', error);
                schoolSelect.innerHTML = '<option value="">Error loading schools</option>';
            });
    });

    schoolSelect.addEventListener('change', () => {
        const schoolId = schoolSelect.value;
        const schoolTypeInput = document.getElementById('school-type');

        schoolTypeInput.value = 'Loading...';

        if (!schoolId) {
            schoolTypeInput.value = '';
            return;
        }

        fetch(`/api/schooltype?schoolid=${schoolId}`)
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                if (data.schooltype) {
                    schoolTypeInput.value = data.schooltype;
                } else {
                    schoolTypeInput.value = 'Not found';
                }
            })
            .catch(error => {
                console.error('Error fetching school type:', error);
                schoolTypeInput.value = 'Error';
            });
    });

    const affiliationType = document.getElementById("individual-affiliation-type");
    if (affiliationType) {
        affiliationType.addEventListener("change", function () {
            const affiliationTypeValue = this.value;
            const organizationFields = document.getElementById("ind-organization-dropdown"); // <-- FIXED ID
            const schoolFields = document.getElementById("ind-school-dropdown"); // <-- FIXED ID
            const orgName = document.getElementById("ind-organization-select");
            const orgAddress = document.getElementById("ind-organization-address");
            const schoolRegion = document.getElementById("ind-school-region");
            const schoolProvince = document.getElementById("ind-school-province");
            const schoolCity = document.getElementById("ind-school-city");
            const schoolName = document.getElementById("ind-school-name");

            if (affiliationTypeValue === "organization") {
                if (organizationFields) organizationFields.style.display = "block";
                if (schoolFields) schoolFields.style.display = "none";
                // Remove required attributes
                if (orgName) orgName.removeAttribute("required");
                if (orgAddress) orgAddress.removeAttribute("required");
                if (schoolRegion) schoolRegion.removeAttribute("required");
                if (schoolProvince) schoolProvince.removeAttribute("required");
                if (schoolCity) schoolCity.removeAttribute("required");
                if (schoolName) schoolName.removeAttribute("required");
            } else if (affiliationTypeValue === "school") {
                if (schoolFields) schoolFields.style.display = "block";
                if (organizationFields) organizationFields.style.display = "none";
                // Remove required attributes
                if (schoolRegion) schoolRegion.removeAttribute("required");
                if (schoolProvince) schoolProvince.removeAttribute("required");
                if (schoolCity) schoolCity.removeAttribute("required");
                if (schoolName) schoolName.removeAttribute("required");
                if (orgName) orgName.removeAttribute("required");
                if (orgAddress) orgAddress.removeAttribute("required");
            } else {
                if (organizationFields) organizationFields.style.display = "none";
                if (schoolFields) schoolFields.style.display = "none";
                // Remove required attributes
                if (orgName) orgName.removeAttribute("required");
                if (orgAddress) orgAddress.removeAttribute("required");
                if (schoolRegion) schoolRegion.removeAttribute("required");
                if (schoolProvince) schoolProvince.removeAttribute("required");
                if (schoolCity) schoolCity.removeAttribute("required");
                if (schoolName) schoolName.removeAttribute("required");
            }
        });
    }

});
