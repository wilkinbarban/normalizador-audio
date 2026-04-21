# Changelog · Change Log · Registro de Mudanças

- [Español](#español)
- [English](#english)
- [Português (Brasil)](#português-brasil)

---

## Español

Todos los cambios notables en este proyecto serán documentados en este archivo.

### [1.1.1] - 2026-04-21

#### ✨ Nuevas Funcionalidades

**Instalación automatizada de FFmpeg**
- **Validación en instaladores PowerShell**: `install.ps1` e `install_secure.ps1` ahora detectan si FFmpeg está en el sistema y lo instalan automáticamente mediante `winget` (paquete `Gyan.FFmpeg` con fallback a `FFmpeg.FFmpeg`), siguiendo el mismo patrón que la instalación de Python.
- **Auto-instalación al iniciar la app**: si FFmpeg no se detecta al arrancar, la aplicación ofrece instalarlo automáticamente con winget desde una ventana de consola, sin redirigir al usuario a un sitio web.
- **Menú Ayuda › Instalar FFmpeg**: nueva opción visible en el menú Ayuda que verifica si FFmpeg ya está instalado antes de actuar — si está presente muestra un mensaje informativo; si falta, inicia el instalador automático.

**Documentación y manual**
- **Manual integrado reescrito**: `manual_text_full` completamente renovado en los 3 idiomas con 10 secciones estructuradas, emojis e iconos, cubriendo todas las funcionalidades actuales incluyendo presets, waveform, GPU y gestión de FFmpeg.
- **Guía rápida actualizada**: `manual_text` actualizado con los 6 pasos esenciales que incluyen presets, perfil de referencia y la opción de instalar FFmpeg.

**Servicio de dependencias**
- Nuevos métodos en `DependencyService`: `install_ffmpeg_via_winget()`, `check_winget()` y `_refresh_windows_path()`.
- `check_ffmpeg()` ahora valida correctamente el código de retorno del proceso, no solo la ausencia de excepciones.

#### 🛠️ Compatibilidad

- Sin cambios incompatibles. No requiere actualización de configuración.

### [1.1.0] - 2026-04-20

#### ✨ Nuevas Funcionalidades

**Rendimiento y procesamiento**
- **Aceleración GPU inteligente (FFmpeg)**: detección automática de `hwaccel` compatible y activación opcional desde la interfaz.
- **Fallback automático a CPU**: si FFmpeg falla con `-hwaccel`, el procesamiento reintenta en CPU sin interrumpir el flujo.
- **Procesamiento paralelo mejorado**: ejecución concurrente de múltiples videos con límite configurable de workers.
- **Cancelación robusta**: al cancelar, se terminan todos los procesos FFmpeg activos de forma segura.

**Interfaz de usuario**
- **Presets predefinidos**: YouTube, Netflix, Spotify y Podcast, con modo `Custom`.
- **Selector de concurrencia**: nuevo control en UI para elegir cantidad de procesos simultáneos.
- **Waveform visual en Perfil**: previsualización de forma de onda generada con FFmpeg al seleccionar video de referencia.

**Infraestructura interna**
- Nuevos módulos: `gpu_service`, `waveform_service` y `waveform_worker`.
- Limpieza de caché ampliada para incluir waveform cache temporal.

#### 🛠️ Compatibilidad

- Sin cambios incompatibles en flujo principal para usuarios de v1.0.0.
- Configuración migrada automáticamente con nuevas claves (`gpu_accel`, `parallel_jobs`).

### [1.0.0] - 2026-04-20

#### ✨ Características Principales

**Core**
- **Normalización LUFS profesional**: Procesamiento de audio basado en FFmpeg loudnorm
- **Procesamiento por lotes**: Normalizar múltiples videos simultáneamente
- **Perfil de referencia**: Analizar un video como referencia y aplicar sus parámetros al lote
- **Reportes detallados**: Antes/después (I, LRA, TP) por video con estadísticas globales
- **Exportación de reportes**: CSV y TXT para análisis posterior

**Interfaz de Usuario**
- **Multilenguaje completo**: Español, English, Português (Brasil)
- **Tema dinámico**: Claro/Oscuro con transiciones suaves
- **Interfaz moderna**: Diseño responsivo basado en PyQt6
- **Indicadores de estado**: Progreso en tiempo real durante procesamiento

**Ayuda y Soporte**
- **Manual integrado**: Guía completa de uso directamente en la app
- **Diálogo de apoyo al proyecto**: Con QR code generado localmente (sin Internet)
- **Enlaces de pago**: Wise (todas las regiones) y PIX (Brasil)
- **Verificación de actualizaciones**: Chequea automáticamente GitHub para nuevas versiones

**Configuración y Herramientas**
- **Gestión de configuración**: Rutas por defecto personalizables
- **Verificación de dependencias**: Detecta FFmpeg y Python automáticamente
- **Limpieza de caché**: Elimina archivos temporales y logs antiguos (retención 7 días)
- **Visualización de logs**: Acceso a registros de errores en tiempo real
- **Restauración de configuración**: Vuelve a valores por defecto con un clic

**Instalación y Distribución**
- **PowerShell installer**: `install.ps1` y `install_secure.ps1` para instalación remota
- **Batch installer**: `install_dependencies.bat` con auto-detección de Python/FFmpeg
- **Bootstrap remoto**: Descarga automática del repo si no existe localmente
- **Ejecutable independiente**: `.exe` único (onefile) sin dependencias externas de Python
- **Licencia GPL v3**: Código abierto y distribuible

#### 📦 Stack Técnico

- **Framework**: PyQt6 ≥6.0.0
- **Backend**: Python 3.8–3.14 (recomendado 3.11)
- **Procesamiento de audio**: FFmpeg con filtro loudnorm
- **QR local**: qrcode[pil], sin API remota
- **CI/CD**: GitHub Actions (tests, linting, security checks)

#### 📋 Requisitos del Sistema

- **SO**: Windows 10/11 64-bit
- **Python**: 3.8–3.14 (preinstalado o auto-descargable)
- **FFmpeg**: Instalado en PATH (auto-descargable vía winget)
- **RAM**: Mínimo 2 GB (recomendado 4 GB+)

#### 📝 Notas

Primera versión de lanzamiento. Todas las características core están implementadas y listas para producción.

**Próximas versiones considerarán:**
- Soporte para formatos de audio directo (.mp3, .wav, .flac)
- Historial de procesamiento con rollback
- Interfaz de línea de comandos (CLI)

---

## English

All notable changes to this project will be documented in this file.

### [1.1.1] - 2026-04-21

#### ✨ New Features

**Automated FFmpeg management**
- **Validation in PowerShell installers**: `install.ps1` and `install_secure.ps1` now detect whether FFmpeg is available and install it automatically via `winget` (`Gyan.FFmpeg` with fallback to `FFmpeg.FFmpeg`), mirroring the existing Python install pattern.
- **Auto-install on app startup**: if FFmpeg is not found at launch, the app offers to install it automatically via winget in a console window — no browser redirect.
- **Help › Install FFmpeg menu item**: new visible option in the Help menu that checks if FFmpeg is already installed before acting — shows an informational message if present, or launches the automatic installer if missing.

**Documentation and manual**
- **Built-in manual rewritten**: `manual_text_full` fully rewritten in all 3 languages with 10 structured sections, emojis and icons, covering all current features including presets, waveform, GPU and FFmpeg management.
- **Quick guide updated**: `manual_text` updated with 6 essential steps including presets, reference profile, and the Install FFmpeg option.

**Dependency service**
- New methods on `DependencyService`: `install_ffmpeg_via_winget()`, `check_winget()`, and `_refresh_windows_path()`.
- `check_ffmpeg()` now correctly validates the process return code, not just the absence of exceptions.

#### 🛠️ Compatibility

- No breaking changes. No configuration update required.

### [1.1.0] - 2026-04-20

#### ✨ New Features

**Performance and processing**
- **Smart GPU acceleration (FFmpeg)**: automatic detection of supported `hwaccel` method with optional UI toggle.
- **Automatic CPU fallback**: if FFmpeg fails with `-hwaccel`, processing retries on CPU without breaking the workflow.
- **Improved parallel processing**: concurrent processing for multiple videos with configurable worker limit.
- **Robust cancellation**: cancel now terminates all active FFmpeg processes safely.

**User interface**
- **Built-in presets**: YouTube, Netflix, Spotify and Podcast, plus `Custom` mode.
- **Concurrency selector**: new UI control to choose simultaneous processing jobs.
- **Visual waveform in Profile tab**: waveform preview generated with FFmpeg when selecting a reference video.

**Internal infrastructure**
- New modules: `gpu_service`, `waveform_service`, and `waveform_worker`.
- Cache cleanup now also handles temporary waveform cache.

#### 🛠️ Compatibility

- No breaking changes for users upgrading from v1.0.0.
- Configuration auto-migration with new keys (`gpu_accel`, `parallel_jobs`).

### [1.0.0] - 2026-04-20

#### ✨ Main Features

**Core**
- **Professional LUFS normalization**: FFmpeg loudnorm-based audio processing
- **Batch processing**: Normalize multiple videos at the same time
- **Reference profile**: Analyze a video as reference and apply its parameters to the batch
- **Detailed reports**: Before/after (I, LRA, TP) per video with global statistics
- **Report export**: CSV and TXT for further analysis

**User Interface**
- **Full multilingual support**: Español, English, Português (Brasil)
- **Dynamic theme**: Light/Dark with smooth transitions
- **Modern interface**: Responsive design based on PyQt6
- **Status indicators**: Real-time progress during processing

**Help and Support**
- **Built-in manual**: Complete usage guide directly in the app
- **Support the project dialog**: With locally generated QR code (no Internet required)
- **Payment links**: Wise (all regions) and PIX (Brazil)
- **Update checker**: Automatically checks GitHub for new versions

**Configuration and Tools**
- **Configuration manager**: Customizable default paths
- **Dependency checker**: Detects FFmpeg and Python automatically
- **Cache cleanup**: Removes temporary files and old logs (7-day retention)
- **Log viewer**: Real-time access to error logs
- **Configuration restore**: Reset to defaults in one click

**Installation and Distribution**
- **PowerShell installer**: `install.ps1` and `install_secure.ps1` for remote installation
- **Batch installer**: `install_dependencies.bat` with Python/FFmpeg auto-detection
- **Remote bootstrap**: Auto-downloads the repo if not present locally
- **Standalone executable**: Single onefile `.exe` with no external Python dependencies
- **GPL v3 license**: Open source and freely distributable

#### 📦 Tech Stack

- **Framework**: PyQt6 ≥6.0.0
- **Backend**: Python 3.8–3.14 (recommended 3.11)
- **Audio processing**: FFmpeg with loudnorm filter
- **Local QR**: qrcode[pil], no remote API
- **CI/CD**: GitHub Actions (tests, linting, security checks)

#### 📋 System Requirements

- **OS**: Windows 10/11 64-bit
- **Python**: 3.8–3.14 (preinstalled or auto-downloadable)
- **FFmpeg**: Installed in PATH (auto-downloadable via winget)
- **RAM**: Minimum 2 GB (4 GB+ recommended)

#### 📝 Release Notes

First release version. All core features are implemented and production-ready.

**Future versions may include:**
- Direct audio format support (.mp3, .wav, .flac)
- Processing history with rollback
- Command-line interface (CLI)

---

## Português (Brasil)

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

### [1.1.1] - 2026-04-21

#### ✨ Novas Funcionalidades

**Gerenciamento automatizado de FFmpeg**
- **Validação nos instaladores PowerShell**: `install.ps1` e `install_secure.ps1` agora verificam se o FFmpeg está disponível e o instalam automaticamente via `winget` (pacote `Gyan.FFmpeg` com fallback para `FFmpeg.FFmpeg`), seguindo o mesmo padrão da instalação do Python.
- **Auto-instalação na inicialização do app**: se o FFmpeg não for detectado ao iniciar, o aplicativo oferece instalá-lo automaticamente via winget em uma janela de console — sem redirecionar o usuário para um site.
- **Menu Ajuda › Instalar FFmpeg**: nova opção visível no menu Ajuda que verifica se o FFmpeg já está instalado antes de agir — exibe mensagem informativa se presente, ou inicia o instalador automático se ausente.

**Documentação e manual**
- **Manual integrado reescrito**: `manual_text_full` completamente renovado nos 3 idiomas com 10 seções estruturadas, emojis e ícones, cobrindo todas as funcionalidades atuais incluindo presets, waveform, GPU e gerenciamento de FFmpeg.
- **Guia rápido atualizado**: `manual_text` atualizado com os 6 passos essenciais que incluem presets, perfil de referência e a opção de instalar o FFmpeg.

**Serviço de dependências**
- Novos métodos em `DependencyService`: `install_ffmpeg_via_winget()`, `check_winget()` e `_refresh_windows_path()`.
- `check_ffmpeg()` agora valida corretamente o código de retorno do processo, não apenas a ausência de exceções.

#### 🛠️ Compatibilidade

- Sem mudanças incompatíveis. Nenhuma atualização de configuração necessária.

### [1.1.0] - 2026-04-20

#### ✨ Novas Funcionalidades

**Desempenho e processamento**
- **Aceleração GPU inteligente (FFmpeg)**: detecção automática de método `hwaccel` compatível com ativação opcional na interface.
- **Fallback automático para CPU**: se o FFmpeg falhar com `-hwaccel`, o processamento tenta novamente em CPU sem quebrar o fluxo.
- **Processamento paralelo melhorado**: execução concorrente de múltiplos vídeos com limite configurável de workers.
- **Cancelamento robusto**: ao cancelar, todos os processos FFmpeg ativos são encerrados com segurança.

**Interface do usuário**
- **Presets integrados**: YouTube, Netflix, Spotify e Podcast, além do modo `Custom`.
- **Seletor de concorrência**: novo controle na UI para definir quantidade de processos simultâneos.
- **Waveform visual na aba Perfil**: pré-visualização da forma de onda gerada com FFmpeg ao selecionar vídeo de referência.

**Infraestrutura interna**
- Novos módulos: `gpu_service`, `waveform_service` e `waveform_worker`.
- Limpeza de cache ampliada para incluir cache temporário de waveform.

#### 🛠️ Compatibilidade

- Sem mudanças incompatíveis para usuários que atualizam da v1.0.0.
- Migração automática de configuração com novas chaves (`gpu_accel`, `parallel_jobs`).

### [1.0.0] - 2026-04-20

#### ✨ Principais Funcionalidades

**Core**
- **Normalização LUFS profissional**: Processamento de áudio baseado no filtro loudnorm do FFmpeg
- **Processamento em lote**: Normalizar múltiplos vídeos simultaneamente
- **Perfil de referência**: Analisar um vídeo como referência e aplicar seus parâmetros ao lote
- **Relatórios detalhados**: Antes/depois (I, LRA, TP) por vídeo com estatísticas globais
- **Exportação de relatórios**: CSV e TXT para análise posterior

**Interface do Usuário**
- **Suporte multilíngue completo**: Español, English, Português (Brasil)
- **Tema dinâmico**: Claro/Escuro com transições suaves
- **Interface moderna**: Design responsivo baseado em PyQt6
- **Indicadores de status**: Progresso em tempo real durante o processamento

**Ajuda e Suporte**
- **Manual integrado**: Guia completo de uso diretamente no aplicativo
- **Diálogo de apoio ao projeto**: Com QR code gerado localmente (sem Internet)
- **Links de pagamento**: Wise (todas as regiões) e PIX (Brasil)
- **Verificação de atualizações**: Verifica automaticamente o GitHub por novas versões

**Configuração e Ferramentas**
- **Gerenciador de configuração**: Caminhos padrão personalizáveis
- **Verificador de dependências**: Detecta FFmpeg e Python automaticamente
- **Limpeza de cache**: Remove arquivos temporários e logs antigos (retenção de 7 dias)
- **Visualizador de logs**: Acesso em tempo real aos registros de erros
- **Restauração de configuração**: Redefinir padrões com um clique

**Instalação e Distribuição**
- **Instalador PowerShell**: `install.ps1` e `install_secure.ps1` para instalação remota
- **Instalador Batch**: `install_dependencies.bat` com auto-detecção de Python/FFmpeg
- **Bootstrap remoto**: Download automático do repositório se não existir localmente
- **Executável independente**: `.exe` único (onefile) sem dependências externas de Python
- **Licença GPL v3**: Código aberto e distribuível livremente

#### 📦 Stack Técnico

- **Framework**: PyQt6 ≥6.0.0
- **Backend**: Python 3.8–3.14 (recomendado 3.11)
- **Processamento de áudio**: FFmpeg com filtro loudnorm
- **QR local**: qrcode[pil], sem API remota
- **CI/CD**: GitHub Actions (testes, linting, verificações de segurança)

#### 📋 Requisitos do Sistema

- **SO**: Windows 10/11 64-bit
- **Python**: 3.8–3.14 (pré-instalado ou baixável automaticamente)
- **FFmpeg**: Instalado no PATH (baixável automaticamente via winget)
- **RAM**: Mínimo 2 GB (4 GB+ recomendado)

#### 📝 Notas de Versão

Primeira versão de lançamento. Todas as funcionalidades principais estão implementadas e prontas para produção.

**Versões futuras poderão incluir:**
- Suporte a formatos de áudio direto (.mp3, .wav, .flac)
- Histórico de processamento com rollback
- Interface de linha de comando (CLI)

---

## Versioning · Versionado · Versionamento

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes / Cambios incompatibles / Mudanças incompatíveis
- **MINOR**: New features / Nuevas características / Novas funcionalidades
- **PATCH**: Bug fixes / Corrección de bugs / Correção de bugs

Format: `MAJOR.MINOR.PATCH` — e.g. `1.0.0`
