document.addEventListener('DOMContentLoaded', () => {
    console.log("Login JavaScript loaded");

    const loginForm = document.getElementById('loginForm');

    if (!loginForm) {
        console.error("Login form not found!");
        return;
    }

    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    if (!emailInput || !passwordInput) {
        console.error("Email or password input not found!");
        return;
    }

    loginForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

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
            if (data.user.user_type === 'staff') {
                window.location.href = '/admindashboard';
            } else if (data.user.user_type === 'member') {
                window.location.href = '/userdashboard';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Login failed. Please check your credentials and try again.');
        });
    });
});
