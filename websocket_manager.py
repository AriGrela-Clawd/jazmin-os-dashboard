"""
Jazmín OS - WebSocket Manager
==============================
Gestión de conexiones WebSocket para actualizaciones en tiempo real.
"""

from typing import List, Dict, Any
from fastapi import WebSocket
import json
import asyncio
from datetime import datetime


class ConnectionManager:
    """Gestiona conexiones WebSocket del dashboard."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.agent_subscribers: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket):
        """Acepta una nueva conexión WebSocket."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"[WS] Nueva conexión. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Desconecta un WebSocket."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"[WS] Conexión cerrada. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Envía un mensaje a un cliente específico."""
        await websocket.send_json(message)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast a todos los clientes conectados."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"[WS] Error enviando mensaje: {e}")
                disconnected.append(connection)
        
        # Limpiar conexiones rotas
        for conn in disconnected:
            self.disconnect(conn)
    
    def broadcast_agent_update(self, data: Dict[str, Any]):
        """Envía actualización de agente (versión sync que programa async)."""
        message = {
            "type": "agent_update",
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }
        # Programar broadcast async
        asyncio.create_task(self.broadcast(message))
    
    def broadcast_system_metrics(self, data: Dict[str, Any]):
        """Envía actualización de métricas del sistema."""
        message = {
            "type": "system_metrics",
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }
        asyncio.create_task(self.broadcast(message))
    
    def broadcast_new_log(self, log_data: Dict[str, Any]):
        """Envía notificación de nuevo log."""
        message = {
            "type": "new_log",
            "timestamp": datetime.utcnow().isoformat(),
            "data": log_data,
        }
        asyncio.create_task(self.broadcast(message))
    
    def broadcast_task_update(self, task_data: Dict[str, Any]):
        """Envía actualización de tarea."""
        message = {
            "type": "task_update",
            "timestamp": datetime.utcnow().isoformat(),
            "data": task_data,
        }
        asyncio.create_task(self.broadcast(message))


# Instancia global del manager
manager = ConnectionManager()
