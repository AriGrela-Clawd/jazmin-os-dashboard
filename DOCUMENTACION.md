# Jazmín OS - Dashboard Personal

## Descripción
Dashboard personal de control para el ecosistema Clawdbot/Jazmín. Proporciona una interfaz web centralizada para monitorear agentes, métricas del sistema, proyectos activos, memoria, cron jobs y herramientas disponibles.

## Arquitectura

### Stack Tecnológico
- **Backend**: FastAPI (Python 3.12+)
- **Base de Datos**: SQLite + SQLAlchemy ORM
- **Frontend**: HTML5 + Jinja2 Templates + CSS3 + Vanilla JavaScript
- **WebSockets**: Para actualizaciones en tiempo real
- **Estilo**: Dark mode minimalista con acento rosa Jazmín (#f0abfc)

### Estructura del Proyecto
```
jazmin-os/
├── main.py                 # Punto de entrada FastAPI
├── database.py             # Configuración DB y modelos
├── models.py               # Modelos SQLAlchemy
├── schemas.py              # Pydantic schemas
├── config.py               # Configuración centralizada
├── websocket_manager.py    # Gestor de WebSockets
├── requirements.txt        # Dependencias
├── README.md               # Documentación
├── data/                   # Base de datos SQLite
├── static/                 # Assets estáticos (CSS, JS, imágenes)
│   ├── css/
│   ├── js/
│   └── img/
└── templates/              # Templates Jinja2
    ├── base.html
    ├── dashboard.html
    ├── agents.html
    ├── metrics.html
    ├── memory.html
    ├── logs.html
    ├── projects.html
    └── tools.html
```

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/AriGrela-Clawd/jazmin-os.git
cd jazmin-os

# Crear entorno virtual (opcional pero recomendado)
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos (automático al primer run)
python main.py
```

## Uso

### Iniciar la aplicación
```bash
python main.py
```

La aplicación estará disponible en: `http://localhost:8000`

### Acceso a endpoints principales
- **Dashboard**: `/` - Vista general del sistema
- **Agentes**: `/agents` - Control de agentes nocturnos
- **Métricas**: `/metrics` - CPU, RAM, disco, red en tiempo real
- **Memory**: `/memory` - Feed cronológico de memoria
- **Logs**: `/logs` - Logs del sistema
- **Proyectos**: `/projects` - Gestión de proyectos activos
- **Tools**: `/tools` - Acceso rápido a skills

### API Endpoints (JSON)
- `GET /api/system/metrics` - Métricas del sistema
- `GET /api/agents/status` - Estado de agentes
- `GET /api/memory/entries` - Entradas de memoria
- `GET /api/projects` - Lista de proyectos
- `WebSocket /ws` - Actualizaciones en tiempo real

## Características Principales

### 🤖 Panel de Agentes
- Estado en tiempo real de agentes nocturnos
- Ejecución manual de tareas
- Historial de ejecuciones
- Indicadores de salud

### 📊 Métricas del Sistema
- CPU usage y procesos principales
- RAM y swap usage
- Uso de discos
- Uptime del sistema
- Actualización en tiempo real vía WebSocket

### 📁 Proyectos Activos
- Listado de proyectos del ecosistema
- Estado de cada proyecto
- Accesos directos a repos y documentación

### 📝 Memory Feed
- Visualización cronológica de memoria
- Filtrado por fecha y categoría
- Integración con sistema de memoria de Jazmín

### ⏰ Cron Jobs
- Administración de tareas programadas
- Estado de ejecuciones pasadas
- Próximas ejecuciones

### 🛠️ Herramientas
- Acceso rápido a skills instaladas
- Documentación inline
- Atajos de comandos

## Screenshots/Demo

### Dashboard Principal
Vista general con tarjetas de resumen:
- Estado de agentes (activos/inactivos)
- Métricas clave del sistema
- Proyectos recientes
- Últimas entradas de memoria

**Diseño:**
- Sidebar de navegación izquierda (colapsable)
- Área principal con grid de widgets
- Tema oscuro con acentos en rosa Jazmín
- Tipografía moderna y legible
- Iconografía consistente

### Panel de Agentes
- Lista de agentes con estado (🟢 activo / 🔴 inactivo)
- Botones de ejecución manual
- Logs de última ejecución
- Frecuencia de ejecución configurada

### Métricas en Tiempo Real
- Gráficos animados de CPU y RAM
- Barras de progreso visuales
- Indicadores de alerta (rojo/amarillo/verde)
- Datos de red (IPs, estado de conexión)

## Dependencias Principales

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
pydantic>=2.5.0
jinja2>=3.1.0
python-multipart>=0.0.6
websockets>=12.0
psutil>=5.9.0
aiofiles>=23.2.0
```

## GitHub

**Repositorio:** https://github.com/AriGrela-Clawd/jazmin-os

**Commits principales:**
- `307dfe7` - Initial commit: Jazmín OS Dashboard v1.0.0

## Roadmap Futuro

- [ ] Autenticación de usuarios
- [ ] Integración con más servicios (Notion, Discord)
- [ ] Exportación de métricas a CSV/JSON
- [ ] Soporte para múltiples instancias
- [ ] Tema claro opcional
- [ ] App móvil (PWA)

## Autor

**Agente Arquitecto 🏗️** - Sistema Clawdbot/Jazmín

Creado: 2026-02-06
Versión: 1.0.0

---

*Documentación generada automáticamente por Agente Arquitecto*
