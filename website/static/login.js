document.addEventListener('DOMContentLoaded', () => {
    console.log("Login JavaScript loaded"); // Debugging line
    const loginForm = document.getElementById('loginForm');

    if (!loginForm) {
        console.error("Login form not found!"); // Debugging line
        return; // Exit if the form is not found
    }

    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    if (!emailInput || !passwordInput) {
        console.error("Email or password input not found!"); // Debugging line
        return; // Exit if inputs are not found
    }

    loginForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission

        const email = emailInput.value; // Access the value of the email input
        const password = passwordInput.value; // Access the value of the password input

        // Perform login request
        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.json();
        })
        .then(data => {
            // Handle successful login
            console.log('Login successful:', data);
            // Redirect to the user dashboard
            window.location.href = '/userdashboard'; // Change this to your actual dashboard URL
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Login failed. Please check your credentials and try again.');
        });
    });
});
