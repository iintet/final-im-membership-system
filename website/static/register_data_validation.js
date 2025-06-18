// register_data_validation.js

// Function to update required attributes based on selected role
function updateRequiredAttributes() {
  const role = document.getElementById('role').value;
  const individualFields = document.querySelectorAll('#individual-fields input, #individual-fields select');
  const institutionFields = document.querySelectorAll('#institution-fields input, #institution-fields select');

  if (role === 'individual') {
    individualFields.forEach(el => el.setAttribute('required', ''));
    institutionFields.forEach(el => el.removeAttribute('required'));
  } else if (role === 'institution') {
    institutionFields.forEach(el => el.setAttribute('required', ''));
    individualFields.forEach(el => el.removeAttribute('required'));
  } else {
    individualFields.forEach(el => el.removeAttribute('required'));
    institutionFields.forEach(el => el.removeAttribute('required'));
  }
}

// Function to validate affiliation type fields for Individual users
function validateAffiliationFields() {
  const affiliationType = document.getElementById('affiliation-type').value;

  const organizationName = document.getElementById('organization-name');
  const organizationAddress = document.getElementById('organization-address');

  const schoolName = document.getElementById('school-name');
  const schoolType = document.getElementById('school-type');
  const schoolRegion = document.getElementById('school-region');
  const schoolProvince = document.getElementById('school-province');
  const schoolCity = document.getElementById('school-city');

  let isValid = true;
  let messages = [];

  // Clear previous error highlights
  const clearErrors = (elements) => {
    elements.forEach(el => el.classList.remove('input-error'));
  };

  clearErrors([organizationName, organizationAddress, schoolName, schoolType, schoolRegion, schoolProvince, schoolCity]);

  if (affiliationType === 'organization') {
    if (!organizationName.value.trim()) {
      isValid = false;
      messages.push('Organization Name is required.');
      organizationName.classList.add('input-error');
    }
    if (!organizationAddress.value.trim()) {
      isValid = false;
      messages.push('Organization Address is required.');
      organizationAddress.classList.add('input-error');
    }
  } else if (affiliationType === 'school') {
    if (!schoolName.value.trim()) {
      isValid = false;
      messages.push('School Name is required.');
      schoolName.classList.add('input-error');
    }
    if (!schoolType.value) {
      isValid = false;
      messages.push('School Type is required.');
      schoolType.classList.add('input-error');
    }
    if (!schoolRegion.value) {
      isValid = false;
      messages.push('School Region is required.');
      schoolRegion.classList.add('input-error');
    }
    if (!schoolProvince.value) {
      isValid = false;
      messages.push('School Province is required.');
      schoolProvince.classList.add('input-error');
    }
    if (!schoolCity.value) {
      isValid = false;
      messages.push('School City is required.');
      schoolCity.classList.add('input-error');
    }
  }
  return { isValid, messages };
}

// Attach event listeners
document.addEventListener('DOMContentLoaded', () => {
  // Initialize required state on page load
  updateRequiredAttributes();

  // Update required attributes when role changes
  document.getElementById('role').addEventListener('change', updateRequiredAttributes);

  // Validate affiliation fields on form submission
  const form = document.getElementById('registrationForm');
  if (form) {
    form.addEventListener('submit', function(event) {
      const affiliationValidation = validateAffiliationFields();
      if (!affiliationValidation.isValid) {
        event.preventDefault(); // Stop form submission
        alert('Please fix the following errors:\n' + affiliationValidation.messages.join('\n'));
      }
    });
  }
});

// CSS for .input-error (add to your stylesheet or inside a <style> tag)
/*
.input-error {
  border-color: #dc2626;  // Red-600
  background-color: #fee2e2; // Red-100
  transition: background-color 0.3s ease, border-color 0.3s ease;
}
*/
