@powershell -NoProfile -ExecutionPolicy Bypass -Command "$ScriptRoot = '%~dp0'; Invoke-Expression ((Get-Content '%~f0' -Encoding utf8 | Select-Object -Skip 1) -join [Environment]::NewLine)" & exit /b
# Normalizador Audio local launcher. PowerShell starts after the BAT line.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$Version = "1.1.0"
$Host.UI.RawUI.WindowTitle = "Normalizador Audio - Iniciando..."
Clear-Host

Write-Host ""
Write-Host "  *** N O R M A L I Z A D O R   A U D I O ***" -ForegroundColor Green
Write-Host "  ===========================================" -ForegroundColor DarkCyan
Write-Host "   Lanzador Local - Version $Version" -ForegroundColor Gray
Write-Host "  ===========================================" -ForegroundColor DarkCyan
Write-Host ""

function Show-Step {
    param([string]$Message)
    Write-Host "  >> $Message..." -ForegroundColor Gray
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

if ([string]::IsNullOrWhiteSpace($ScriptRoot)) {
    Show-Error "Error de Directorio" "No se pudo determinar el directorio del lanzador." "Ejecute Iniciar.bat desde la carpeta del proyecto."
}

Set-Location $ScriptRoot
$ProjectRoot = (Get-Location).Path
$RequiredFiles = @('normalizador.py', 'requirements.txt')
foreach ($file in $RequiredFiles) {
    if (-not (Test-Path (Join-Path $ProjectRoot $file))) {
        Show-Error "Proyecto Incompleto" "No se encontro $file en $ProjectRoot." "Descargue el proyecto completo o ejecute install.ps1."
    }
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
    Write-Host "  [!] Python no detectado en el sistema." -ForegroundColor Yellow
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Show-Error "Python No Encontrado" "No se encontro Python ni winget." "Instale Python desde https://www.python.org/downloads/ y agreguelo al PATH."
    }

    $installRes = Run-WithProgress "winget" "install --id Python.Python.3.14 --accept-source-agreements --accept-package-agreements" "Instalando Python"
    if (-not $installRes.Success) {
        Show-Error "Instalacion de Python Fallida" "Fallo al instalar Python mediante winget." "Instale Python manualmente desde el sitio web de Python."
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
        Show-Error "Reinicio de Consola Requerido" "Python fue instalado, pero esta terminal aun no reconoce el comando." "Cierre todas las consolas y vuelva a ejecutar Iniciar.bat."
    }
}

Write-Host "  [OK] Python base detectado ($pythonCmd). Piso local: >=$pythonMinimum" -ForegroundColor Green

Show-Step "Verificando FFmpeg"
$ffmpegReady = $false
try {
    $null = & ffmpeg -version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $ffmpegReady = $true
    }
} catch { }

if (-not $ffmpegReady) {
    Write-Host "  [!] FFmpeg no detectado en PATH." -ForegroundColor Yellow
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Show-Error "FFmpeg No Encontrado" "No se encontro FFmpeg ni winget." "Instale FFmpeg manualmente y asegurese de que ffmpeg.exe este en PATH."
    }

    $ffmpegRes = Run-WithProgress "winget" "install --id Gyan.FFmpeg --exact --source winget --accept-source-agreements --accept-package-agreements" "Instalando FFmpeg"
    if (-not $ffmpegRes.Success) {
        $ffmpegRes = Run-WithProgress "winget" "install --id FFmpeg.FFmpeg --exact --source winget --accept-source-agreements --accept-package-agreements" "Instalando FFmpeg alternativo"
    }

    if (-not $ffmpegRes.Success) {
        Show-Error "Instalacion de FFmpeg Fallida" "winget no pudo instalar FFmpeg." "Instale FFmpeg manualmente y vuelva a ejecutar Iniciar.bat."
    }

    Refresh-CurrentPath
}

$venvDir = Join-Path $ProjectRoot '.venv'
$venvPython = Join-Path $venvDir 'Scripts\python.exe'
$venvPip = Join-Path $venvDir 'Scripts\pip.exe'
$recreateVenv = $false

if (Test-Path $venvPython) {
    if (-not (Test-PythonMinimum -PythonPath $venvPython -MinimumVersion $pythonMinimum)) {
        $recreateVenv = $true
    }
}

if ($recreateVenv) {
    Write-Host "  [!] Entorno virtual anterior a Python $pythonMinimum detectado. Recreando .venv..." -ForegroundColor Yellow
    Remove-Item -Path $venvDir -Recurse -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path $venvPython)) {
    $parts = $pythonCmd -split ' '
    $cmd = $parts[0]
    $venvArgs = if ($parts.Count -gt 1) { "$($parts[1]) -m venv `"$venvDir`"" } else { "-m venv `"$venvDir`"" }

    $venvRes = Run-WithProgress $cmd $venvArgs "Creando entorno virtual (.venv)"
    if (-not $venvRes.Success) {
        Show-Error "Error de Entorno Virtual" "No se pudo crear la carpeta .venv." "Verifique permisos o ejecute: python -m venv .venv"
    }
} else {
    Write-Host "  [OK] Entorno virtual detectado (.venv)" -ForegroundColor Green
}

Show-Step "Instalando dependencias"
$env:PIP_USER = "no"
$pipUpgrade = Run-WithProgress $venvPython "-m pip install --no-input --upgrade pip" "Actualizando instalador pip"
if (-not $pipUpgrade.Success) {
    Show-Error "Error de pip" "No se pudo actualizar pip dentro del entorno virtual." "Revise la conexion o ejecute: .venv\Scripts\python.exe -m pip install --upgrade pip"
}

$ReqPath = Join-Path $ProjectRoot "requirements.txt"
$depsRes = Run-WithProgress $venvPip "install --no-input -r `"$ReqPath`"" "Instalando dependencias de Python"
if (-not $depsRes.Success) {
    $logFile = Join-Path $venvDir "install.log"
    ($depsRes.Stdout + "`n" + $depsRes.Stderr) | Out-File -FilePath $logFile -Encoding utf8
    Show-Error "Error en Dependencias" "Fallo al instalar paquetes de requirements.txt." "Consulte el log: $logFile`nIntente manualmente: .venv\Scripts\pip.exe install -r requirements.txt"
}

Write-Host ""
Write-Host "  >>> Iniciando Normalizador Audio..." -ForegroundColor Green
Write-Host ""

try {
    $entrypoint = Join-Path $ProjectRoot "normalizador.py"
    $proc = Start-Process -FilePath $venvPython -ArgumentList "`"$entrypoint`"" -NoNewWindow -PassThru -Wait
    $exitCode = $proc.ExitCode
    if ($exitCode -ne 0) {
        Show-Error "Ejecucion Fallida" "La aplicacion finalizo con codigo de error ($exitCode)." "Consulte los mensajes anteriores o los logs de la aplicacion."
    }
} catch {
    Show-Error "Fallo Critico al Iniciar" $_.Exception.Message "Compruebe que .venv no este danado y vuelva a ejecutar Iniciar.bat."
}
