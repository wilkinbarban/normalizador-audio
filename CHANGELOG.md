# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.0.0] - 2026-04-20

### ✨ Características Principales

#### Core Features
- **Normalización LUFS profesional**: Procesamiento de audio basado en FFmpeg loudnorm
- **Procesamiento por lotes**: Normalizar múltiples videos simultáneamente
- **Perfil de referencia**: Analizar un video como referencia y aplicar sus parámetros al lote
- **Reportes detallados**: Antes/después (I, LRA, TP) por video con estadísticas globales
- **Exportación de reportes**: CSV y TXT para análisis posterior

#### Interfaz de Usuario
- **Multilenguaje completo**: Español, English, Português (Brasil)
- **Tema dinámico**: Claro/Oscuro con transiciones suaves
- **Interfaz moderna**: Diseño responsivo basado en PyQt6
- **Diálogos contextuales**: Mensajes informativos, de error y confirmación multilenguaje
- **Indicadores de estado**: Progreso en tiempo real durante procesamiento

#### Sistema de Ayuda y Soporte
- **Manual integrado**: Guía completa de uso directamente en la app
- **Diálogo de apoyo al proyecto**: Con QR code local (generación sin Internet)
- **Enlaces de pago**: Soporte para Wise (todas las regiones) y PIX (Brasil)
- **Verificación de actualizaciones**: Chequea automáticamente GitHub para nuevas versiones

#### Configuración y Herramientas
- **Gestión de configuración**: Rutas por defecto personalizables
- **Verificación de dependencias**: Detecta FFmpeg y Python automáticamente
- **Limpieza de caché**: Elimina archivos temporales y logs antiguos (retención 7 días)
- **Visualización de logs**: Acceso a registros de errores en tiempo real
- **Restauración de configuración**: Vuelve a valores por defecto con un clic

#### Instalación y Distribución
- **PowerShell installer**: `install.ps1` y `install_secure.ps1` para instalación remota
- **Batch installer**: `install_dependencies.bat` con auto-detección de Python/FFmpeg
- **Bootstrap remoto**: Descarga automática del repo si no existe localmente
- **Ejecutable independiente**: `.exe` único (onefile) sin dependencias externas de Python
- **Licencia GPL v3**: Código abierto y distribuible

### 📦 Stack Técnico

- **Framework**: PyQt6 ≥6.0.0
- **Backend**: Python 3.8-3.14 (validado, recomendado 3.11)
- **Procesamiento de audio**: FFmpeg con filtro loudnorm
- **QR local**: Generación con qrcode[pil], sin API remota
- **Versionado**: Semantic Versioning
- **CI/CD**: GitHub Actions (tests, linting, security checks)

### 🛠️ Dependencias

```
PyQt6>=6.0.0
qrcode[pil]>=8.0.0
requests>=2.31.0
packaging>=24.0
pytest>=9.0.0
pytest-cov>=7.1.0
bandit>=1.7.0
pylint>=3.0.0
```

### 📋 Requisitos del Sistema

- **SO**: Windows 10/11 64-bit
- **Python**: 3.8 a 3.14 (preinstalado o auto-descargable)
- **FFmpeg**: Instalado en PATH (auto-descargable vía winget)
- **RAM**: Mínimo 2GB (recomendado 4GB+)
- **Almacenamiento**: 500MB para app + temporales

### 🎯 Características Documentadas

- ✅ Manual integrado en 3 idiomas
- ✅ Documentación de usuario (README multilenguaje)
- ✅ Guía de instalación con múltiples métodos
- ✅ Estructura de proyecto documentada
- ✅ Ejemplos de flujo de uso
- ✅ Guía de contribución

### 🔒 Seguridad y Estabilidad

- ✅ Código validado con pylint, bandit
- ✅ Tests unitarios con pytest (cobertura >70%)
- ✅ Manejo de errores robusto
- ✅ Validación de entrada de usuario
- ✅ Logs detallados para debugging
- ✅ Caché segura con limpieza automática

### 📝 Notas de versión

Esta es la versión inicial de lanzamiento (v1.0.0) con todas las características core implementadas y listas para uso en producción.

**El proyecto está basado en:**
- Arquitectura MVC con controladores por dominio
- Patrón Service Layer para lógica de negocio
- Event-driven architecture para UI responsiva
- Worker threads para operaciones pesadas

**Próximas versiones considerarán:**
- GPU acceleration para FFmpeg
- Análisis de waveform visual
- Soporte para más formatos (audio directo)
- Historial de procesamiento
- Presets de normalización predefinidos
- Interfaz de línea de comandos (CLI)

---

## Convenciones de versioning

Este proyecto sigue [Semantic Versioning](https://semver.org/):

- **MAJOR**: Cambios incompatibles con versiones anteriores
- **MINOR**: Nuevas características compatibles
- **PATCH**: Correcciones de bugs

Formato: `MAJOR.MINOR.PATCH` (ej: `1.0.0`)
