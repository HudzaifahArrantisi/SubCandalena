let activeScanId = null;

document.getElementById("scanForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const domain = document.getElementById("domainInput").value.trim();
    if (!domain) return;

    const response = await fetch("/api/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({domain})
    });
    const data = await response.json();
    if (!response.ok) {
        setStatus(data.detail || "Scan failed to start.");
        return;
    }
    activeScanId = data.scan_id;
    setStatus(`Scan queued for ${data.domain}.`);
    pollStatus();
});

document.getElementById("tableFilter").addEventListener("input", (event) => {
    const value = event.target.value.toLowerCase();
    document.querySelectorAll("#resultsBody tr").forEach((row) => {
        row.style.display = row.textContent.toLowerCase().includes(value) ? "" : "none";
    });
});

async function pollStatus() {
    if (!activeScanId) return;
    const response = await fetch(`/api/status/${activeScanId}`);
    const data = await response.json();
    setStatus(`Scan ${data.status}. Progress ${data.progress || 0}%.`);
    await loadDashboard();
    if (data.status === "queued" || data.status === "running") {
        setTimeout(pollStatus, 4000);
    }
}

async function loadDashboard() {
    const response = await fetch("/api/results");
    const data = await response.json();
    renderStats(data);
    renderRows(data.data || []);
}

function renderStats(data) {
    document.getElementById("statsCards").innerHTML = `
        <div class="stat"><strong>${data.total || data.count || 0}</strong><span>Total Subdomains</span></div>
        <div class="stat"><strong>${data.live || 0}</strong><span>Live</span></div>
        <div class="stat"><strong>${data.high_risk || 0}</strong><span>High Risk</span></div>
    `;
}

function renderRows(rows) {
    const body = document.getElementById("resultsBody");
    body.innerHTML = rows.map((row) => {
        const riskLevel = row.risk_level || "low";
        const riskClass = `risk-${riskLevel}`;
        const url = row.url || `https://${row.subdomain}`;
        return `
            <tr>
                <td><a href="${escapeAttr(url)}" target="_blank" rel="noreferrer">${escapeHtml(row.subdomain || "")}</a></td>
                <td>${escapeHtml(row.ip_address || "N/A")}</td>
                <td>${escapeHtml(row.status_code ?? "N/A")}</td>
                <td>${escapeHtml(row.title || "N/A")}</td>
                <td>${escapeHtml(row.tech_stack || "Unknown")}</td>
                <td class="${riskClass}">${escapeHtml(riskLevel)} (${escapeHtml(row.risk_score ?? 0)})</td>
                <td>${escapeHtml(row.source || "Unknown")}</td>
            </tr>
        `;
    }).join("");
}

function setStatus(message) {
    document.getElementById("jobStatus").textContent = message;
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function escapeAttr(value) {
    return escapeHtml(value).replaceAll("`", "&#096;");
}

loadDashboard();
setInterval(loadDashboard, 8000);
