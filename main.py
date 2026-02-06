#!/usr/bin/env python3
"""
Jazmín OS - Dashboard Personal
FastAPI Application
"""

import os
import psutil
import asyncio
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database as db

# Configuration
PORT = int(os.getenv('JAZMIN_OS_PORT', 8000))
HOST = os.getenv('JAZMIN_OS_HOST', '0.0.0.0')

# Base directories
BASE_DIR = Path(__file__).parent
CLAWD_DIR = Path.home() / 'clawd'
PROJECTS_DIR = CLAWD_DIR / 'proyectos'
MEMORY_DIR = CLAWD_DIR / 'memory'
SKILLS_DIR = CLAWD_DIR / 'skills'

# Initialize FastAPI app
app = FastAPI(title="Jazmín OS", description="Dashboard personal para Clawdbot", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                disconnected.append(connection)
        
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

# ============== System Metrics ==============

def get_system_metrics() -> Dict[str, Any]:
    """Get current system metrics."""
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    
    memory = psutil.virtual_memory()
    memory_used_gb = memory.used / (1024**3)
    memory_total_gb = memory.total / (1024**3)
    
    disk = psutil.disk_usage('/')
    disk_used_gb = disk.used / (1024**3)
    disk_total_gb = disk.total / (1024**3)
    
    boot_time = psutil.boot_time()
    uptime_seconds = int(datetime.now().timestamp() - boot_time)
    
    return {
        "cpu": {
            "percent": round(cpu_percent, 1),
            "cores": cpu_count,
            "freq_mhz": round(cpu_freq.current, 0) if cpu_freq else 0
        },
        "memory": {
            "percent": memory.percent,
            "used_gb": round(memory_used_gb, 2),
            "total_gb": round(memory_total_gb, 2),
            "available_gb": round(memory.available / (1024**3), 2)
        },
        "disk": {
            "percent": disk.percent,
            "used_gb": round(disk_used_gb, 2),
            "total_gb": round(disk_total_gb, 2),
            "free_gb": round(disk.free / (1024**3), 2)
        },
        "uptime": {
            "seconds": uptime_seconds,
            "formatted": format_uptime(uptime_seconds)
        },
        "timestamp": datetime.now().isoformat()
    }

def format_uptime(seconds: int) -> str:
    """Format uptime seconds to human readable."""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    
    return " ".join(parts)

# ============== Agents ==============

def get_agents_status() -> List[Dict[str, Any]]:
    """Get status of all agents."""
    agents = db.get_agents_config()
    runs = db.get_agent_runs(limit=100)
    
    runs_by_agent: Dict[str, List[Dict]] = {}
    for run in runs:
        name = run['agent_name']
        if name not in runs_by_agent:
            runs_by_agent[name] = []
        runs_by_agent[name].append(run)
    
    result = []
    for agent in agents:
        agent_runs = runs_by_agent.get(agent['name'], [])
        last_run = agent_runs[0] if agent_runs else None
        
        successes = sum(1 for r in agent_runs if r['status'] == 'success')
        failures = sum(1 for r in agent_runs if r['status'] == 'error')
        
        result.append({
            "id": agent['name'],
            "name": agent['display_name'],
            "description": agent['description'],
            "schedule": agent['schedule'],
            "enabled": bool(agent['enabled']),
            "last_run": last_run['started_at'] if last_run else None,
            "last_status": last_run['status'] if last_run else None,
            "total_runs": len(agent_runs),
            "successes": successes,
            "failures": failures
        })
    
    return result

async def run_agent_manual(agent_id: str) -> Dict[str, Any]:
    """Manually trigger an agent run."""
    run_id = db.add_agent_run(agent_id, 'running')
    
    try:
        agent_commands = {
            'agente-nocturno-creador': 'clawdbot cron run agente-nocturno-creador',
            'agente-nocturno-ari': 'clawdbot cron run agente-nocturno-ari',
            'agente-matutino': 'clawdbot cron run agente-matutino-11am',
        }
        
        command = agent_commands.get(agent_id)
        if not command:
            raise ValueError(f"Unknown agent: {agent_id}")
        
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await proc.communicate()
        output = stdout.decode().strip()
        error = stderr.decode().strip()
        
        if proc.returncode == 0:
            db.update_agent_run(run_id, 'success', output)
            return {"status": "success", "output": output}
        else:
            db.update_agent_run(run_id, 'error', output, error)
            return {"status": "error", "error": error}
    
    except Exception as e:
        db.update_agent_run(run_id, 'error', error_message=str(e))
        return {"status": "error", "error": str(e)}

# ============== Projects ==============

def get_projects() -> List[Dict[str, Any]]:
    """Get list of projects from ~/clawd/proyectos/."""
    projects = []
    
    if not PROJECTS_DIR.exists():
        return projects
    
    for item in sorted(PROJECTS_DIR.iterdir()):
        if item.is_dir():
            has_git = (item / '.git').exists()
            has_readme = (item / 'README.md').exists() or (item / 'readme.md').exists()
            has_requirements = (item / 'requirements.txt').exists()
            has_package_json = (item / 'package.json').exists()
            
            try:
                mtime = item.stat().st_mtime
                last_modified = datetime.fromtimestamp(mtime).isoformat()
            except:
                last_modified = None
            
            try:
                file_count = sum(1 for _ in item.rglob('*') if _.is_file())
            except:
                file_count = 0
            
            projects.append({
                "name": item.name,
                "path": str(item),
                "has_git": has_git,
                "has_readme": has_readme,
                "has_requirements": has_requirements,
                "has_package_json": has_package_json,
                "file_count": file_count,
                "last_modified": last_modified
            })
    
    return projects

# ============== Memory ==============

def get_memory_entries(limit: int = 50) -> List[Dict[str, Any]]:
    """Get memory entries from ~/clawd/memory/."""
    entries = []
    
    if not MEMORY_DIR.exists():
        return entries
    
    memory_files = sorted(MEMORY_DIR.glob('*.md'), reverse=True)
    
    for file_path in memory_files[:limit]:
        try:
            content = file_path.read_text(encoding='utf-8')
            date_str = file_path.stem
            
            try:
                entry_date = datetime.strptime(date_str, '%Y-%m-%d')
                formatted_date = entry_date.strftime('%d %b %Y')
            except:
                formatted_date = date_str
            
            stat = file_path.stat()
            size_kb = stat.st_size / 1024
            
            entries.append({
                "filename": file_path.name,
                "date": date_str,
                "formatted_date": formatted_date,
                "content": content,
                "size_kb": round(size_kb, 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return entries

# ============== Cron Jobs ==============

def get_cron_jobs() -> List[Dict[str, Any]]:
    """Get cron jobs from clawdbot."""
    jobs = []
    
    try:
        result = subprocess.run(
            ['clawdbot', 'cron', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines[2:]:  # Skip header lines
                if line.strip() and not line.startswith('─') and '|' in line:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 2:
                        jobs.append({
                            "name": parts[0],
                            "schedule": parts[1],
                            "status": "active"
                        })
    except Exception as e:
        print(f"Error getting cron jobs: {e}")
    
    return jobs

# ============== Tools ==============

def get_tools() -> List[Dict[str, Any]]:
    """Get installed skills/tools."""
    tools = []
    
    if not SKILLS_DIR.exists():
        return tools
    
    for item in sorted(SKILLS_DIR.iterdir()):
        if item.is_dir():
            has_python = list(item.glob('*.py'))
            has_sh = list(item.glob('*.sh'))
            readme_file = item / 'README.md'
            
            description = ""
            if readme_file.exists():
                try:
                    readme_content = readme_file.read_text()
                    lines = readme_content.split('\n')
                    for line in lines[1:]:
                        if line.strip():
                            description = line.strip()
                            break
                except:
                    pass
            
            tools.append({
                "name": item.name,
                "description": description,
                "has_python": len(has_python) > 0,
                "has_shell": len(has_sh) > 0,
                "path": str(item)
            })
    
    return tools

# ============== Background Tasks ==============

async def metrics_broadcast_loop():
    """Broadcast metrics every 5 seconds."""
    while True:
        try:
            metrics = get_system_metrics()
            await manager.broadcast({
                "type": "metrics",
                "data": metrics
            })
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error in metrics loop: {e}")
            await asyncio.sleep(5)

# ============== Routes ==============

@app.on_event("startup")
async def startup_event():
    """Start background tasks."""
    asyncio.create_task(metrics_broadcast_loop())

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page."""
    metrics = get_system_metrics()
    agents = get_agents_status()
    projects = get_projects()[:6]
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "metrics": metrics,
        "agents": agents,
        "projects": projects,
        "page_title": "Dashboard"
    })

@app.get("/agents", response_class=HTMLResponse)
async def agents_page(request: Request):
    """Agents management page."""
    agents = get_agents_status()
    runs = db.get_agent_runs(limit=20)
    
    return templates.TemplateResponse("agents.html", {
        "request": request,
        "agents": agents,
        "runs": runs,
        "page_title": "Agentes"
    })

@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    """Projects page."""
    projects = get_projects()
    
    return templates.TemplateResponse("projects.html", {
        "request": request,
        "projects": projects,
        "page_title": "Proyectos"
    })

@app.get("/memory", response_class=HTMLResponse)
async def memory_page(request: Request):
    """Memory feed page."""
    entries = get_memory_entries()
    
    return templates.TemplateResponse("memory.html", {
        "request": request,
        "entries": entries,
        "page_title": "Memory Feed"
    })

@app.get("/metrics", response_class=HTMLResponse)
async def metrics_page(request: Request):
    """Detailed metrics page."""
    return templates.TemplateResponse("metrics.html", {
        "request": request,
        "page_title": "Métricas"
    })

@app.get("/tools", response_class=HTMLResponse)
async def tools_page(request: Request):
    """Tools/skills page."""
    tools = get_tools()
    
    return templates.TemplateResponse("tools.html", {
        "request": request,
        "tools": tools,
        "page_title": "Herramientas"
    })

# ============== API Endpoints ==============

@app.get("/api/metrics")
async def api_metrics():
    """Get current system metrics."""
    return get_system_metrics()

@app.get("/api/agents")
async def api_agents():
    """Get agents status."""
    return get_agents_status()

@app.post("/api/agents/{agent_id}/run")
async def api_run_agent(agent_id: str):
    """Manually run an agent."""
    result = await run_agent_manual(agent_id)
    return result

@app.get("/api/projects")
async def api_projects():
    """Get projects list."""
    return get_projects()

@app.get("/api/memory")
async def api_memory(limit: int = 50):
    """Get memory entries."""
    return get_memory_entries(limit)

@app.get("/api/cron")
async def api_cron():
    """Get cron jobs."""
    return get_cron_jobs()

@app.get("/api/tools")
async def api_tools():
    """Get tools/skills."""
    return get_tools()

# ============== WebSocket ==============

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    await websocket.send_json({
        "type": "metrics",
        "data": get_system_metrics()
    })
    
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ============== Main ==============

if __name__ == "__main__":
    import uvicorn
    print(f"🌸 Jazmín OS starting on http://{HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)
