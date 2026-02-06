# Jazmín OS 🌸

Dashboard personal de control para el ecosistema Clawdbot/Jazmín.

![Versión](https://img.shields.io/badge/version-1.0.0-pink)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)

## ✨ Características

- **🤖 Panel de Agentes**: Estado de agentes nocturnos con ejecución manual
- **📊 Métricas del Sistema**: CPU, RAM, disco y uptime en tiempo real
- **📁 Proyectos Activos**: Gestión de proyectos del ecosistema
- **📝 Memory Feed**: Visualización cronológica de memoria
- **⏰ Cron Jobs**: Administración de tareas programadas
- **🛠️ Herramientas**: Acceso rápido a skills instaladas

## 🎨 Diseño

- **Tema**: Dark mode minimalista
- **Acento**: Rosa Jazmín (#f0abfc)
- **Layout**: Sidebar navigation + área principal
- **Responsive**: Optimizado para mobile y desktop

## 🚀 Instalación

### 1. Navegar al proyecto

```bash
cd ~/clawd/proyectos/jazmin-os
```

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python main.py
```

La aplicación estará disponible en: **http://localhost:8000**

## 📁 Estructura del Proyecto

```
jazmin-os/
├── main.py              # Aplicación FastAPI principal
├── database.py          # Modelos y conexión SQLite
├── requirements.txt     # Dependencias de Python
├── README.md           # Este archivo
├── static/
│   ├── css/
│   │   └── style.css   # Estilos con variables CSS
│   ├── js/
│   │   └── app.js      # Lógica frontend
│   └── img/
│       └── favicon.svg # Icono de flor/jazmín
└── templates/
    ├── base.html       # Template base con layout
    ├── dashboard.html  # Vista principal
    ├── agents.html     # Gestión de agentes
    ├── projects.html   # Lista de proyectos
    ├── memory.html     # Visualización de memoria
    ├── metrics.html    # Métricas detalladas
    └── tools.html      # Herramientas disponibles
```

## 🔌 API Endpoints

### Dashboard
- `GET /` - Dashboard principal
- `GET /ws` - WebSocket para métricas en tiempo real

### API REST
- `GET /api/metrics` - Métricas del sistema
- `GET /api/agents` - Estado de agentes
- `POST /api/agents/{agent_id}/run` - Ejecutar agente manualmente
- `GET /api/projects` - Lista de proyectos
- `GET /api/memory` - Entradas de memoria
- `GET /api/cron` - Jobs de cron
- `GET /api/tools` - Skills instaladas

## 🖼️ Screenshots

### Dashboard Principal
Vista general con métricas en tiempo real, estado de agentes y proyectos recientes.

### Panel de Agentes
Control completo de agentes nocturnos con historial de ejecuciones.

### Métricas del Sistema
Gráficos de CPU, memoria y uso de disco con actualización en tiempo real.

### Memory Feed
Timeline cronológico de todas las entradas de memoria.

## ⚙️ Configuración

La base de datos SQLite se crea automáticamente en:
```
~/clawd/proyectos/jazmin-os/data/jazmin_os.db
```

### Variables de entorno (opcionales)

```bash
export JAZMIN_OS_PORT=8000        # Puerto (default: 8000)
export JAZMIN_OS_HOST=0.0.0.0     # Host (default: 0.0.0.0)
```

## 🔄 Actualización de Datos

- **Métricas**: WebSocket con actualización cada 5 segundos
- **Agentes**: Polling cada 30 segundos
- **Proyectos**: Escaneo en tiempo real
- **Memory**: Actualización bajo demanda

## 🛠️ Desarrollo

```bash
uvicorn main:app --reload --port 8000
```

---

💜 Creado con amor por Jazmín para Ari
