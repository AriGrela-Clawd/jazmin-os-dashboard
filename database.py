import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Base directory
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "jazmin_os.db"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

def get_db_connection() -> sqlite3.Connection:
    """Get a database connection with row factory."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with all tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Agent runs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT NOT NULL,
            agent_type TEXT DEFAULT 'nocturnal',
            status TEXT DEFAULT 'pending',
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            output TEXT,
            error_message TEXT,
            execution_time_ms INTEGER
        )
    ''')
    
    # System metrics history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpu_percent REAL,
            memory_percent REAL,
            memory_used_gb REAL,
            memory_total_gb REAL,
            disk_percent REAL,
            disk_used_gb REAL,
            disk_total_gb REAL,
            uptime_seconds INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Agent configuration
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            display_name TEXT,
            description TEXT,
            schedule TEXT,
            enabled BOOLEAN DEFAULT 1,
            last_run TIMESTAMP,
            last_status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default agents if not exist
    default_agents = [
        ('agente-nocturno-creador', 'Agente Creador (3AM)', 'Crea herramientas para el sistema', '0 3 * * *', True),
        ('agente-nocturno-ari', 'Agente Ari (4AM)', 'Proyectos personales de Ari', '0 4 * * *', True),
        ('agente-matutino', 'Agente Matutino (11AM)', 'Reporte diario completo', '0 11 * * *', True),
    ]
    
    for agent in default_agents:
        cursor.execute('''
            INSERT OR IGNORE INTO agent_config (name, display_name, description, schedule, enabled)
            VALUES (?, ?, ?, ?, ?)
        ''', agent)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

# Agent operations
def get_agent_runs(limit: int = 50) -> List[Dict[str, Any]]:
    """Get recent agent runs."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM agent_runs 
        ORDER BY started_at DESC 
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_agents_config() -> List[Dict[str, Any]]:
    """Get all agent configurations."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM agent_config ORDER BY name')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_agent_run(agent_name: str, status: str = 'pending', output: str = None) -> int:
    """Add a new agent run record."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO agent_runs (agent_name, status, output)
        VALUES (?, ?, ?)
    ''', (agent_name, status, output))
    run_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return run_id

def update_agent_run(run_id: int, status: str, output: str = None, error_message: str = None):
    """Update agent run status."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT started_at FROM agent_runs WHERE id = ?', (run_id,))
    row = cursor.fetchone()
    
    if row:
        started = datetime.fromisoformat(row['started_at'])
        now = datetime.now()
        execution_time = int((now - started).total_seconds() * 1000)
        
        cursor.execute('''
            UPDATE agent_runs 
            SET status = ?, output = ?, error_message = ?, 
                completed_at = ?, execution_time_ms = ?
            WHERE id = ?
        ''', (status, output, error_message, now, execution_time, run_id))
        
        conn.commit()
    
    conn.close()

# System metrics
def save_system_metrics(cpu: float, memory: float, memory_used: float, memory_total: float,
                        disk: float, disk_used: float, disk_total: float, uptime: int):
    """Save system metrics to database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO system_metrics 
        (cpu_percent, memory_percent, memory_used_gb, memory_total_gb,
         disk_percent, disk_used_gb, disk_total_gb, uptime_seconds)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (cpu, memory, memory_used, memory_total, disk, disk_used, disk_total, uptime))
    conn.commit()
    conn.close()

# Initialize on import
init_db()
