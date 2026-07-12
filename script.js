const BASE = "http://127.0.0.1:8000";

let chart;
let map;
let lastId = null;
let logCount = 0;

// 🌍 animation tracking
let lastAttackPoint = null;

window.onload = () => {
    init();
    setInterval(fetchLogs, 1500);
};

// ================= INIT =================

function init() {

    chart = new Chart(document.getElementById("chartCanvas"), {
        type: "line",
        data: {
            labels: [],
            datasets: [
                {
                    label: "Normal",
                    borderColor: "#00ffcc",
                    data: []
                },
                {
                    label: "Threat",
                    borderColor: "#ff0040",
                    data: []
                },
                {
                    label: "Threshold",
                    borderColor: "#ffd000",
                    borderDash: [5,5],
                    data: []
                }
            ]
        },
        options: {
            scales: {
                y: { min: 0, max: 1 }
            }
        }
    });

    map = L.map('map').setView([20, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
        .addTo(map);

    fetchStats();
}

// ================= FETCH LOGS =================

async function fetchLogs() {

    try {
        const res = await fetch(BASE + "/logs");
        const data = await res.json();

        if (!data.logs.length) return;

        const latest = data.logs[0];

        if (lastId !== latest.id) {
            lastId = latest.id;
            update(latest);
        }

    } catch (e) {
        console.log("Fetch error:", e);
    }
}

// ================= FETCH STATS =================

async function fetchStats() {

    try {
        const res = await fetch(BASE + "/stats");
        const data = await res.json();

        document.getElementById("total").innerText = data.total ?? 0;
        document.getElementById("threats").innerText = data.threats ?? 0;
        document.getElementById("normal").innerText = data.normal ?? 0;
        document.getElementById("rate").innerText =
            (data.threat_rate_pct ?? 0) + "%";

    } catch (e) {
        console.log("Stats error:", e);
    }
}

// ================= BUTTONS =================

async function simulate() {
    const res = await fetch(BASE + "/simulate");
    const data = await res.json();
    update(data); // instant update
}

async function burst() {
    const res = await fetch(BASE + "/simulate/burst");
    const data = await res.json();
    data.forEach(update);
}

async function clearLogs() {
    await fetch(BASE + "/clear", { method: "DELETE" });
    location.reload();
}

// ================= UPDATE =================

function update(log) {

    logCount++;

    // ================= TABLE =================
    const tbody = document.getElementById("tbody");

    tbody.innerHTML =
    `<tr>
        <td>${log.time}</td>
        <td>${log.ip}</td>
        <td>${log.activity}</td>
        <td class="${log.status === "THREAT" ? "threat" : "normal"}">
            ${log.status}
        </td>
        <td>${log.score}</td>
    </tr>` + tbody.innerHTML;

    // ================= CHART =================
    chart.data.labels.push(chart.data.labels.length + 1);
    chart.data.datasets[2].data.push(0.55);

    if (log.status === "THREAT") {
        chart.data.datasets[1].data.push(log.score);
        chart.data.datasets[0].data.push(null);
    } else {
        chart.data.datasets[0].data.push(log.score);
        chart.data.datasets[1].data.push(null);
    }

    if (chart.data.labels.length > 20) {
        chart.data.labels.shift();
        chart.data.datasets.forEach(d => d.data.shift());
    }

    chart.update();

    // ================= MAP =================

    const currentPoint = [log.lat, log.lon];

    // 🔴 BLINKING RADAR POINT
    const marker = L.circleMarker(currentPoint, {
        radius: 6,
        color: log.status === "THREAT" ? "#ff0040" : "#00ff66",
        fillOpacity: 0.7
    }).addTo(map);

    // 🔥 pulse animation
    let pulseRadius = 6;

    const pulse = setInterval(() => {
        pulseRadius += 2;
        marker.setRadius(pulseRadius);

        if (pulseRadius > 20) {
            pulseRadius = 6;
        }
    }, 200);

    // 🌍 ATTACK LINE
    if (lastAttackPoint) {

        const line = L.polyline([lastAttackPoint, currentPoint], {
            color: log.status === "THREAT" ? "#ff0040" : "#00ff66",
            weight: 2,
            opacity: 0.7
        }).addTo(map);

        let opacity = 0.7;

        const fade = setInterval(() => {
            opacity -= 0.05;
            line.setStyle({ opacity });

            if (opacity <= 0) {
                map.removeLayer(line);
                clearInterval(fade);
            }
        }, 100);
    }

    lastAttackPoint = currentPoint;

    // ================= TERMINAL =================

    const terminal = document.getElementById("terminal");

    terminal.innerHTML =
        `[${logCount}] [${log.time}] ${log.ip} → ${log.activity} (${log.status})<br>`
        + terminal.innerHTML;

    // ================= STATS =================
    fetchStats();
}