document.addEventListener('DOMContentLoaded', () => {
  // Utility helpers
  const isSkippable = (el) => el?.id === 'middle-name';
  const isValidEmail = (val) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(val);
  const isValidPhone = (val) => /^09\d{9}$/.test(val);

  // Set required fields based on selected role
  function updateRequiredAttributes() {
    const role = document.getElementById('role')?.value;
    const individualFields = document.querySelectorAll('#individual-fields input, #individual-fields select');
    const institutionFields = document.querySelectorAll('#institution-fields input, #institution-fields select');

    individualFields.forEach(el => isSkippable(el) ? el.removeAttribute('required') : el.setAttribute('required', ''));
    institutionFields.forEach(el => el.removeAttribute('required'));

    if (role === 'institution') {
      institutionFields.forEach(el => el.setAttribute('required', ''));
      individualFields.forEach(el => el.removeAttribute('required'));
    }
  }

  // Live feedback on email, phone, confirm-password
  function attachLiveValidation() {
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirm = document.getElementById('confirm-password');
    const phone = document.getElementById('phone');
    const emergencyIndiv = document.getElementById('emergency-contact-number-indiv');
    const emergencyInst = document.getElementById('emergency-contact-number-inst');

    email?.addEventListener('input', () => {
      email.classList.toggle('input-error', !isValidEmail(email.value));
    });

    [phone, emergencyIndiv, emergencyInst].forEach(field => {
      field?.addEventListener('input', () => {
        field.classList.toggle('input-error', !isValidPhone(field.value));
      });
    });

    if (password && confirm) {
      const matchCheck = () => {
        confirm.classList.toggle('input-error', password.value !== confirm.value);
      };
      password.addEventListener('input', matchCheck);
      confirm.addEventListener('input', matchCheck);
    }
  }

  function isVisible(el) {
    return !!(el && el.offsetParent !== null);
  }
  
  function validateBasicAccountFields() {
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirm = document.getElementById('confirm-password');
    const phone = document.getElementById('phone');
    const emergencyContactIndiv = document.getElementById('emergency-contact-number-indiv');
    const emergencyContactInst = document.getElementById('emergency-contact-number-inst');

    const fields = [email, password, confirm, phone, emergencyContactIndiv, emergencyContactInst];
    fields.forEach(f => f?.classList.remove('input-error'));

    const messages = [];
    if (email && !isValidEmail(email.value)) {
      email.classList.add('input-error');
      messages.push('Invalid email format.');
    }

    if (password && confirm && password.value !== confirm.value) {
      confirm.classList.add('input-error');
      messages.push('Passwords do not match.');
    }

    if (phone && !isValidPhone(phone.value)) {
      phone.classList.add('input-error');
      messages.push('Phone number must start with "09" and be 11 digits.');
    }

    if (emergencyContactIndiv && !isValidPhone(emergencyContactIndiv.value)) {
      emergencyContactIndiv.classList.add('input-error');
      messages.push('Individual emergency contact must start with "09" and be 11 digits.');
    }

    if (emergencyContactInst && !isValidPhone(emergencyContactInst.value)) {
      emergencyContactInst.classList.add('input-error');
      messages.push('Institution emergency contact must start with "09" and be 11 digits.');
    }

    return { isValid: messages.length === 0, messages };
  }

  function validateIndividualAffiliation() {
    const type = document.getElementById('affiliation-type')?.value;
    const fields = {
      organization: [
        { id: 'organization-name', label: 'Organization Name' },
        { id: 'organization-address', label: 'Organization Address' }
      ],
      school: [
        { id: 'ind-school-name', label: 'School Name' },
        { id: 'ind-school-type', label: 'School Type' },
        { id: 'ind-school-region', label: 'School Region' },
        { id: 'ind-school-province', label: 'School Province' },
        { id: 'ind-school-city', label: 'School City' }
      ]
    };

    const group = fields[type] || [];
    const messages = [];

    group.forEach(({ id, label }) => {
      const el = document.getElementById(id);
      el?.classList.remove('input-error');
      if (!el?.value.trim()) {
        el?.classList.add('input-error');
        messages.push(`${label} is required.`);
      }
    });

    return { isValid: messages.length === 0, messages };
  }

  function validateInstitutionalFields() {
    const ids = ['ins-school-name', 'ins-school-type', 'ins-school-region', 'ins-school-province', 'ins-school-city'];
    const messages = [];

    ids.forEach(id => {
      const el = document.getElementById(id);
      el?.classList.remove('input-error');
      if (!el?.value.trim()) {
        el?.classList.add('input-error');
        const label = el?.previousElementSibling?.textContent || id;
        messages.push(`${label} is required.`);
      }
    });

    return { isValid: messages.length === 0, messages };
  }

  const form = document.getElementById('registrationForm');
  if (form) {
    updateRequiredAttributes();
    attachLiveValidation();

    document.getElementById('role')?.addEventListener('change', updateRequiredAttributes);

    form.addEventListener('submit', (event) => {
      const role = document.getElementById('role')?.value;
      const results = [validateBasicAccountFields()];

      if (role === 'individual') results.push(validateIndividualAffiliation());
      if (role === 'institution') results.push(validateInstitutionalFields());

      const errors = results.flatMap(r => r.messages);
      const hasErrors = results.some(r => !r.isValid);

      if (hasErrors) {
        event.preventDefault();
        alert('Please fix the following:\n\n' + errors.join('\n'));
      }
    });
  }

  const middle = document.getElementById('middle-name');
    if (middle) middle.removeAttribute('required');

});
