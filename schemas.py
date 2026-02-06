"""
Jazmín OS - Pydantic Schemas
=============================
Schemas para validación y serialización de datos.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ============== AGENT SCHEMAS ==============

class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    display_name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    agent_type: str = "background"
    config: Dict[str, Any] = Field(default_factory=dict)


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    agent_type: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class AgentResponse(AgentBase):
    id: int
    status: str
    last_seen: datetime
    created_at: datetime
    updated_at: datetime
    is_online: bool = False

    class Config:
        from_attributes = True


class AgentHeartbeat(BaseModel):
    status: str = "online"
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ============== PROJECT SCHEMAS ==============

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: str = "planning"
    priority: int = Field(default=2, ge=1, le=4)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=4)
    progress: Optional[float] = Field(None, ge=0, le=100)


class ProjectResponse(ProjectBase):
    id: int
    progress: float
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    task_count: int = 0
    completed_tasks: int = 0

    class Config:
        from_attributes = True


# ============== TASK SCHEMAS ==============

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    description: Optional[str] = None
    status: str = "pending"
    priority: int = Field(default=2, ge=1, le=4)


class TaskCreate(TaskBase):
    project_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=4)


class TaskResponse(TaskBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============== METRIC SCHEMAS ==============

class MetricBase(BaseModel):
    metric_type: str = Field(..., min_length=1, max_length=50)
    value: float
    unit: Optional[str] = Field(None, max_length=20)
    metadata_json: Dict[str, Any] = Field(default_factory=dict)


class MetricCreate(MetricBase):
    agent_id: Optional[int] = None


class MetricResponse(MetricBase):
    id: int
    agent_id: Optional[int] = None
    timestamp: datetime
    agent_name: Optional[str] = None

    class Config:
        from_attributes = True


class SystemMetrics(BaseModel):
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_total_mb: float
    disk_percent: float
    disk_used_gb: float
    disk_total_gb: float
    timestamp: datetime


# ============== LOG SCHEMAS ==============

class LogBase(BaseModel):
    level: str = "info"
    source: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1)
    metadata_json: Dict[str, Any] = Field(default_factory=dict)


class LogCreate(LogBase):
    pass


class LogResponse(LogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# ============== CRON JOB SCHEMAS ==============

class CronJobBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    schedule: str = Field(..., min_length=1, max_length=100)  # Cron expression
    command: Optional[str] = None
    status: str = "active"


class CronJobCreate(CronJobBase):
    pass


class CronJobUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    schedule: Optional[str] = None
    command: Optional[str] = None
    status: Optional[str] = None
    next_run: Optional[datetime] = None


class CronJobResponse(CronJobBase):
    id: int
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int
    success_count: int
    fail_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== DASHBOARD SCHEMAS ==============

class DashboardStats(BaseModel):
    total_agents: int
    online_agents: int
    offline_agents: int
    total_projects: int
    active_projects: int
    completed_projects: int
    total_tasks: int
    pending_tasks: int
    completed_tasks: int
    total_cron_jobs: int
    active_cron_jobs: int


class RecentActivity(BaseModel):
    logs: List[LogResponse]
    metrics: List[MetricResponse]


class AgentStatusSummary(BaseModel):
    id: int
    name: str
    display_name: Optional[str]
    status: str
    is_online: bool
    last_seen: datetime
    agent_type: str


class ProjectSummary(BaseModel):
    id: int
    name: str
    status: str
    progress: float
    priority: int
    task_count: int
    completed_tasks: int


class DashboardData(BaseModel):
    stats: DashboardStats
    agents: List[AgentStatusSummary]
    projects: List[ProjectSummary]
    recent_logs: List[LogResponse]
    system_metrics: Optional[SystemMetrics] = None
    cron_jobs: List[CronJobResponse]
