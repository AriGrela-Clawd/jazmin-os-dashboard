"""
Jazmín OS - Database Models
============================
Modelos SQLAlchemy para todas las entidades.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship

from database import Base


class Agent(Base):
    """Modelo para agentes del sistema."""
    
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="offline")
    agent_type = Column(String(50), default="background")
    last_seen = Column(DateTime, default=datetime.utcnow)
    config = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    metrics = relationship("Metric", back_populates="agent", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Agent {self.name}>"
    
    def is_online(self, timeout_seconds: int = 300) -> bool:
        """Verifica si el agente está online basado en last_seen."""
        if not self.last_seen:
            return False
        delta = datetime.utcnow() - self.last_seen
        return delta.total_seconds() < timeout_seconds


class Project(Base):
    """Modelo para proyectos."""
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="planning")
    progress = Column(Float, default=0.0)  # 0.0 - 100.0
    priority = Column(Integer, default=2)  # 1-4
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relaciones
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project {self.name}>"
    
    def update_progress(self):
        """Calcula el progreso basado en tareas completadas."""
        if not self.tasks:
            self.progress = 0.0
            return
        
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.status == "completed")
        self.progress = round((completed / total) * 100, 2)


class Task(Base):
    """Modelo para tareas dentro de proyectos."""
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending")
    priority = Column(Integer, default=2)  # 1-4
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relaciones
    project = relationship("Project", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task {self.title}>"


class Metric(Base):
    """Modelo para métricas de agentes y sistema."""
    
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    metric_type = Column(String(50), nullable=False)  # cpu, memory, disk, custom
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=True)  # %, MB, GB, etc.
    metadata_json = Column(JSON, default=dict)  # Datos adicionales
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    agent = relationship("Agent", back_populates="metrics")
    
    def __repr__(self):
        return f"<Metric {self.metric_type}={self.value}>"


class Log(Base):
    """Modelo para logs del sistema."""
    
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), default="info")  # debug, info, warning, error, critical
    source = Column(String(100), nullable=False)  # nombre del agente o sistema
    message = Column(Text, nullable=False)
    metadata_json = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<Log [{self.level}] {self.source}>"


class CronJob(Base):
    """Modelo para jobs programados (cron jobs)."""
    
    __tablename__ = "cron_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    schedule = Column(String(100), nullable=False)  # Expresión cron
    command = Column(String(500), nullable=True)  # Comando a ejecutar
    status = Column(String(20), default="active")  # active, paused, disabled
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    run_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<CronJob {self.name}>"
