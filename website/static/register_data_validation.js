// Fields to skip from being marked 'required'
function isSkippable(el) {
  return el.id === 'middlename';
}

document.addEventListener('DOMContentLoaded', () => {
  // Update required fields dynamically by role
  function updateRequiredAttributes() {
    const role = document.getElementById('role')?.value;
    const individualFields = document.querySelectorAll('#individual-fields input, #individual-fields select');
    const institutionFields = document.querySelectorAll('#institution-fields input, #institution-fields select');

    if (role === 'individual') {
      individualFields.forEach(el => {
        if (!isSkippable(el)) el.setAttribute('required', '');
        else el.removeAttribute('required');
      });
      institutionFields.forEach(el => el.removeAttribute('required'));
    } else if (role === 'institution') {
      institutionFields.forEach(el => el.setAttribute('required', ''));
      individualFields.forEach(el => el.removeAttribute('required'));
    } else {
      individualFields.forEach(el => el.removeAttribute('required'));
      institutionFields.forEach(el => el.removeAttribute('required'));
    }
  }

  // Validate Individual > School or Organization fields
  function validateIndividualAffiliation() {
    const type = document.getElementById('affiliation-type')?.value;

    const orgName = document.getElementById('organization-name');
    const orgAddr = document.getElementById('organization-address');

    const schName = document.getElementById('ind-school-name');
    const schType = document.getElementById('ind-school-type');
    const schRegion = document.getElementById('ind-school-region');
    const schProvince = document.getElementById('ind-school-province');
    const schCity = document.getElementById('ind-school-city');

    let isValid = true;
    let messages = [];

    const clearErrors = (elements) => {
      elements.forEach(el => el?.classList.remove('input-error'));
    };

    clearErrors([orgName, orgAddr, schName, schType, schRegion, schProvince, schCity]);

    if (type === 'organization') {
      if (!orgName?.value.trim()) {
        messages.push("Organization Name is required.");
        orgName?.classList.add("input-error");
        isValid = false;
      }
      if (!orgAddr?.value.trim()) {
        messages.push("Organization Address is required.");
        orgAddr?.classList.add("input-error");
        isValid = false;
      }
    } else if (type === 'school') {
      if (!schName?.value.trim()) {
        messages.push("School Name is required.");
        schName?.classList.add("input-error");
        isValid = false;
      }
      if (!schType?.value) {
        messages.push("School Type is required.");
        schType?.classList.add("input-error");
        isValid = false;
      }
      if (!schRegion?.value) {
        messages.push("School Region is required.");
        schRegion?.classList.add("input-error");
        isValid = false;
      }
      if (!schProvince?.value) {
        messages.push("School Province is required.");
        schProvince?.classList.add("input-error");
        isValid = false;
      }
      if (!schCity?.value) {
        messages.push("School City is required.");
        schCity?.classList.add("input-error");
        isValid = false;
      }
    }

    return { isValid, messages };
  }

  // Validate Institutional school dropdowns
  function validateInstitutionalFields() {
    const schName = document.getElementById('ins-school-name');
    const schType = document.getElementById('ins-school-type');
    const schRegion = document.getElementById('ins-school-region');
    const schProvince = document.getElementById('ins-school-province');
    const schCity = document.getElementById('ins-school-city');

    let isValid = true;
    let messages = [];

    const clearErrors = (elements) => {
      elements.forEach(el => el?.classList.remove('input-error'));
    };

    clearErrors([schName, schType, schRegion, schProvince, schCity]);

    if (!schName?.value.trim()) {
      messages.push("Institution School Name is required.");
      schName?.classList.add("input-error");
      isValid = false;
    }
    if (!schType?.value) {
      messages.push("Institution School Type is required.");
      schType?.classList.add("input-error");
      isValid = false;
    }
    if (!schRegion?.value) {
      messages.push("Institution School Region is required.");
      schRegion?.classList.add("input-error");
      isValid = false;
    }
    if (!schProvince?.value) {
      messages.push("Institution School Province is required.");
      schProvince?.classList.add("input-error");
      isValid = false;
    }
    if (!schCity?.value) {
      messages.push("Institution School City is required.");
      schCity?.classList.add("input-error");
      isValid = false;
    }

    return { isValid, messages };
  }

  // 🎯 Final submit validation wrapper
  document.addEventListener('DOMContentLoaded', () => {
    updateRequiredAttributes();

    document.getElementById('role')?.addEventListener('change', updateRequiredAttributes);

    const form = document.getElementById('registrationForm');
    if (form) {
      form.addEventListener('submit', function (event) {
        const role = document.getElementById('role')?.value;
        const individual = role === 'individual';
        const institutional = role === 'institution';

        const results = [];

        if (individual) results.push(validateIndividualAffiliation());
        if (institutional) results.push(validateInstitutionalFields());

        const allMessages = results.flatMap(r => r.messages);
        const anyInvalid = results.some(r => !r.isValid);

        if (anyInvalid) {
          event.preventDefault();
          alert("Please fix the following errors:\n" + allMessages.join("\n"));
        }
      });
    }
  });

  // Utility validators
  function isValidEmail(email) {
    return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
  }

  function isValidPhone(phone) {
    return /^09\d{9}$/.test(phone); // Starts with 09 and total 11 digits
  }

  // Password match and input format validation
  function validateBasicAccountFields() {
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirm = document.getElementById('confirmPassword');
    const phone = document.getElementById('phone');
    const emergencyPhone = document.getElementById('emergency-contact-number');

    let isValid = true;
    let messages = [];

    const clear = el => el?.classList.remove('input-error');

    clear(email);
    clear(password);
    clear(confirm);
    clear(phone);
    clear(emergencyPhone);

    if (!isValidEmail(email?.value)) {
      isValid = false;
      messages.push('Invalid email format.');
      email?.classList.add('input-error');
    }

    if (password?.value !== confirm?.value) {
      isValid = false;
      messages.push('Passwords do not match.');
      confirm?.classList.add('input-error');
    }

    if (!isValidPhone(phone?.value)) {
      isValid = false;
      messages.push('Phone number must start with "09" and be 11 digits.');
      phone?.classList.add('input-error');
    }

    if (!isValidPhone(emergencyPhone?.value)) {
      isValid = false;
      messages.push('Emergency contact number must start with "09" and be 11 digits.');
      emergencyPhone?.classList.add('input-error');
    }

    return { isValid, messages };
  }

  const form = document.getElementById('registrationForm');
  if (form) {
    form.addEventListener('submit', function (event) {
      const role = document.getElementById('role')?.value;

      const results = [validateBasicAccountFields()];

      if (role === 'individual') results.push(validateIndividualAffiliation());
      if (role === 'institution') results.push(validateInstitutionalFields());

      const messages = results.flatMap(r => r.messages);
      const hasErrors = results.some(r => !r.isValid);

      if (hasErrors) {
        event.preventDefault();
        alert("Please fix the following:\n" + messages.join("\n"));
      }
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    const email = document.getElementById('email');
    const phone = document.getElementById('phone');
    const emergencyPhone = document.getElementById('emergency-contact-number');
    const password = document.getElementById('password');
    const confirm = document.getElementById('confirmPassword');

    if (email) {
      email.addEventListener('input', () => {
        const valid = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value);
        email.classList.toggle('input-error', !valid && email.value.length > 0);
      });
    }

    const validatePhone = (input) => {
      const valid = /^09\d{9}$/.test(input.value);
      input.classList.toggle('input-error', !valid && input.value.length > 0);
    };

    if (phone) phone.addEventListener('input', () => validatePhone(phone));
    if (emergencyPhone) emergencyPhone.addEventListener('input', () => validatePhone(emergencyPhone));

    if (password && confirm) {
      const checkMatch = () => {
        const isMismatch = password.value !== confirm.value && confirm.value.length > 0;
        confirm.classList.toggle('input-error', isMismatch);
      };
      password.addEventListener('input', checkMatch);
      confirm.addEventListener('input', checkMatch);
    }
  });
});
