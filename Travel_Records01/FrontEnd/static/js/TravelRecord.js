let travelId = null;

// =========================
// GET QUERY PARAM
// =========================
function getTravelId() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

// =========================
// LOAD DATA
// =========================
async function loadTravel() {

    travelId = getTravelId();
    if (!travelId) return;

    const res = await fetch(`/api/travel/${travelId}`);
    const data = await res.json();

    const travel = data.travel;
    const days = data.days;

    document.getElementById("travelDetail").innerHTML = `
        <h3>${travel.destination}</h3>
        <p>${travel.start_date} → ${travel.end_date}</p>
        <p>${travel.purpose}</p>
        <p>${travel.impression || ""}</p>
    `;

    const list = document.getElementById("dayList");
    list.innerHTML = "";

    days.forEach(d => {
        list.innerHTML += `
            <div class="day-card">
                <h4>${d.day_date}</h4>
                <p>${d.day_destination}</p>
                <p>${d.activities || ""}</p>
                <p>${d.day_impression || ""}</p>
                <p>$${d.day_cost}</p>
            </div>
        `;
    });
}

// =========================
// CREATE TRAVEL
// =========================
document.getElementById("travelForm").addEventListener("submit", async e => {
    e.preventDefault();

    const data = {
        destination: destination.value,
        start_date: start_date.value,
        end_date: end_date.value,
        purpose: purpose.value,
        impression: impression.value,
        total_cost: total_cost.value
    };

    const res = await fetch("/api/travel", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (result.success) {
        alert("Created!");
        window.location.href = `/TravelRecord?id=${result.id}`;
    } else {
        alert(result.message);
    }
});

// =========================
// ADD DAY
// =========================
document.getElementById("dayForm").addEventListener("submit", async e => {
    e.preventDefault();

    if (!travelId) {
        alert("Create travel first");
        return;
    }

    const data = {
        travel_id: travelId,
        day_date: day_date.value,
        day_destination: day_destination.value,
        activities: activities.value,
        day_impression: day_impression.value,
        day_cost: day_cost.value
    };

    const res = await fetch("/api/travel/day", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (result.success) {
        loadTravel();
    } else {
        alert(result.message);
    }
});

window.onload = loadTravel;