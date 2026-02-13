# 🌸 Jazmín OS

Dashboard personal para monitorear agentes, métricas del sistema y logs en tiempo real.

![Jazmín OS](https://img.shields.io/badge/Jazmín%20OS-v1.0-6366f1?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=flat-square)

## ✨ Características

- 📊 **Métricas en tiempo real** - CPU, memoria, disco y uptime
- 🤖 **Estado de agentes** - Monitorea tus agentes automáticos
- 📝 **Logs centralizados** - Visualiza logs de todos los agentes
- ⚡ **Procesos activos** - Top 20 procesos por uso de CPU
- 🎨 **UI moderna** - Tema oscuro con diseño responsive

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/AriGrela/jazmin-os.git
cd jazmin-os

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Iniciar el servidor
python main.py
```

## 🌐 Acceso

Una vez iniciado, abre tu navegador en:
```
http://localhost:8080
```

## 📡 API Endpoints

| Endpoint | Descripción |
|----------|-------------|
| `GET /` | Dashboard web |
| `GET /api/system` | Métricas del sistema |
| `GET /api/agents` | Lista de agentes |
| `POST /api/agents` | Crear agente |
| `GET /api/logs` | Logs recientes |
| `POST /api/logs` | Agregar log |
| `GET /api/processes` | Procesos activos |
| `GET /api/health` | Health check |

## 🏗️ Arquitectura

```
jazmin-os/
├── main.py              # FastAPI app
├── requirements.txt     # Dependencias
├── jazmin_os.db        # SQLite database
├── templates/
│   └── index.html      # Dashboard UI
└── static/
    ├── css/
    │   └── style.css   # Estilos
    └── js/
        └── app.js      # Frontend logic
```

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI + Uvicorn
- **Base de datos**: SQLite
- **Frontend**: HTML5 + CSS3 + Vanilla JS
- **Monitoreo**: psutil (Python)
- **UI**: Diseño dark theme con gradientes

## 📝 Uso

### Agregar un agente
```bash
curl -X POST http://localhost:8080/api/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "mi-agente", "status": "active"}'
```

### Agregar un log
```bash
curl -X POST http://localhost:8080/api/logs \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "mi-agente", "level": "info", "message": "Todo OK"}'
```

## 🎯 Roadmap

- [ ] Autenticación con JWT
- [ ] WebSockets para updates en tiempo real
- [ ] Gráficos históricos de métricas
- [ ] Configuración de alertas
- [ ] Integración con Telegram
- [ ] Modo claro/oscuro

## 👤 Autor

**Ari Grela** - [@AriGrela](https://twitter.com/AriGrela)

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

---

<p align="center">🌸 Hecho con amor por Jazmín</p>
