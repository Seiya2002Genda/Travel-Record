document.getElementById("signupForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        username: document.getElementById("username").value,
        first_name: document.getElementById("first_name").value,
        last_name: document.getElementById("last_name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    const response = await fetch("/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    const message = document.getElementById("message");

    if (result.success) {
        message.style.color = "green";
        message.textContent = "Account created! Redirecting...";

        setTimeout(() => {
            window.location.href = "/login";
        }, 1500);
    } else {
        message.style.color = "red";
        message.textContent = result.message;
    }
});