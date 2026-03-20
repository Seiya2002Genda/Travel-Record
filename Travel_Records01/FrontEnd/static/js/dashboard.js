async function loadTravels() {

    const response = await fetch("/api/travels");
    const data = await response.json();

    const container = document.getElementById("travelList");
    container.innerHTML = "";

    if (data.length === 0) {
        container.innerHTML = "<p>No travel records yet.</p>";
        return;
    }

    data.forEach(travel => {

        const card = document.createElement("div");
        card.className = "travel-card";

        card.innerHTML = `
            <h3>${travel.destination}</h3>
            <p>${travel.start_date} → ${travel.end_date}</p>
            <p>${travel.purpose}</p>
            <button onclick="viewTravel(${travel.id})">View</button>
        `;

        container.appendChild(card);
    });
}

function viewTravel(id) {
    window.location.href = `/TravelRecord?id=${id}`;
}

window.onload = loadTravels;