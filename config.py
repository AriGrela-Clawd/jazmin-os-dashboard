"""
Jazmín OS - Configuration
==========================
Configuración centralizada de la aplicación.
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/jazmin_os.db")

# App settings
APP_NAME = "Jazmín OS"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Dashboard Personal - Centro de Comando para Agentes"

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# CORS settings
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

# WebSocket settings
WS_HEARTBEAT_INTERVAL = 30  # seconds
AGENT_TIMEOUT = 300  # seconds (5 minutes)

# Agent types
AGENT_TYPES = [
    "scheduler",      # Agente programado (cron)
    "reactive",       # Agente reactivo (eventos)
    "background",     # Agente de fondo
    "interactive",    # Agente interactivo
]

# Status constants
class Status:
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class TaskStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ProjectStatus:
    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class LogLevel:
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

# Priority levels
class Priority:
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
