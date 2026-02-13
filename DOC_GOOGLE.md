# 🌸 Jazmín OS - Dashboard Personal

**Fecha:** 2026-02-13  
**Agente:** Agente Arquitecto  
**Repositorio:** https://github.com/AriGrela-Clawd/jazmin-os-dashboard

---

## 🎯 Descripción

Dashboard personal para monitorear agentes, métricas del sistema y logs en tiempo real. Una interfaz web elegante construida con FastAPI que muestra el estado completo del sistema y los agentes automáticos.

---

## 🏗️ Arquitectura

| Componente | Tecnología |
|------------|------------|
| **Backend** | FastAPI (Python) + Uvicorn |
| **Base de datos** | SQLite |
| **Frontend** | HTML5 + CSS3 + JavaScript vanilla |
| **Monitoreo** | psutil para métricas del sistema |
| **UI** | Tema oscuro moderno con gradientes |

---

## 📁 Estructura

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

---

## 🚀 Instalación

```bash
# Clonar
git clone https://github.com/AriGrela-Clawd/jazmin-os-dashboard.git
cd jazmin-os-dashboard

# Entorno virtual
python -m venv venv
source venv/bin/activate

# Dependencias
pip install -r requirements.txt

# Iniciar
python main.py
```

---

## 🌐 Uso

1. Iniciar: `python main.py`
2. Abrir navegador en `http://localhost:8080`
3. El dashboard se actualiza automáticamente cada 5 segundos

### Secciones del Dashboard:

| Sección | Descripción |
|---------|-------------|
| 📊 **Métricas del Sistema** | CPU, memoria, disco, uptime en tiempo real |
| 🤖 **Estado de Agentes** | Lista de agentes cron activos con estado |
| 📝 **Logs Recientes** | Logs centralizados de todos los agentes |
| ⚡ **Procesos Activos** | Top 20 procesos ordenados por uso de CPU |

---

## 🔌 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Dashboard web |
| `/api/system` | GET | Métricas del sistema |
| `/api/agents` | GET | Lista de agentes |
| `/api/agents` | POST | Crear nuevo agente |
| `/api/logs` | GET | Logs recientes |
| `/api/logs` | POST | Agregar log |
| `/api/processes` | GET | Procesos activos |
| `/api/health` | GET | Health check |

---

## 🎨 Screenshots / Demo

- **Interfaz:** Dark theme con gradientes índigo/rosa
- **Métricas:** Cards con datos en tiempo real
- **Progreso:** Barras animadas para CPU/memoria/disco
- **Agentes:** Lista con indicadores de estado (activo/inactivo/error)
- **Logs:** Color coding (info/warning/error/success)
- **Procesos:** Tabla ordenada por uso de CPU

---

## 📝 Notas

- **Puerto:** 8080 (configurable)
- **Actualización:** Automática cada 5 segundos
- **Database:** SQLite autocreada al iniciar
- **Compatibilidad:** Linux / macOS / Windows

---

**— Agente Arquitecto 🏗️**  
*2026-02-13 05:00 AM*
