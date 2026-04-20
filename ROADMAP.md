# Roadmap de Desarrollo Post v1.0.0

Documento de planificación para futuras versiones y mejoras del proyecto **Normalizador Audio**.

---

## 📊 Ciclo 2: v1.1.0 - Características Intermedias (Q2-Q3 2026)

### 🎯 Prioridad: ALTA

#### 2.1 Mejoras de Rendimiento
- **GPU Acceleration**: Integración con FFmpeg GPU (NVIDIA NVENC, AMD VCE, Intel QuickSync)
  - Reducir tiempo de procesamiento en 50-70%
  - Detectar capacidad GPU automáticamente
  - Fallback a CPU si no disponible
  - Nueva opción en perfil de audio

- **Caché de análisis inteligente**: 
  - No re-analizar videos con mismo hash MD5
  - Base de datos SQLite local de análisis previos
  - Opción de forzar re-análisis si se necesita

- **Procesamiento paralelo mejorado**:
  - Procesar múltiples videos simultáneamente (multi-threading robusto)
  - Límite configurable de workers concurrentes
  - Barra de progreso global + individual por video

#### 2.2 Características de Interfaz
- **Waveform visual**:
  - Previsualización de onda antes/después del procesamiento
  - Selección visual de segmentos para normalizar (trim points)
  - Espectro LUFS real-time

- **Presets predefinidos**:
  - YouTube (LUFS -14, LRA 7, TP -1.5)
  - Netflix (LUFS -27, TP -2)
  - Spotify (LUFS -14, TP -1)
  - Podcast (LUFS -16, TP -1)
  - Custom: guardar/cargar propios presets

- **Interfaz de arrastrar-soltar mejorada**:
  - Arrastrar archivos directamente a tab de normalizar
  - Mostrar vista previa en tiempo real mientras se arrastra
  - Soporte para carpetas (agregar todos los videos dentro)

#### 2.3 Reportes Avanzados
- **Gráficos interactivos**:
  - Matplotlib/Plotly embebido: comparativa antes/después
  - Histogramas de distribución LUFS
  - Timeline de cambios durante procesamiento

- **Exportación avanzada**:
  - Excel (.xlsx) con gráficos embebidos
  - JSON con metadatos completos
  - PDF con reporte ejecutivo

---

## 📊 Ciclo 3: v1.2.0 - Modo CLI + Automatización (Q3-Q4 2026)

### 🎯 Prioridad: MEDIA-ALTA

#### 3.1 Interfaz de Línea de Comandos
```bash
normalizador-audio normalize --input ./videos --output ./normalized --lufs -14 --lra 7 --preset youtube
normalizador-audio analyze --file video.mp4 --json
normalizador-audio batch --config batch.json --parallel 4
```

- Click/argparse para parsing de argumentos
- Configuración vía JSON/YAML
- Modo watch para carpetas (procesar nuevos videos automáticamente)
- Integración con scripts de terceros

#### 3.2 Daemon/Servicio
- Ejecutable como servicio Windows (pywin32)
- Monitor de carpetas configurable
- Procesamiento en background sin GUI
- API REST simple (http://localhost:9000) para consultar estado

#### 3.3 Webhooks y Notificaciones
- Callback HTTP POST al finalizar procesamiento
- Notificaciones por email (SMTP configurable)
- Integración Slack/Discord para alertas
- Logs enviados a syslog/ELK

---

## 📊 Ciclo 4: v2.0.0 - Audio Directo + Extensibilidad (Q1 2027)

### 🎯 Prioridad: MEDIA

#### 4.1 Soporte de Audio Directo
- Procesar archivos de audio (.mp3, .wav, .aac, .flac)
- No solo extraído de video
- Interfaz simplificada para audio puro

#### 4.2 Sistema de Plugins
- Plugin API estable
- Plugins de terceros para:
  - Procesamiento adicional (de-esser, compressor)
  - Nuevos formatos de entrada
  - Exportadores personalizados

#### 4.3 Historial y Versioning
- Base de datos SQLite: historial de procesamiento
- Revisor de cambios (timeline)
- Rollback de procesamiento (deshacer cambios)

---

## 🔒 Ciclo de Seguridad y Mantenimiento (Contínuo)

### Seguridad
- ✅ Code signing para .exe (certificado EV/OV)
- ✅ Reproducibilidad de builds (Docker)
- ✅ Auditoría de dependencias (OWASP, safety)
- ✅ Fuzz testing en parser de audio/video
- ✅ Soporte de Windows Defender SmartScreen

### Confiabilidad
- ✅ E2E GUI testing con pytest-qt (>80% cobertura)
- ✅ Stress testing con 100+ videos paralelos
- ✅ Memory leak detection (tracemalloc)
- ✅ Benchmarks automáticos vs versiones previas

### Mantenimiento
- ✅ Actualización de dependencias (Dependabot)
- ✅ Security patches (15 días de SLA)
- ✅ LTS branches (bugfixes por 12 meses)

---

## 🌍 Opcionales (Baja Prioridad, Si Demanda)

### 5.1 Plataforma Web (Electron/Tauri)
- Aplicación web basada en React + FastAPI
- Sincronización en la nube de perfiles
- Acceso remoto (no solo Windows)

### 5.2 Soporte Macbook/Linux
- Versiones nativas para macOS y Linux
- Misma lógica, UI nativa por SO

### 5.3 Integración con DAWs
- Plugin VST/AU para integrarse en productoras de audio
- Normalización en tiempo real

### 5.4 Mobile App
- iOS/Android versión simplificada
- Upload de videos, procesamiento en server
- Descarga de resultado

---

## 📋 Tareas Inmediatas Pre-GitHub (Esta Semana)

Para que v1.0.0 esté lista para publicación en GitHub:

- [ ] 1. **Crear .gitignore** (actualizar si existe)
  ```
  __pycache__/
  .pytest_cache/
  *.egg-info/
  build/
  dist/
  *.pyc
  .env
  normalizador_config.ini
  audio_profile.json
  normalizador_errors.log
  .vscode/
  ```

- [ ] 2. **Crear SECURITY.md**
  ```markdown
  # Security Policy
  Reportar vulnerabilidades a: [email seguro]
  No abrir issues públicos de seguridad
  Respuesta en 48 horas
  ```

- [ ] 3. **Crear .github/workflows/release.yml**
  - Build automático del .exe en GitHub Actions
  - Crear release en GitHub con .exe adjunto
  - Changelog automático

- [ ] 4. **Crear versión etiquetada en Git**
  ```bash
  git tag -a v1.0.0 -m "Release version 1.0.0"
  git push origin v1.0.0
  ```

- [ ] 5. **Crear Release en GitHub**
  - Subir NormalizadorAudio.exe a la release
  - Incluir instrucciones de descarga
  - Changelog en descripción

- [ ] 6. **Actualizar badges en README**
  - Downloads count
  - Release version
  - Build status

- [ ] 7. **Crear SUPPORT.md**
  ```markdown
  # Support
  - Issues: GitHub Issues
  - Discussions: GitHub Discussions  
  - Email: [tu email]
  - Donaciones: [enlaces]
  ```

---

## 📈 Métricas de Éxito v1.0.0

Para considerar que v1.0.0 fue exitosa post-lanzamiento:

- [ ] ≥50 stars en GitHub (1 mes)
- [ ] ≥100 descargas de .exe (1 mes)
- [ ] ≥3 issues válidos (feedback usuarios)
- [ ] ≥1 PR de comunidad
- [ ] Test coverage ≥70%
- [ ] 0 bugs críticos encontrados (1 mes)

---

## 🛠️ Stack Recomendado para Futuras Versiones

- **Testing**: pytest, hypothesis, faker
- **Performance**: cProfile, memory_profiler, py-spy
- **CLI**: Click, Rich (para output fancy)
- **Web**: FastAPI, SQLAlchemy, Pydantic
- **Visualization**: Matplotlib, Plotly
- **Desktop**: PyQt6.5+ (cuando disponible)
- **Deployment**: PyInstaller, GitHub Actions, Docker

---

**Documento de planificación actualizado: 2026-04-20**  
**Responsable**: Wilkin Barbán  
**Feedback**: Bienvenido en discussions o issues
