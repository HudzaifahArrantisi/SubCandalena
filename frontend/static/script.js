// Auto-refresh dashboard
setInterval(loadDashboard, 5000);

async function loadDashboard() {
    const response = await fetch('/api/results');
    const data = await response.json();
    
    document.getElementById('stats-cards').innerHTML = `
        <div class="col-md-3">
            <div class="stats-card text-center">
                <h3>${data.total}</h3>
                <p>Total Subdomains</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stats-card high-risk text-center">
                <h3>${data.high_risk}</h3>
                <p>High Risk</p>
            </div>
        </div>
    `;
    
    // Update table
    createTable(data.data);
}

function createTable(data) {
    let html = `
        <table class="table table-hover">
            <thead><tr>
                <th>Subdomain</th>
                <th>Status</th>
               th>Risk</th>
                <th>Tech</th>
            </tr></thead>
            <tbody>
    `;
    
    data.forEach(row => {
        const riskClass = row.risk_score > 70 ? 'high-risk' : 'medium-risk';
        html += `
            <tr class="${riskClass}">
                <td><a href="${row.url}" target="_blank">${row.subdomain}</a></td>
                <td>${row.status_code}</td>
                <td><strong>${row.risk_score}%</strong></td>
                <td>${row.tech_stack}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    document.getElementById('subdomains-table').innerHTML = html;
}