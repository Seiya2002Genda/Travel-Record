document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value
    };

    const response = await fetch("/login", {
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
        message.textContent = "Login successful! Redirecting...";

        setTimeout(() => {
            window.location.href = "/dashboard";
        }, 1000);
    } else {
        message.style.color = "red";
        message.textContent = result.message;
    }
});