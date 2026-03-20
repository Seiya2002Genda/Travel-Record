let userEmail = "";

async function sendOTP() {
    userEmail = document.getElementById("email").value;

    const res = await fetch("/api/send-otp", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email: userEmail })
    });

    const result = await res.json();
    showMessage(result);

    if (result.success) {
        document.getElementById("step1").style.display = "none";
        document.getElementById("step2").style.display = "block";
    }
}

async function verifyOTP() {
    const otp = document.getElementById("otp").value;

    const res = await fetch("/api/verify-otp", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email: userEmail, otp })
    });

    const result = await res.json();
    showMessage(result);

    if (result.success) {
        document.getElementById("step2").style.display = "none";
        document.getElementById("step3").style.display = "block";
    }
}

async function resetPassword() {
    const password = document.getElementById("new_password").value;

    const res = await fetch("/api/reset-password", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email: userEmail, password })
    });

    const result = await res.json();
    showMessage(result);

    if (result.success) {
        setTimeout(() => window.location.href = "/login", 1500);
    }
}

function showMessage(result) {
    const msg = document.getElementById("message");
    msg.style.color = result.success ? "green" : "red";
    msg.textContent = result.message;
}