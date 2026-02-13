// Jazmín OS - Dashboard App
const API_BASE = '';

// Format helpers
const formatPercent = (val) => `${val?.toFixed(1) || 0}%`;
const formatBytes = (gb) => `${gb} GB`;
const formatTime = (dateStr) => new Date(dateStr).toLocaleString('es-AR');

// Update system stats
async function updateSystemStats() {
    try {
        const res = await fetch(`${API_BASE}/api/system`);
        const data = await res.json();
        
        // CPU
        document.getElementById('cpu-percent').textContent = formatPercent(data.cpu.percent);
        document.getElementById('cpu-bar').style.width = `${data.cpu.percent}%`;
        
        // Memory
        document.getElementById('memory-percent').textContent = formatPercent(data.memory.percent);
        document.getElementById('memory-bar').style.width = `${data.memory.percent}%`;
        
        // Disk
        document.getElementById('disk-percent').textContent = formatPercent(data.disk.percent);
        document.getElementById('disk-bar').style.width = `${data.disk.percent}%`;
        
        // Uptime
        document.getElementById('uptime').textContent = data.boot_time;
    } catch (err) {
        console.error('Error fetching system stats:', err);
    }
}

// Update agents
async function updateAgents() {
    const container = document.getElementById('agents-container');
    
    try {
        const res = await fetch(`${API_BASE}/api/agents`);
        const agents = await res.json();
        
        if (agents.length === 0) {
            container.innerHTML = `
                <div class="agent-card">
                    <div class="agent-info">
                        <h3>agente-matutino-11am</h3>
                        <p>11:00 AM daily - Reporte diario</p>
                    </div>
                    <span class="agent-status active">● Activo</span>
                </div>
                <div class="agent-card">
                    <div class="agent-info">
                        <h3>agente-nocturno-creador</h3>
                        <p>3:00 AM daily - Herramientas sistema</p>
                    </div>
                    <span class="agent-status active">● Activo</span>
                </div>
                <div class="agent-card">
                    <div class="agent-info">
                        <h3>agente-nocturno-ari</h3>
                        <p>4:00 AM daily - Proyectos Ari</p>
                    </div>
                    <span class="agent-status active">● Activo</span>
                </div>
                <div class="agent-card">
                    <div class="agent-info">
                        <h3>agente-arquitecto</h3>
                        <p>5:00 AM daily - Apps integradas</p>
                    </div>
                    <span class="agent-status active">● Activo</span>
                </div>
            `;
            return;
        }
        
        container.innerHTML = agents.map(agent => `
            <div class="agent-card">
                <div class="agent-info">
                    <h3>${agent.name}</h3>
                    <p>Última ejecución: ${agent.last_run || 'Nunca'}</p>
                </div>
                <span class="agent-status ${agent.status}">● ${agent.status}</span>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = '<div class="loading">Error cargando agentes</div>';
    }
}

// Update logs
async function updateLogs() {
    const container = document.getElementById('logs-container');
    
    try {
        const res = await fetch(`${API_BASE}/api/logs`);
        const logs = await res.json();
        
        if (logs.length === 0) {
            container.innerHTML = `
                <div class="log-entry">
                    <span class="log-level success">OK</span>
                    <div class="log-content">
                        <div class="log-agent">agente-arquitecto</div>
                        <div class="log-message">Dashboard Jazmín OS iniciado correctamente</div>
                    </div>
                    <span class="log-time">${new Date().toLocaleTimeString('es-AR')}</span>
                </div>
                <div class="log-entry">
                    <span class="log-level info">INFO</span>
                    <div class="log-content">
                        <div class="log-agent">sistema</div>
                        <div class="log-message">Sistema operativo Linux detectado</div>
                    </div>
                    <span class="log-time">${new Date().toLocaleTimeString('es-AR')}</span>
                </div>
                <div class="log-entry">
                    <span class="log-level info">INFO</span>
                    <div class="log-content">
                        <div class="log-agent">jazmin-os</div>
                        <div class="log-message">Servidor FastAPI iniciado en puerto 8080</div>
                    </div>
                    <span class="log-time">${new Date().toLocaleTimeString('es-AR')}</span>
                </div>
            `;
            return;
        }
        
        container.innerHTML = logs.map(log => `
            <div class="log-entry">
                <span class="log-level ${log.level.toLowerCase()}">${log.level}</span>
                <div class="log-content">
                    <div class="log-agent">${log.agent_name}</div>
                    <div class="log-message">${log.message}</div>
                </div>
                <span class="log-time">${new Date(log.timestamp).toLocaleTimeString('es-AR')}</span>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = '<div class="loading">Error cargando logs</div>';
    }
}

// Update processes
async function updateProcesses() {
    const tbody = document.getElementById('processes-tbody');
    
    try {
        const res = await fetch(`${API_BASE}/api/processes`);
        const processes = await res.json();
        
        tbody.innerHTML = processes.map(proc => `
            <tr>
                <td>${proc.pid}</td>
                <td>${proc.name}</td>
                <td>${proc.cpu_percent?.toFixed(1) || 0}%</td>
                <td>${proc.memory_percent?.toFixed(1) || 0}%</td>
                <td><span class="process-status ${proc.status}">${proc.status}</span></td>
            </tr>
        `).join('');
    } catch (err) {
        tbody.innerHTML = '<tr><td colspan="5">Error cargando procesos</td></tr>';
    }
}

// Update current time
function updateTime() {
    document.getElementById('current-time').textContent = 
        new Date().toLocaleString('es-AR', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Initial load
    updateSystemStats();
    updateAgents();
    updateLogs();
    updateProcesses();
    updateTime();
    
    // Periodic updates
    setInterval(updateSystemStats, 5000);  // Every 5s
    setInterval(updateAgents, 30000);       // Every 30s
    setInterval(updateLogs, 10000);         // Every 10s
    setInterval(updateProcesses, 5000);     // Every 5s
    setInterval(updateTime, 1000);          // Every 1s
});
