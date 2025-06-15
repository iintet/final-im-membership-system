// static/login.js

// Wait for the DOM to fully load before attaching event listeners
document.addEventListener('DOMContentLoaded', function() {
  // Attach the event listener to the login form
  document.querySelector('.login-form form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = this.querySelector('input[type="email"]').value;
    const password = this.querySelector('input[type="password"]').value;

    try {
      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email, password })
      });
      
      const data = await response.json();

      if (response.ok) {
        alert('Login successful!');
        // Optionally redirect user, e.g., to dashboard:
        // window.location.href = '/dashboard';
      } else {
        alert('Login failed: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      alert('Error during login: ' + error.message);
    }
  });
});
