# Changelog · Change Log · Registro de Mudanças

- [Español](#español)
- [English](#english)
- [Português (Brasil)](#português-brasil)

---

## Español

Todos los cambios notables en este proyecto serán documentados en este archivo.

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
- Aceleración GPU para FFmpeg
- Waveform visual antes/después
- Soporte para formatos de audio directo (.mp3, .wav, .flac)
- Historial de procesamiento con rollback
- Presets predefinidos (YouTube, Netflix, Spotify, Podcast)
- Interfaz de línea de comandos (CLI)

---

## English

All notable changes to this project will be documented in this file.

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
- GPU acceleration for FFmpeg
- Visual waveform before/after
- Direct audio format support (.mp3, .wav, .flac)
- Processing history with rollback
- Built-in presets (YouTube, Netflix, Spotify, Podcast)
- Command-line interface (CLI)

---

## Português (Brasil)

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

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
- Aceleração GPU para FFmpeg
- Forma de onda visual antes/depois
- Suporte a formatos de áudio direto (.mp3, .wav, .flac)
- Histórico de processamento com rollback
- Presets integrados (YouTube, Netflix, Spotify, Podcast)
- Interface de linha de comando (CLI)

---

## Versioning · Versionado · Versionamento

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes / Cambios incompatibles / Mudanças incompatíveis
- **MINOR**: New features / Nuevas características / Novas funcionalidades
- **PATCH**: Bug fixes / Corrección de bugs / Correção de bugs

Format: `MAJOR.MINOR.PATCH` — e.g. `1.0.0`
