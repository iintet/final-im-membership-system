document.getElementById("registrationForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Perform additional validation here...

    const formData = new FormData(this);
    const data = {};

    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch('/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Registration failed');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        window.location.href = "/userdashboard";
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during registration. Please try again.');
    });
});
