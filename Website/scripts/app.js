// Change this variable to your actual Codespace API URL
const API_URL = "https://ishfwilf-code50-102620886-q7g94qxvphxj77-8000.app.github.dev/api/employees";
const appRoot = document.getElementById('app-root');

async function loadEmployees() {
    const response = await fetch('https://ishfwilf-code50-102620886-q7g94qxvphxj77-8000.app.github.dev/api/employees');
    const employees = await response.json();

    const container = document.querySelector('#timelines .employee-list');
    container.innerHTML = ""; // Clear the "Jane Smith" mock data

    employees.forEach(emp => {
        container.innerHTML += `
            <div class="employee-card">
                <h3>${emp.name}</h3>
                <p>ID: ${emp.id}</p>
                <p>Status: <span class="badge">${emp.status}</span></p>
                <button onclick="viewDetails('${emp.id}')">View Timeline</button>
            </div>
        `;
    });
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", loadEmployees);



// 1. Helper function to wrap pages in the Sidebar/Header layout
function withLayout(title, contentHtml) {
    const user = JSON.parse(localStorage.getItem('inout_session')) || { email: 'Admin' };
    const hash = window.location.hash;

    return `
        <div class="app-container">
            <aside class="sidebar">
                <div class="brand-section">
                    <h1 class="text-gradient">MEDA:Inout</h1>
                    <span class="version-tag">v2.4.1 Enterprise</span>
                </div>

                <nav class="nav-list">
                    <div class="nav-group">
                        <label class="nav-label">MANAGEMENT</label>
                        <a href="#/dashboard" class="nav-item ${hash === '#/dashboard' ? 'active' : ''}">📊 Overview</a>
                        <a href="#/employees" class="nav-item ${hash === '#/employees' ? 'active' : ''}">👥 Employees</a>
                        <a href="#/screenshots" class="nav-item ${hash === '#/screenshots' ? 'active' : ''}">🖼️ Screenshots</a>
                        <a href="#/analytics" class="nav-item ${hash === '#/analytics' ? 'active' : ''}">📈 Analytics</a>
                        <a href="#/leave-management" class="nav-item ${hash === '#/leave-management' ? 'active' : ''}">📅 Leave Management</a>
                        <a href="#/reports" class="nav-item ${hash === '#/reports' ? 'active' : ''}">📄 Reports</a>
                    </div>

                    <div class="nav-group" style="margin-top: 2rem;">
                        <label class="nav-label">SYSTEM</label>
                        <a href="#/settings" class="nav-item ${hash === '#/settings' ? 'active' : ''}">⚙️ Settings</a>
                    </div>
                </nav>

                <div class="sidebar-footer">
                    <div class="user-info">
                        <div class="status-dot"></div>
                        <span>${user.email}</span>
                    </div>
                    <button onclick="logout()" class="logout-btn">Terminate Session</button>
                </div>
            </aside>
            <main class="main-content">
                <header class="top-header">
                    <h2>${title}</h2>
                    <div class="system-badge">● System Live</div>
                </header>
                <div class="content-padding">${contentHtml}</div>
            </main>
        </div>
    `;
}

// 2. Define UI Modules
const routes = {
    '/login': () => `
        <div class="login-container">
            <div class="glass-card login-card">
                <h1 class="text-gradient" style="font-size: 2.5rem;">Inout</h1>
                <p style="color: var(--text-muted); margin-bottom: 1.5rem;">MEDA HR Portal</p>
                <form id="login-form">
                    <div style="text-align:left; margin-bottom:1rem;">
                        <label style="font-size:0.8rem; color:var(--text-muted)">Email</label>
                        <input type="email" id="email" placeholder="demo@meda.test" required style="width:100%; padding:0.8rem; border-radius:8px; border:1px solid #ddd;">
                    </div>
                    <div style="text-align:left; margin-bottom:0.5rem;">
                        <label style="font-size:0.8rem; color:var(--text-muted)">Password</label>
                        <input type="password" id="password" placeholder="••••••••" required style="width:100%; padding:0.8rem; border-radius:8px; border:1px solid #ddd;">
                    </div>
                    <div style="text-align:right; margin-bottom:1rem;">
                        <a href="javascript:void(0)" onclick="showForgotPassword()" style="font-size:0.75rem; color:var(--text-muted); text-decoration:none;">Forgot password?</a>
                    </div>
                    <button type="submit" class="btn-primary" style="width:100%; padding:0.8rem; background:var(--gradient-brand); color:white; border:none; border-radius:8px; font-weight:600; cursor:pointer;">Sign In</button>
                    <div id="error-msg" style="color: #ef4444; font-size: 0.8rem; margin-top: 1rem; display: none;">Invalid credentials.</div>
                </form>
            </div>
        </div>
        <div id="reset-modal" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(15,23,42,0.6); display:none; justify-content:center; align-items:center; z-index:1000;" onclick="this.style.display='none'">
            <div class="glass-card" style="max-width:350px; padding:2rem; text-align:center;" onclick="event.stopPropagation()">
                <h3>Reset Password</h3>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin: 1rem 0;">Contact Admin for reset.</p>
                <button onclick="document.getElementById('reset-modal').style.display='none'" style="width:100%; padding:0.5rem;">Close</button>
            </div>
        </div>`,

'/dashboard': () => {
        const dashboardHtml = `
            <div class="stats-grid">
                <div class="glass-card kpi-card">
                    <span class="kpi-label">Active Employees</span>
                    <span class="kpi-value" id="active-emp-count">...</span>
                    <span class="kpi-trend trend-up">↑ 12% vs yesterday</span>
                </div>
                <div class="glass-card kpi-card">
                    <span class="kpi-label">Avg. Productivity</span>
                    <span class="kpi-value">88.4%</span>
                    <span class="kpi-trend trend-up">↑ 2.1% this week</span>
                </div>
                <div class="glass-card kpi-card">
                    <span class="kpi-label">Idle Time (Total)</span>
                    <span class="kpi-value">14h 22m</span>
                    <span class="kpi-trend trend-down">↓ 5% improvement</span>
                </div>
            </div>

            <div class="glass-card chart-container">
                <h3 style="margin-bottom: 1.5rem; font-size: 1.1rem;">Weekly Rendered Hours</h3>
                <div style="height: 300px; width: 100%;">
                    <canvas id="weeklyHoursChart"></canvas>
                </div>
            </div>
        `;

        // Small delay to ensure the DOM is ready before Chart.js looks for the ID
        setTimeout(() => {
        initDashboardChart();
        updateDashboardStats(); // Add this line here
    }, 100);

    return withLayout('Dashboard Overview', dashboardHtml);
},

'/employees': () => {
    const timelineHtml = `
        <div class="glass-card" style="padding: 2rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                <h3>Employee Directory</h3>
                <input type="text" placeholder="Search by name or ID..." class="search-bar" id="emp-search">
            </div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Designation</th>
                        <th>Status</th>
                        <th>Last Sync</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="employee-table-body">
                    <tr><td colspan="6" style="text-align:center;">Loading database...</td></tr>
                </tbody>
            </table>
        </div>
    `;

    // Trigger the real data fetch after the HTML is placed on the screen
    setTimeout(refreshEmployeeData, 50);

    return withLayout('Individual Timelines', timelineHtml);
},
'/screenshots': () => {
        // Mock data for screenshots
        const screenshots = [
            { id: 1, user: "Mark Espedido", time: "10:15 AM", url: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=500" },
            { id: 2, user: "Jane Smith", time: "10:12 AM", url: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=500" },
            { id: 3, user: "John Doe", time: "09:45 AM", url: "https://images.unsplash.com/photo-1587620962725-abab7fe55159?w=500" },
            { id: 4, user: "Alice Brown", time: "09:30 AM", url: "https://images.unsplash.com/photo-1550439062-609e1531270e?w=500" }
        ];

        const cards = screenshots.map(s => `
            <div class="glass-card screenshot-card">
                <img src="${s.url}" class="screenshot-img privacy-blur" alt="Work Evidence">
                <div class="screenshot-info">
                    <p style="font-weight:600; font-size:0.9rem;">${s.user}</p>
                    <span class="timestamp-label">Captured at ${s.time}</span>
                </div>
            </div>
        `).join('');

        const galleryHtml = `
            <div class="privacy-toggle-container">
                <label style="font-size:0.85rem; font-weight:600; cursor:pointer;">
                    <input type="checkbox" id="privacy-toggle" checked style="margin-right:8px;">
                    Enable Privacy Blurring (AI Filter)
                </label>
            </div>

            <div class="gallery-grid">
                ${cards}
            </div>
        `;

        // Logic to toggle the blur effect
        setTimeout(() => {
            const toggle = document.getElementById('privacy-toggle');
            if (toggle) {
                toggle.addEventListener('change', (e) => {
                    const images = document.querySelectorAll('.screenshot-img');
                    images.forEach(img => {
                        if (e.target.checked) {
                            img.classList.add('privacy-blur');
                        } else {
                            img.classList.remove('privacy-blur');
                        }
                    });
                });
            }
        }, 100);

        return withLayout('Screenshot Review', galleryHtml);
    },
'/analytics': () => withLayout('System Analytics', `
        <div class="analytics-container">
            <div class="glass-card chart-main">
                <h3>Productivity Trend</h3>
                <canvas id="productivityChart"></canvas>
            </div>
            <div class="analytics-grid">
                <div class="glass-card">
                    <h3>App Usage Distribution</h3>
                    <canvas id="appUsageChart"></canvas>
                </div>
                <div class="glass-card">
                    <h3>Idle vs Active Time</h3>
                    <canvas id="idleActiveChart"></canvas>
                </div>
            </div>
        </div>
`),

'/leave-management': () => {
    const html = withLayout('Leave Management', `
        <div class="leave-container">
            <div class="glass-card">
                <h3 style="color: var(--text-main); margin-bottom: 20px;">Pending Requests</h3>
                <div class="leave-list" id="leave-list-container">
                    <div class="leave-item-card glass-card">
                        <div style="display:flex; align-items:center; gap:15px;">
                            <div class="user-avatar-mini">MC</div>
                            <div>
                                <strong style="color:white">Marcus Chen</strong><br>
                                <small style="color:var(--text-muted)">Engineering • Vacation</small>
                            </div>
                        </div>
                        <div class="leave-actions">
                            <button class="btn-approve">✔</button>
                            <button class="btn-reject">✖</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `);
    return html;
},

'/reports': () => withLayout('Reports', `
    <div class="reports-grid">
        <div class="glass-card report-item">
            <h4>Attendance Report</h4>
            <button class="btn-primary">Download CSV</button>
        </div>
        <div class="glass-card report-item">
            <h4>Activity Summary</h4>
            <button class="btn-primary">Generate PDF</button>
        </div>
    </div>
`),
'/settings': () => {
        const settingsHtml = `
            <div class="glass-card" style="padding: 2.5rem;">
                <div class="settings-section">
                    <h3 style="margin-bottom: 1.5rem;">Data Retention & Privacy</h3>

                    <div class="settings-row">
                        <div class="settings-info">
                            <span class="settings-title">Log Retention Period</span>
                            <span class="settings-desc">How many days should attendance and activity logs be stored?</span>
                        </div>
                        <input type="number" class="input-small" value="90">
                    </div>

                    <div class="settings-row">
                        <div class="settings-info">
                            <span class="settings-title">Screenshot Blur Intensity</span>
                            <span class="settings-desc">Default blurring level for employee screen captures.</span>
                        </div>
                        <select class="input-small" style="width: 120px;">
                            <option>Low</option>
                            <option selected>Medium</option>
                            <option>High (Strict)</option>
                        </select>
                    </div>

                    <div class="settings-row">
                        <div class="settings-info">
                            <span class="settings-title">Automated Idle Detection</span>
                            <span class="settings-desc">Mark employee as 'Idle' after 5 minutes of no activity.</span>
                        </div>
                        <input type="checkbox" checked style="width:20px; height:20px; cursor:pointer;">
                    </div>
                </div>

                <div class="settings-section" style="border-top: 2px solid #f8fafc; padding-top: 1.5rem;">
                    <h3 style="margin-bottom: 1rem;">System Alerts</h3>
                    <div class="settings-row">
                        <div class="settings-info">
                            <span class="settings-title">Late Arrival Notifications</span>
                            <span class="settings-desc">Email HR when an employee logs in 15+ minutes late.</span>
                        </div>
                        <input type="checkbox" style="width:20px; height:20px; cursor:pointer;">
                    </div>
                </div>

                <button class="btn-save" onclick="saveSettings()">Save Configuration</button>
                <p id="save-status" style="display:none; color:#10b981; font-size:0.85rem; margin-top:1rem; font-weight:600;">✓ Settings updated successfully!</p>
            </div>
        `;
        return withLayout('Organization Settings', settingsHtml);
    },
};

// 3. Core Logic
window.showForgotPassword = () => document.getElementById('reset-modal').style.display = 'flex';

window.logout = () => {
    localStorage.removeItem('inout_session');
    window.location.hash = '/login';
};

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMsg = document.getElementById('error-msg');

    try {
        const response = await fetch('https://ishfwilf-code50-102620886-q7g94qxvphxj77-8000.app.github.dev/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            // Data includes name and role from backend
            localStorage.setItem('inout_session', JSON.stringify(data.user));
            window.location.hash = '/dashboard';
        } else {
            errorMsg.innerText = "Invalid credentials. Access denied.";
            errorMsg.style.display = 'block';
        }
    } catch (err) {
        errorMsg.innerText = "Server connection failed.";
        errorMsg.style.display = 'block';
    }
}

function router() {
    const hash = window.location.hash.slice(1) || '/login';
    const session = localStorage.getItem('inout_session');

    if (!session && hash !== '/login') {
        window.location.hash = '/login';
        return;
    }

    const viewFn = routes[hash] || (() => '<h1>404</h1>');
    appRoot.innerHTML = viewFn();

    if (hash === '/login') {
        document.getElementById('login-form').addEventListener('submit', handleLogin);
    }
    // Trigger chart rendering if on analytics page
    if (hash === '/analytics') {
        initAnalytics();
    }
}
window.addEventListener('hashchange', () => {
    const route = window.location.hash.replace('#', '');
    handleNavigation(route);
});
window.addEventListener('hashchange', router);
window.addEventListener('DOMContentLoaded', router);
// Global function to handle button clicks
window.handleLeaveAction = function(leaveId, action) {
    const row = document.getElementById(`leave-row-${leaveId}`);

    if (action === 'approve') {
        alert("Request Approved");
        row.style.border = "1px solid #22c55e";
        row.style.opacity = "0.5";
        // In a real app, you'd fetch() to your FastAPI backend here
    } else {
        alert("Request Rejected");
        row.style.border = "1px solid #ef4444";
        row.style.opacity = "0.5";
    }

    // Optional: Remove the row after a delay
    setTimeout(() => {
        row.style.display = 'none';
    }, 1000);
};
function initDashboardChart() {
    const ctx = document.getElementById('weeklyHoursChart');
    if (!ctx) return;

    // Destroy existing chart instance if it exists to prevent glitches on re-navigation
    if (window.myDashboardChart) {
        window.myDashboardChart.destroy();
    }

    window.myDashboardChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Work Hours',
                data: [310, 425, 380, 460, 415, 120, 85],
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#6366f1'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#f1f5f9' },
                    ticks: { font: { family: 'Inter' } }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { family: 'Inter' } }
                }
            }
        }
    });
}

function renderEmployeeRows(data) {
    const tbody = document.getElementById('employee-table-body');
    if (!tbody) return;
    tbody.innerHTML = data.map(emp => `
        <tr>
            <td><b>${emp.id}</b></td>
            <td>${emp.name}</td>
            <td>${emp.role}</td>
            <td><span class="status-badge ${emp.status === 'Active' ? 'status-active' : 'status-idle'}">${emp.status}</span></td>
            <td>${emp.lastSync}</td>
            <td><a href="javascript:void(0)" class="btn-view">View Logs →</a></td>
        </tr>
    `).join('');
}

window.saveSettings = () => {
    const status = document.getElementById('save-status');
    if (status) {
        status.style.display = 'block';
        setTimeout(() => {
            status.style.display = 'none';
        }, 3000);
    }
};

function handleNavigation(route) {
    // Hide all sections first
    document.querySelectorAll('.page-section').forEach(section => {
        section.style.display = 'none';
    });

    // Show the one we want
    const activeSection = document.getElementById(route);
    if (activeSection) {
        activeSection.style.display = 'block';
        if (route === 'timelines') {
            loadEmployees(); // Refresh data from PostgreSQL when clicking Timelines
        }
    }
}

async function refreshEmployeeData() {
    const tbody = document.getElementById('employee-table-body');
    if (!tbody) return;

    try {
        const response = await fetch('https://ishfwilf-code50-102620886-q7g94qxvphxj77-8000.app.github.dev/api/employees');
        const employees = await response.json();

        if (employees.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No employees found in database.</td></tr>';
            return;
        }

        tbody.innerHTML = employees.map(emp => `
            <tr>
                <td><b>${emp.id}</b></td>
                <td>${emp.name}</td>
                <td>${emp.role || 'N/A'}</td>
                <td><span class="status-badge ${emp.status === 'Online' ? 'status-active' : 'status-idle'}">${emp.status}</span></td>
                <td>${new Date(emp.last_sync).toLocaleString()}</td>
                <td><a href="javascript:void(0)" class="btn-view">View Logs →</a></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error("Database connection failed:", error);
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:red;">Error: Could not connect to Backend</td></tr>';
    }
}
async function updateDashboardStats() {
    try {
        const response = await fetch('https://ishfwilf-code50-102620886-q7g94qxvphxj77-8000.app.github.dev/api/employees');
        const employees = await response.json();

        const countElement = document.getElementById('active-emp-count');
        if (countElement) {
            // This replaces the "..." with the actual number of employees in Postgres
            countElement.innerText = employees.length;
        }
    } catch (e) {
        console.error("Failed to update dashboard stats:", e);
    }
}
// Helper function to initialize charts after rendering
function initAnalytics() {
    const ctxTrend = document.getElementById('productivityChart');
    if (!ctxTrend) return;

    // Common Chart Options for Dark Theme
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: '#94a3b8', font: { family: 'Inter' } } }
        },
        scales: {
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
        }
    };

    // 1. Productivity Trend (Line Chart)
    new Chart(ctxTrend, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            datasets: [{
                label: 'Avg Productivity %',
                data: [75, 82, 78, 90, 85],
                borderColor: '#9333ea',
                backgroundColor: 'rgba(147, 51, 234, 0.2)',
                fill: true,
                tension: 0.4
            }]
        },
        options: chartOptions
    });

    // 2. App Usage (Doughnut)
    new Chart(document.getElementById('appUsageChart'), {
        type: 'doughnut',
        data: {
            labels: ['VS Code', 'Chrome', 'Discord', 'Terminal'],
            datasets: [{
                data: [45, 25, 15, 15],
                backgroundColor: ['#9333ea', '#c084fc', '#ec4899', '#1e293b'],
                borderWidth: 0
            }]
        },
        options: { plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } } }
    });
    // 3. Idle vs Active Time (Bar Chart)
    new Chart(document.getElementById('idleActiveChart'), {
        type: 'bar',
        data: {
            labels: ['Mark Espedido', 'Jane Smith', 'John Doe', 'Alice Brown'],
        datasets: [
                    { label: 'Active', data: [6, 7, 5, 4, 6], backgroundColor: '#9333ea' },
                    { label: 'Idle', data: [1, 0.5, 2, 3, 1], backgroundColor: '#334155' }
                ]
            },
            options: chartOptions // Now this will work!
        });
}
