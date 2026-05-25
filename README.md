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

> Educational project. Normalizador Audio demonstrates Python + PyQt6 desktop development, FFmpeg loudness normalization, background workers, and multilingual UI patterns.

## Language / Idioma / Idioma

- [Español](#espanol)
- [English](#english)
- [Português Brasil](#portugues-brasil)

## Screenshots

![Main application view](normalizador_app/assets/Captura_1.png)
![Audio profile view](normalizador_app/assets/Captura_2.png)
![Reports view](normalizador_app/assets/Captura_3.png)

## Espanol

### Que hace

Normalizador Audio es una aplicacion de escritorio para Windows que normaliza el volumen de lotes de video con FFmpeg `loudnorm` (LUFS). Incluye presets, perfil de referencia, procesamiento paralelo, aceleracion GPU opcional, reportes antes/despues y una interfaz multilenguaje.

### Requisitos

- Windows 10/11.
- Python instalado o instalable mediante `winget`.
- FFmpeg instalado o instalable mediante `winget`.
- Conexion a Internet para bootstrap remoto e instalacion automatica de dependencias.

El instalador no fija una version estatica de Python. Detecta la version `major.minor` disponible en el sistema y la usa como piso local de compatibilidad. Ejemplo: si detecta Python 3.14, el entorno local queda tratado como Python `>=3.14`.

### Instalacion recomendada

Si ya tienes el repositorio:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; .\install.ps1
```

Si no tienes el repositorio:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; irm https://raw.githubusercontent.com/wilkinbarban/normalizador-audio/main/install.ps1 | iex
```

`install.ps1` es ahora el instalador unico. Si se ejecuta fuera del proyecto, descarga el repositorio desde GitHub, lo instala por defecto en `%USERPROFILE%\Desktop\normalizador-audio`, crea o valida `.venv`, instala `requirements.txt`, comprueba FFmpeg y lanza la aplicacion.

Para cambiar el directorio de instalacion remota:

```powershell
$env:NORM_INSTALL_DIR = "D:\Apps\normalizador-audio"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; irm https://raw.githubusercontent.com/wilkinbarban/normalizador-audio/main/install.ps1 | iex
```

### Ejecucion manual despues de clonar

Si ya clonaste o descargaste el repositorio en una carpeta, tambien puedes iniciar la app con:

```bat
Iniciar.bat
```

`Iniciar.bat` debe ejecutarse desde la raiz del proyecto. Valida que el proyecto este completo, detecta Python, crea o reutiliza `.venv`, instala `requirements.txt`, comprueba FFmpeg y abre `normalizador.py`. No descarga el repositorio; para bootstrap remoto usa `install.ps1`.

Los archivos de estado de usuario no se guardan dentro del repositorio. Configuracion, perfil y logs viven en:

```text
%LOCALAPPDATA%\NormalizadorAudio\
```

## English

### What It Does

Normalizador Audio is a Windows desktop application that normalizes loudness across video batches with FFmpeg `loudnorm` (LUFS). It includes presets, reference profiles, parallel processing, optional GPU acceleration, before/after reports, and a multilingual UI.

### Requirements

- Windows 10/11.
- Python already installed or installable through `winget`.
- FFmpeg already installed or installable through `winget`.
- Internet access for remote bootstrap and automatic dependency setup.

The installer does not pin a static Python version. It detects the available `major.minor` Python version and uses it as the local compatibility floor. Example: Python 3.14 detected means the local environment is treated as Python `>=3.14`.

### Recommended Install

If you already have the repository:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; .\install.ps1
```

If you do not have the repository:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; irm https://raw.githubusercontent.com/wilkinbarban/normalizador-audio/main/install.ps1 | iex
```

`install.ps1` is now the single installer. When run outside the project, it downloads the GitHub repository, installs it by default to `%USERPROFILE%\Desktop\normalizador-audio`, creates or validates `.venv`, installs `requirements.txt`, checks FFmpeg, and launches the app.

To change the remote install directory:

```powershell
$env:NORM_INSTALL_DIR = "D:\Apps\normalizador-audio"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; irm https://raw.githubusercontent.com/wilkinbarban/normalizador-audio/main/install.ps1 | iex
```

### Manual Run After Cloning

If you already cloned or downloaded the repository into a folder, you can also start the app with:

```bat
Iniciar.bat
```

`Iniciar.bat` must be run from the project root. It checks that the project is complete, detects Python, creates or reuses `.venv`, installs `requirements.txt`, checks FFmpeg, and opens `normalizador.py`. It does not download the repository; use `install.ps1` for remote bootstrap.

User state files are not stored inside the repository. Config, profile, and logs live in:

```text
%LOCALAPPDATA%\NormalizadorAudio\
```

## Portugues Brasil

### O Que Faz

Normalizador Audio e um aplicativo desktop para Windows que normaliza o volume de lotes de video com FFmpeg `loudnorm` (LUFS). Inclui presets, perfil de referencia, processamento paralelo, aceleracao GPU opcional, relatorios antes/depois e interface multilingue.

### Requisitos

- Windows 10/11.
- Python ja instalado ou instalavel via `winget`.
- FFmpeg ja instalado ou instalavel via `winget`.
- Internet para bootstrap remoto e instalacao automatica de dependencias.

O instalador nao fixa uma versao estatica de Python. Ele detecta a versao `major.minor` disponivel no sistema e usa essa versao como piso local de compatibilidade. Exemplo: Python 3.14 detectado significa ambiente local tratado como Python `>=3.14`.

### Instalacao Recomendada

Se voce ja tem o repositorio:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; .\install.ps1
```

Se voce nao tem o repositorio:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; irm https://raw.githubusercontent.com/wilkinbarban/normalizador-audio/main/install.ps1 | iex
```

`install.ps1` agora e o instalador unico. Quando executado fora do projeto, ele baixa o repositorio do GitHub, instala por padrao em `%USERPROFILE%\Desktop\normalizador-audio`, cria ou valida `.venv`, instala `requirements.txt`, verifica FFmpeg e inicia o app.

Para mudar o diretorio da instalacao remota:

```powershell
$env:NORM_INSTALL_DIR = "D:\Apps\normalizador-audio"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; irm https://raw.githubusercontent.com/wilkinbarban/normalizador-audio/main/install.ps1 | iex
```

### Execucao Manual Depois de Clonar

Se voce ja clonou ou baixou o repositorio em uma pasta, tambem pode iniciar o app com:

```bat
Iniciar.bat
```

`Iniciar.bat` deve ser executado a partir da raiz do projeto. Ele valida que o projeto esta completo, detecta Python, cria ou reutiliza `.venv`, instala `requirements.txt`, verifica FFmpeg e abre `normalizador.py`. Ele nao baixa o repositorio; para bootstrap remoto use `install.ps1`.

Os arquivos de estado do usuario nao ficam dentro do repositorio. Configuracao, perfil e logs ficam em:

```text
%LOCALAPPDATA%\NormalizadorAudio\
```

## Project Structure

| Path | Description |
| --- | --- |
| `normalizador.py` | Main launcher entry point |
| `install.ps1` | Single PowerShell installer, remote bootstrapper, dependency setup, and launcher |
| `Iniciar.bat` | Local launcher for a cloned/downloaded project folder |
| `requirements.txt` | Python dependencies and runtime policy note |
| `normalizador_app/main.py` | Application bootstrap |
| `normalizador_app/core/` | Config, constants, i18n, and logging |
| `normalizador_app/services/` | Audio, dependency, update, GPU, waveform, and report services |
| `normalizador_app/ui/` | Main window, styles, widgets, controllers, and dialogs |
| `normalizador_app/workers/` | Background workers for processing and analysis |
| `normalizador_app/assets/` | Icons and screenshots |
| `tests/` | Automated test suite |
| `.github/workflows/` | CI pipelines |

## Troubleshooting

- Python installed but not detected: close the terminal, open a new one, and run `install.ps1` again.
- FFmpeg installed but not detected: close the terminal so PATH updates are visible, then rerun `install.ps1`.
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
