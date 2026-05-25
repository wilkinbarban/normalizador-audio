#Requires -Version 5.1
<#
.SYNOPSIS
    Normalizador Audio - One-command installer and launcher for Windows.

.DESCRIPTION
    Uses a single installer for both local and remote execution. If project
    files are not present next to this script, it downloads the repository,
    installs it to a user-owned directory, and delegates to the local copy.

    The installer detects the installed Python runtime and treats that
    major.minor version as the local minimum dependency floor, creates an
    isolated virtual environment, installs Python requirements, validates
    FFmpeg, and launches the application.

    This script is intended for EDUCATIONAL USE ONLY.

.EXAMPLE
    .\install.ps1

    irm https://raw.githubusercontent.com/wilkinbarban/normalizador-audio/main/install.ps1 | iex

.NOTES
    Platform : Windows 10/11
    License  : GNU General Public License v3.0
    Author   : wilkinbarban
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$Version = "1.1.0"

$Host.UI.RawUI.WindowTitle = "Normalizador Audio - Instalando..."
Clear-Host

Write-Host ""
Write-Host "  *** N O R M A L I Z A D O R   A U D I O ***" -ForegroundColor Green
Write-Host "  ===========================================" -ForegroundColor DarkCyan
Write-Host "   Instalador y Lanzador - Version $Version" -ForegroundColor Gray
Write-Host "  ===========================================" -ForegroundColor DarkCyan
Write-Host ""

function Show-Step {
    param([string]$Message)
    Write-Host "  >> $Message..." -ForegroundColor Gray
}

function Show-Info {
    param([string]$Message)
    Write-Host "  [INFO] $Message" -ForegroundColor Cyan
}

function Show-Warn {
    param([string]$Message)
    Write-Host "  [!] $Message" -ForegroundColor Yellow
}

function Show-Ok {
    param([string]$Message)
    Write-Host "  [OK] $Message" -ForegroundColor Green
}

function Show-Error {
    param(
        [string]$Title,
        [string]$Detail,
        [string]$Action
    )

    Write-Host ""
    Write-Host "  [ERROR] $Title" -ForegroundColor Red
    Write-Host "  --------------------------------------------------------" -ForegroundColor Red
    Write-Host "   Detalle : $Detail" -ForegroundColor Yellow
    Write-Host "   Accion  : $Action" -ForegroundColor Cyan
    Write-Host "  --------------------------------------------------------" -ForegroundColor Red
    Write-Host ""
    Read-Host "  Presione Enter para salir..."
    exit 1
}

function Run-WithProgress {
    param(
        [string]$FileName,
        [string]$Arguments,
        [string]$Message
    )

    $pinfo = New-Object System.Diagnostics.ProcessStartInfo
    $pinfo.FileName = $FileName
    $pinfo.Arguments = $Arguments
    $pinfo.RedirectStandardOutput = $true
    $pinfo.RedirectStandardError = $true
    $pinfo.UseShellExecute = $false
    $pinfo.CreateNoWindow = $true

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $pinfo
    $process.EnableRaisingEvents = $true

    $stdoutList = New-Object System.Collections.Generic.List[string]
    $stderrList = New-Object System.Collections.Generic.List[string]

    $outEvent = Register-ObjectEvent -InputObject $process -EventName "OutputDataReceived" -Action {
        if ($EventArgs.Data) {
            $Event.MessageData.Add($EventArgs.Data)
            $script:LastRawLine = $EventArgs.Data
        }
    } -MessageData $stdoutList

    $errEvent = Register-ObjectEvent -InputObject $process -EventName "ErrorDataReceived" -Action {
        if ($EventArgs.Data) {
            $Event.MessageData.Add($EventArgs.Data)
        }
    } -MessageData $stderrList

    try {
        $script:LastRawLine = ""
        $process.Start() | Out-Null
        $process.BeginOutputReadLine()
        $process.BeginErrorReadLine()
    } catch {
        Unregister-Event -SourceIdentifier $outEvent.Name -ErrorAction SilentlyContinue
        Unregister-Event -SourceIdentifier $errEvent.Name -ErrorAction SilentlyContinue
        return @{ Success = $false; Error = $_.Exception.Message; ExitCode = -1 }
    }

    $spinner = @('|', '/', '-', '\')
    $index = 0

    while (-not $process.HasExited) {
        $displayMessage = $Message
        $lastLine = $script:LastRawLine

        if ($lastLine) {
            if ($lastLine -match 'Downloading\s+([a-zA-Z0-9_\-\.]+)') {
                $displayMessage = "Descargando $($Matches[1])"
            } elseif ($lastLine -match 'Installing collected packages:\s*(.*)') {
                $displayMessage = "Instalando paquetes"
            } elseif ($lastLine -match 'Requirement already satisfied:\s*([a-zA-Z0-9_\-\.\:\(\)\ ]+)') {
                $matched = $Matches[1]
                if ($matched -match '^([a-zA-Z0-9_\-]+)') {
                    $displayMessage = "Verificando $($Matches[1])"
                }
            }
        }

        if ($displayMessage.Length -gt 50) {
            $displayMessage = $displayMessage.Substring(0, 47) + "..."
        }

        Write-Host -NoNewline "`r  $($spinner[$index]) $displayMessage..." -ForegroundColor Cyan
        Start-Sleep -Milliseconds 100
        $index = ($index + 1) % $spinner.Count
    }

    Unregister-Event -SourceIdentifier $outEvent.Name -ErrorAction SilentlyContinue
    Unregister-Event -SourceIdentifier $errEvent.Name -ErrorAction SilentlyContinue

    $stdout = $stdoutList -join "`n"
    $stderr = $stderrList -join "`n"
    $exitCode = $process.ExitCode

    Write-Host -NoNewline "`r                                                                              `r"

    if ($exitCode -eq 0) {
        Write-Host "  [OK] $Message [Completado]" -ForegroundColor Green
        return @{ Success = $true; Stdout = $stdout; Stderr = $stderr; ExitCode = $exitCode }
    }

    Write-Host "  [FAIL] $Message [Fallo]" -ForegroundColor Red
    return @{ Success = $false; Stdout = $stdout; Stderr = $stderr; ExitCode = $exitCode }
}

function Invoke-PythonCode {
    param(
        [string]$PythonCommand,
        [string]$Code
    )

    $parts = $PythonCommand -split ' '
    if ($parts.Count -gt 1) {
        return & $parts[0] $parts[1] -c $Code 2>&1
    }

    return & $parts[0] -c $Code 2>&1
}

function Get-PythonMinorVersion {
    param([string]$PythonCommand)

    try {
        $version = Invoke-PythonCode -PythonCommand $PythonCommand -Code "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        if ($LASTEXITCODE -eq 0 -and "$version" -match '^\d+\.\d+$') {
            return "$version"
        }
    } catch { }

    return $null
}

function Test-PythonMinimum {
    param(
        [string]$PythonPath,
        [string]$MinimumVersion
    )

    try {
        $null = & $PythonPath -c "import sys; minimum=tuple(map(int, '$MinimumVersion'.split('.'))); raise SystemExit(0 if sys.version_info[:2] >= minimum else 1)" 2>&1
        return ($LASTEXITCODE -eq 0)
    } catch {
        return $false
    }
}

function Refresh-CurrentPath {
    $machinePath = [System.Environment]::GetEnvironmentVariable('PATH', 'Machine')
    $userPath = [System.Environment]::GetEnvironmentVariable('PATH', 'User')
    $env:PATH = "$machinePath;$userPath"

    $wingetLinks = Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Links'
    if ((Test-Path $wingetLinks) -and -not (($env:PATH -split ';') -contains $wingetLinks)) {
        $env:PATH = "$env:PATH;$wingetLinks"
    }
}

$ScriptRootCandidates = @(
    $PSScriptRoot,
    $(if (-not [string]::IsNullOrWhiteSpace($PSCommandPath)) { Split-Path -Parent $PSCommandPath }),
    (Get-Location).Path,
    '.'
)

$ScriptRoot = $null
foreach ($candidate in $ScriptRootCandidates) {
    if (-not [string]::IsNullOrWhiteSpace($candidate)) {
        $ScriptRoot = $candidate.Trim()
        break
    }
}

if ([string]::IsNullOrWhiteSpace($ScriptRoot)) {
    Show-Error "Error de Directorio" "No se pudo determinar el directorio de trabajo." "Ejecute el instalador desde un directorio con permisos de lectura y escritura."
}

$RequiredFiles = @('normalizador.py', 'requirements.txt')
$IsProjectRoot = $true
foreach ($file in $RequiredFiles) {
    if (-not (Test-Path (Join-Path $ScriptRoot $file))) {
        $IsProjectRoot = $false
        break
    }
}

if (-not $IsProjectRoot) {
    Show-Warn "Archivos de proyecto no encontrados en el directorio actual."
    Show-Info "Entrando a modo bootstrap remoto: descargando repositorio..."

    $RepoOwner = 'wilkinbarban'
    $RepoName = 'normalizador-audio'
    $Branch = 'main'
    $ArchiveUrl = "https://github.com/$RepoOwner/$RepoName/archive/refs/heads/$Branch.zip"
    $DesktopDir = [Environment]::GetFolderPath('Desktop')
    if ([string]::IsNullOrWhiteSpace($DesktopDir)) {
        $DesktopDir = Join-Path $HOME 'Desktop'
    }
    $InstallDir = if ($env:NORM_INSTALL_DIR) { $env:NORM_INSTALL_DIR } else { Join-Path $DesktopDir $RepoName }
    $TempZip = Join-Path $env:TEMP "$RepoName-$Branch.zip"
    $TempExtract = Join-Path $env:TEMP "$RepoName-bootstrap-$(Get-Random)"

    $downloadArgs = "-NoProfile -Command `"Invoke-WebRequest -Uri '$ArchiveUrl' -OutFile '$TempZip' -UseBasicParsing`""
    $downloadResult = Run-WithProgress "powershell" $downloadArgs "Descargando repositorio de GitHub"
    if (-not $downloadResult.Success) {
        Show-Error "Fallo de Descarga" "No se pudo descargar el repositorio desde GitHub." "Verifique su conexion a Internet y que github.com sea accesible."
    }

    $zipSize = (Get-Item $TempZip).Length
    if ($zipSize -lt 1024) {
        Remove-Item -Force $TempZip -ErrorAction SilentlyContinue
        Show-Error "Integridad Invalida" "El archivo descargado es invalido o corrupto (size: $zipSize bytes)." "Vuelva a intentar la ejecucion."
    }

    $null = New-Item -ItemType Directory -Path $TempExtract -Force
    $extractArgs = "-NoProfile -Command `"Expand-Archive -Path '$TempZip' -DestinationPath '$TempExtract' -Force`""
    $extractResult = Run-WithProgress "powershell" $extractArgs "Extrayendo repositorio del instalador"
    Remove-Item -Force $TempZip -ErrorAction SilentlyContinue

    if (-not $extractResult.Success) {
        Remove-Item -Recurse -Force $TempExtract -ErrorAction SilentlyContinue
        Show-Error "Extraccion Fallida" "No se pudo descomprimir el archivo del repositorio." "Asegurese de contar con espacio en disco y permisos de escritura."
    }

    $ExtractedRoot = Join-Path $TempExtract "$RepoName-$Branch"
    if (-not (Test-Path $ExtractedRoot)) {
        Remove-Item -Recurse -Force $TempExtract -ErrorAction SilentlyContinue
        Show-Error "Estructura Invalida" "La carpeta esperada tras la extraccion no existe." "Vuelva a intentar la ejecucion."
    }

    Show-Step "Instalando archivos del repositorio"
    if (Test-Path $InstallDir) {
        Show-Warn "Carpeta destino existente. Actualizando archivos en-lugar..."
        Get-ChildItem -Path $ExtractedRoot | Where-Object { $_.Name -ne '.venv' } | ForEach-Object {
            $destination = Join-Path $InstallDir $_.Name
            Copy-Item -Path $_.FullName -Destination $destination -Recurse -Force
        }
    } else {
        Move-Item -Path $ExtractedRoot -Destination $InstallDir
    }

    Remove-Item -Recurse -Force $TempExtract -ErrorAction SilentlyContinue

    $LocalInstaller = Join-Path $InstallDir 'install.ps1'
    if (-not (Test-Path $LocalInstaller)) {
        Show-Error "Script Faltante" "El script install.ps1 no se encontro en el directorio instalado." "Reporte este error al autor del proyecto."
    }

    Show-Ok "Repositorio instalado con exito."
    Show-Info "Delegando arranque al instalador local..."
    Set-Location $InstallDir
    & $LocalInstaller
    exit $LASTEXITCODE
}

Show-Step "Verificando entorno de Python"

$pythonCmd = $null
$pythonMinimum = $null
$pythonCandidates = @("python", "py", "py -3.14", "py -3.13", "py -3.12", "py -3.11", "py -3.10", "py -3.9", "py -3.8")

foreach ($candidate in $pythonCandidates) {
    $detectedVersion = Get-PythonMinorVersion -PythonCommand $candidate
    if ($detectedVersion) {
        $pythonCmd = $candidate
        $pythonMinimum = $detectedVersion
        break
    }
}

if (-not $pythonCmd) {
    Show-Warn "Python no detectado en el sistema."

    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Show-Error "Python No Encontrado" "No se encontro Python ni el instalador winget en el sistema." "Instale Python desde https://www.python.org/downloads/ marcando 'Add Python to PATH'."
    }

    $installResult = Run-WithProgress "winget" "install --id Python.Python.3.14 --accept-source-agreements --accept-package-agreements" "Instalando Python"
    if (-not $installResult.Success) {
        Show-Error "Instalacion de Python Fallida" "Fallo al instalar Python mediante winget." "Instale Python manualmente desde https://www.python.org/downloads/ y vuelva a ejecutar install.ps1."
    }

    Refresh-CurrentPath

    foreach ($candidate in $pythonCandidates) {
        $detectedVersion = Get-PythonMinorVersion -PythonCommand $candidate
        if ($detectedVersion) {
            $pythonCmd = $candidate
            $pythonMinimum = $detectedVersion
            break
        }
    }

    if (-not $pythonCmd) {
        Show-Error "Reinicio de Consola Requerido" "Python fue instalado, pero la terminal actual aun no reconoce el comando." "Cierre esta ventana, abra una nueva terminal y vuelva a ejecutar install.ps1."
    }
}

Show-Ok "Python base detectado ($pythonCmd). Piso local: >=$pythonMinimum"

Show-Step "Comprobando FFmpeg"
$ffmpegReady = $false
try {
    $null = & ffmpeg -version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $ffmpegReady = $true
    }
} catch { }

if (-not $ffmpegReady) {
    Show-Warn "FFmpeg no detectado en PATH."

    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Show-Error "FFmpeg No Encontrado" "No se encontro FFmpeg ni el instalador winget en el sistema." "Instale FFmpeg manualmente y asegurese de que ffmpeg.exe este en PATH."
    }

    $ffmpegResult = Run-WithProgress "winget" "install --id Gyan.FFmpeg --exact --source winget --accept-source-agreements --accept-package-agreements" "Instalando FFmpeg"
    if (-not $ffmpegResult.Success) {
        Show-Warn "Paquete principal de FFmpeg fallo. Probando paquete alternativo..."
        $ffmpegResult = Run-WithProgress "winget" "install --id FFmpeg.FFmpeg --exact --source winget --accept-source-agreements --accept-package-agreements" "Instalando FFmpeg alternativo"
    }

    if (-not $ffmpegResult.Success) {
        Show-Error "Instalacion de FFmpeg Fallida" "winget no pudo instalar FFmpeg." "Instale FFmpeg manualmente y asegurese de que ffmpeg.exe este en PATH."
    }

    Refresh-CurrentPath

    try {
        $null = & ffmpeg -version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $ffmpegReady = $true
        }
    } catch { }

    if (-not $ffmpegReady) {
        Show-Error "Reinicio de Consola Requerido" "FFmpeg fue instalado, pero la terminal actual aun no lo detecta." "Cierre esta ventana, abra una nueva terminal y vuelva a ejecutar install.ps1."
    }
}

Show-Ok "FFmpeg disponible"

$venvDir = Join-Path $ScriptRoot '.venv'
$venvPython = Join-Path $venvDir 'Scripts\python.exe'
$venvPip = Join-Path $venvDir 'Scripts\pip.exe'
$recreateVenv = $false

if (Test-Path $venvPython) {
    if (-not (Test-PythonMinimum -PythonPath $venvPython -MinimumVersion $pythonMinimum)) {
        $recreateVenv = $true
    }
}

if ($recreateVenv) {
    Show-Warn "Entorno virtual anterior a Python $pythonMinimum detectado. Recreando .venv..."
    Remove-Item -Path $venvDir -Recurse -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path $venvPython)) {
    $parts = $pythonCmd -split ' '
    $cmd = $parts[0]
    $venvArgs = if ($parts.Count -gt 1) { "$($parts[1]) -m venv `"$venvDir`"" } else { "-m venv `"$venvDir`"" }

    $venvResult = Run-WithProgress $cmd $venvArgs "Creando entorno virtual (.venv)"
    if (-not $venvResult.Success) {
        Show-Error "Error de Entorno Virtual" "No se pudo crear la carpeta .venv." "Verifique permisos de escritura o ejecute manualmente: python -m venv .venv"
    }
} else {
    Show-Ok "Entorno virtual detectado (.venv)"
}

Show-Step "Instalando dependencias de Python"
$env:PIP_USER = "no"

$pipUpgrade = Run-WithProgress $venvPython "-m pip install --no-input --upgrade pip" "Actualizando instalador pip"
if (-not $pipUpgrade.Success) {
    Show-Warn "No se pudo actualizar pip. Se intentara continuar con la version disponible."
}

$requirementsPath = Join-Path $ScriptRoot 'requirements.txt'
if (-not (Test-Path $requirementsPath)) {
    Show-Error "requirements.txt Faltante" "No se encontro el archivo requirements.txt." "Verifique que la descarga del repositorio este completa."
}

$depsResult = Run-WithProgress $venvPip "install --no-input -r `"$requirementsPath`"" "Instalando dependencias de Python"
if (-not $depsResult.Success) {
    $logFile = Join-Path $venvDir 'install.log'
    @(
        "STDOUT:",
        $depsResult.Stdout,
        "",
        "STDERR:",
        $depsResult.Stderr
    ) | Out-File -FilePath $logFile -Encoding utf8

    Show-Error "Error en Dependencias" "Fallo al instalar paquetes desde requirements.txt." "Consulte el log: $logFile`nIntente manualmente: .venv\Scripts\pip.exe install -r requirements.txt"
}

Write-Host ""
Write-Host "  >>> Iniciando Normalizador Audio..." -ForegroundColor Green
Write-Host ""

try {
    $entrypoint = Join-Path $ScriptRoot 'normalizador.py'
    $proc = Start-Process -FilePath $venvPython -ArgumentList "`"$entrypoint`"" -NoNewWindow -PassThru -Wait
    $exitCode = $proc.ExitCode
    if ($exitCode -ne 0) {
        Show-Error "Ejecucion Fallida" "La aplicacion finalizo con codigo de error $exitCode." "Revise la salida anterior o %LOCALAPPDATA%\NormalizadorAudio\normalizador_errors.log para mas detalles."
    }
} catch {
    Show-Error "Fallo Critico al Iniciar" $_.Exception.Message "Compruebe que el entorno virtual no este danado y vuelva a ejecutar install.ps1."
}
