<div align="center">
  <img src="normalizador_app/assets/icon.png" alt="Normalizador Audio Logo" width="180">
  <h1>Normalizador Audio</h1>
  <p>
    <a href="https://www.gnu.org/licenses/gpl-3.0"><img alt="License: GPL v3" src="https://img.shields.io/badge/License-GPLv3-blue.svg"></a>
    <a href="https://www.python.org/downloads/"><img alt="Python detected+" src="https://img.shields.io/badge/Python-detected%2B-green.svg"></a>
    <a href="https://www.microsoft.com/windows"><img alt="Windows 10/11" src="https://img.shields.io/badge/Platform-Windows%2010%2F11-lightgrey.svg"></a>
    <a href="https://github.com/wilkinbarban/normalizador-audio/releases"><img alt="Releases" src="https://img.shields.io/github/v/release/wilkinbarban/normalizador-audio"></a>
  </p>
</div>

> Educational project. Normalizador Audio demonstrates Python + PyQt6 desktop development, FFmpeg loudness normalization, background workers, reporting workflows, and multilingual UI patterns.

## Language / Idioma / Idioma

- [Español](#espanol)
- [English](#english)
- [Português Brasil](#portugues-brasil)

## Screenshots

![Main application view](normalizador_app/assets/Captura_1.png)
![Audio profile view](normalizador_app/assets/Captura_2.png)
![Reports view](normalizador_app/assets/Captura_3.png)

## Espanol

### Descripcion

Normalizador Audio es una aplicacion de escritorio para Windows que normaliza el volumen de lotes de video con FFmpeg `loudnorm` (LUFS). Incluye presets, perfil de referencia, procesamiento paralelo, aceleracion GPU opcional, reportes antes/despues y una interfaz multilenguaje.

### Caracteristicas

- Normalizacion LUFS basada en FFmpeg.
- Procesamiento por lotes con tabla de estado por archivo.
- Presets para YouTube, Netflix, Spotify, Podcast y modo Custom.
- Perfil de referencia para aplicar parametros de un video modelo.
- Waveform visual en la pestaña Perfil.
- Reportes CSV/TXT con metricas antes/despues.
- Tema claro/oscuro y soporte Español, English y Português Brasil.

### Requisitos

- Windows 10/11.
- PowerShell 5.1 o superior.
- Conexion a Internet para instalar dependencias automaticamente.
- `winget` recomendado para instalar Python y FFmpeg si faltan.

El instalador detecta la version `major.minor` de Python disponible y la usa como piso local de compatibilidad. Ejemplo: si detecta Python 3.14, el entorno local queda tratado como Python `>=3.14`.

### Instalacion con un solo comando

Ejecuta este unico comando en PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; irm https://raw.githubusercontent.com/wilkinbarban/normalizador-audio/main/install.ps1 | iex
```

**Como funciona:** `install.ps1` valida si los archivos del proyecto ya existen en la carpeta actual. Si no existen, descarga el repositorio desde GitHub mediante HTTPS, valida que el archivo descargado no este vacio, lo extrae por defecto en `%USERPROFILE%\Desktop\normalizador-audio`, crea o reutiliza `.venv`, instala `requirements.txt`, comprueba Python y FFmpeg, y lanza la aplicacion.

Para cambiar la carpeta de instalacion remota antes de ejecutar el comando:

```powershell
$env:NORM_INSTALL_DIR = "D:\Apps\normalizador-audio"
```

Los archivos de usuario no se guardan dentro del repositorio. Configuracion, perfil y logs viven en:

```text
%LOCALAPPDATA%\NormalizadorAudio\
```

## English

### Description

Normalizador Audio is a Windows desktop application that normalizes loudness across video batches with FFmpeg `loudnorm` (LUFS). It includes presets, reference profiles, parallel processing, optional GPU acceleration, before/after reports, and a multilingual UI.

### Features

- FFmpeg-powered LUFS normalization.
- Batch processing with per-file status table.
- YouTube, Netflix, Spotify, Podcast, and Custom presets.
- Reference profile workflow for applying settings from a model video.
- Visual waveform preview in the Profile tab.
- CSV/TXT reports with before/after metrics.
- Light/dark themes and Spanish, English, and Brazilian Portuguese support.

### Requirements

- Windows 10/11.
- PowerShell 5.1 or newer.
- Internet access for automatic dependency setup.
- `winget` recommended for automatic Python and FFmpeg installation when missing.

The installer detects the available Python `major.minor` version and uses it as the local compatibility floor. Example: Python 3.14 detected means the local environment is treated as Python `>=3.14`.

### One-Command Installation

Run this single command in PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; irm https://raw.githubusercontent.com/wilkinbarban/normalizador-audio/main/install.ps1 | iex
```

**How it works:** `install.ps1` checks whether the project files already exist in the current folder. If they are missing, it downloads the repository from GitHub over HTTPS, verifies that the downloaded archive is not empty, extracts it by default to `%USERPROFILE%\Desktop\normalizador-audio`, creates or reuses `.venv`, installs `requirements.txt`, checks Python and FFmpeg, and launches the app.

To change the remote install folder before running the command:

```powershell
$env:NORM_INSTALL_DIR = "D:\Apps\normalizador-audio"
```

User files are not stored inside the repository. Config, profile, and logs live in:

```text
%LOCALAPPDATA%\NormalizadorAudio\
```

## Portugues Brasil

### Descricao

Normalizador Audio e um aplicativo desktop para Windows que normaliza o volume de lotes de video com FFmpeg `loudnorm` (LUFS). Inclui presets, perfil de referencia, processamento paralelo, aceleracao GPU opcional, relatorios antes/depois e interface multilingue.

### Recursos

- Normalizacao LUFS baseada em FFmpeg.
- Processamento em lote com tabela de status por arquivo.
- Presets YouTube, Netflix, Spotify, Podcast e modo Custom.
- Fluxo de perfil de referencia para aplicar parametros de um video modelo.
- Pre-visualizacao visual de waveform na aba Perfil.
- Relatorios CSV/TXT com metricas antes/depois.
- Temas claro/escuro e suporte a Espanhol, Ingles e Portugues Brasil.

### Requisitos

- Windows 10/11.
- PowerShell 5.1 ou superior.
- Internet para instalacao automatica de dependencias.
- `winget` recomendado para instalar Python e FFmpeg automaticamente se estiverem ausentes.

O instalador detecta a versao `major.minor` de Python disponivel e usa essa versao como piso local de compatibilidade. Exemplo: Python 3.14 detectado significa ambiente local tratado como Python `>=3.14`.

### Instalacao com Um Unico Comando

Execute este unico comando no PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; irm https://raw.githubusercontent.com/wilkinbarban/normalizador-audio/main/install.ps1 | iex
```

**Como funciona:** `install.ps1` verifica se os arquivos do projeto ja existem na pasta atual. Se estiverem ausentes, baixa o repositorio do GitHub por HTTPS, valida que o arquivo baixado nao esta vazio, extrai por padrao em `%USERPROFILE%\Desktop\normalizador-audio`, cria ou reutiliza `.venv`, instala `requirements.txt`, verifica Python e FFmpeg, e inicia o aplicativo.

Para mudar a pasta da instalacao remota antes de executar o comando:

```powershell
$env:NORM_INSTALL_DIR = "D:\Apps\normalizador-audio"
```

Os arquivos do usuario nao ficam dentro do repositorio. Configuracao, perfil e logs ficam em:

```text
%LOCALAPPDATA%\NormalizadorAudio\
```

## Project Structure

| Path | Description |
| --- | --- |
| `normalizador.py` | Application entry point |
| `install.ps1` | Single PowerShell installer, remote bootstrapper, dependency setup, and launcher |
| `requirements.txt` | Python dependencies and runtime policy note |
| `normalizador_app/main.py` | Application bootstrap |
| `normalizador_app/core/` | Config, constants, i18n, paths, and logging |
| `normalizador_app/services/` | Audio, dependency, update, GPU, waveform, and report services |
| `normalizador_app/ui/` | Main window, styles, widgets, controllers, and dialogs |
| `normalizador_app/workers/` | Background workers for processing and analysis |
| `normalizador_app/assets/` | Icons and screenshots |
| `tests/` | Automated test suite |
| `.github/workflows/` | CI and release pipelines |

## Troubleshooting

- Python installed but not detected: close the terminal, open a new one, and run the install command again.
- FFmpeg installed but not detected: close the terminal so PATH updates are visible, then rerun the install command.
- Dependency install failed: inspect `.venv\install.log`, then try `.venv\Scripts\pip.exe install -r requirements.txt`.
- App exits with an error: check the console output and `%LOCALAPPDATA%\NormalizadorAudio\normalizador_errors.log`.

## Educational Disclaimer

This software is provided for educational purposes only. It demonstrates desktop architecture, FFmpeg-based audio normalization, worker-based processing, report export workflows, multilingual runtime UI, and automated Windows dependency setup.

The author is not responsible for misuse by third parties.

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for the full license text.

```text
Normalizador Audio  Copyright (C) 2026  wilkinbarban
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions; see LICENSE for details.
```

## Links

- [Code](https://github.com/wilkinbarban/normalizador-audio)
- [Issues](https://github.com/wilkinbarban/normalizador-audio/issues)
- [Pull requests](https://github.com/wilkinbarban/normalizador-audio/pulls)
- [Actions](https://github.com/wilkinbarban/normalizador-audio/actions)
- [Security](https://github.com/wilkinbarban/normalizador-audio/security)
