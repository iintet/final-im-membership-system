document.getElementById("registrationForm").addEventListener("submit", function(event) {
    event.preventDefault();

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
            return response.json().then(err => { throw new Error(err.error); });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        window.location.href = "/userdashboard"; // Redirect to user dashboard
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during registration: ' + error.message);
    });
});
