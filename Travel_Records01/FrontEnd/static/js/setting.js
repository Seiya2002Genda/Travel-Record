// =========================
// LOAD USER
// =========================
async function loadUser() {

    const res = await fetch("/api/account");
    const data = await res.json();

    if (!data.success) return;

    const u = data.user;

    username.value = u.username;
    first_name.value = u.first_name;
    last_name.value = u.last_name;
    email.value = u.email;
}

// =========================
// LOAD SETTINGS
// =========================
async function loadSettings() {

    const res = await fetch("/api/settings");
    const data = await res.json();

    const box = document.getElementById("settingsBox");
    box.innerHTML = "";

    const settings = data.settings;

    for (let key in settings) {
        box.innerHTML += `<p><b>${key}</b>: ${settings[key]}</p>`;
    }
}

// =========================
// UPDATE ACCOUNT
// =========================
document.getElementById("accountForm").addEventListener("submit", async e => {
    e.preventDefault();

    const res = await fetch("/api/account", {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: username.value,
            first_name: first_name.value,
            last_name: last_name.value,
            email: email.value
        })
    });

    const result = await res.json();
    showMessage(result);
});

// =========================
// CHANGE PASSWORD
// =========================
document.getElementById("passwordForm").addEventListener("submit", async e => {
    e.preventDefault();

    const res = await fetch("/api/account/password", {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            new_password: new_password.value
        })
    });

    const result = await res.json();
    showMessage(result);
});

// =========================
// MESSAGE
// =========================
function showMessage(result) {
    const msg = document.getElementById("message");

    msg.style.color = result.success ? "green" : "red";
    msg.textContent = result.message;
}

// =========================
// INIT
// =========================
window.onload = () => {
    loadUser();
    loadSettings();
};