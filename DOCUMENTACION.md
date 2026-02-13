# Jazmín OS

## Descripción
Dashboard personal para monitorear agentes, métricas del sistema y logs en tiempo real. Una interfaz web elegante construida con FastAPI que muestra el estado completo del sistema y los agentes automáticos.

## Arquitectura
- **Backend:** FastAPI (Python) + Uvicorn
- **Base de datos:** SQLite
- **Frontend:** HTML5 + CSS3 + JavaScript vanilla
- **Monitoreo:** psutil para métricas del sistema
- **UI:** Tema oscuro moderno con gradientes y diseño responsive

## Estructura
```
jazmin-os/
├── main.py              # FastAPI app + API endpoints
├── requirements.txt     # Dependencias Python
├── jazmin_os.db        # Base de datos SQLite
├── README.md           # Documentación
├── templates/
│   └── index.html      # Dashboard UI
└── static/
    ├── css/
    │   └── style.css   # Estilos dark theme
    └── js/
        └── app.js      # Frontend logic + actualizaciones
```

## Instalación
```bash
git clone https://github.com/AriGrela-Clawd/jazmin-os-dashboard.git
cd jazmin-os-dashboard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Uso
1. Iniciar: `python main.py`
2. Abrir navegador en `http://localhost:8080`
3. El dashboard se actualiza automáticamente cada 5 segundos

### Secciones del Dashboard:
- 📊 **Métricas del Sistema:** CPU, memoria, disco, uptime
- 🤖 **Estado de Agentes:** Lista de agentes cron activos
- 📝 **Logs Recientes:** Logs centralizados de todos los agentes
- ⚡ **Procesos Activos:** Top 20 procesos por uso de CPU

## API Endpoints
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Dashboard web |
| `/api/system` | GET | Métricas del sistema (CPU, memoria, disco) |
| `/api/agents` | GET | Lista de agentes |
| `/api/agents` | POST | Crear nuevo agente |
| `/api/logs` | GET | Logs recientes |
| `/api/logs` | POST | Agregar log |
| `/api/processes` | GET | Procesos activos |
| `/api/health` | GET | Health check |

## Screenshots/Demo
- Interfaz dark theme con gradientes índigo/rosa
- Cards con métricas en tiempo real
- Barras de progreso animadas para CPU/memoria/disco
- Lista de agentes con indicadores de estado
- Logs con color coding (info/warning/error/success)
- Tabla de procesos ordenada por uso de CPU

## GitHub
https://github.com/AriGrela-Clawd/jazmin-os-dashboard

## Notas
- Puerto por defecto: 8080
- Actualización automática cada 5 segundos (métricas)
- Base de datos SQLite autocreada al iniciar
- Compatible con Linux/macOS/Windows
