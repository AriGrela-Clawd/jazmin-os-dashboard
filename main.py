from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import sqlite3
import psutil
import os
import json
from typing import List, Optional

app = FastAPI(title="Jazmín OS", description="Dashboard Personal de Agentes")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database
DB_PATH = "jazmin_os.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        status TEXT DEFAULT 'inactive',
        last_run TEXT,
        next_run TEXT,
        success_count INTEGER DEFAULT 0,
        fail_count INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        agent_name TEXT,
        level TEXT,
        message TEXT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY,
        metric_type TEXT,
        value REAL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup():
    init_db()

# Models
class Agent(BaseModel):
    id: Optional[int] = None
    name: str
    status: str = "inactive"
    last_run: Optional[str] = None
    next_run: Optional[str] = None
    success_count: int = 0
    fail_count: int = 0

class LogEntry(BaseModel):
    id: Optional[int] = None
    agent_name: str
    level: str
    message: str
    timestamp: Optional[str] = None

# Routes
@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/system")
async def system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "cpu": {
            "percent": cpu_percent,
            "cores": psutil.cpu_count(),
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
        },
        "memory": {
            "total": memory.total // (1024**3),
            "available": memory.available // (1024**3),
            "percent": memory.percent,
            "used": memory.used // (1024**3)
        },
        "disk": {
            "total": disk.total // (1024**3),
            "used": disk.used // (1024**3),
            "free": disk.free // (1024**3),
            "percent": (disk.used / disk.total) * 100
        },
        "boot_time": boot_time,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/api/agents")
async def get_agents():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM agents ORDER BY created_at DESC")
    agents = [dict(row) for row in c.fetchall()]
    conn.close()
    return agents

@app.post("/api/agents")
async def create_agent(agent: Agent):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO agents (name, status, last_run, next_run) 
                 VALUES (?, ?, ?, ?)''',
              (agent.name, agent.status, agent.last_run, agent.next_run))
    conn.commit()
    agent_id = c.lastrowid
    conn.close()
    return {"id": agent_id, **agent.dict()}

@app.get("/api/logs")
async def get_logs(limit: int = 50):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    logs = [dict(row) for row in c.fetchall()]
    conn.close()
    return logs

@app.post("/api/logs")
async def add_log(log: LogEntry):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO logs (agent_name, level, message, timestamp) 
                 VALUES (?, ?, ?, ?)''',
              (log.agent_name, log.level, log.message, 
               log.timestamp or datetime.now().isoformat()))
    conn.commit()
    log_id = c.lastrowid
    conn.close()
    return {"id": log_id, **log.dict()}

@app.get("/api/processes")
async def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:20]

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
