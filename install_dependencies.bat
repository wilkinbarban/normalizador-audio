@echo off
setlocal enabledelayedexpansion
title Dependency Installer - Normalizador Audio
color 0A

cd /d "%~dp0"

echo ===================================================
echo   Installing dependencies for Normalizador Audio...
echo ===================================================
echo.

:CHECK_PYTHON
python --version >nul 2>&1
if %errorlevel% equ 0 goto PY_OK

color 0E
echo [INFO] Python was not found on this system.
echo Trying to install Python automatically using winget...
echo.

winget install --id Python.Python.3.11 -e --source winget --accept-package-agreements --accept-source-agreements
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python could not be installed automatically.
    echo Please install Python manually from https://python.org and make sure it is added to PATH.
    echo.
    pause
    exit /b 1
)

echo [INFO] Python installed (winget reported success). Trying to locate python.exe...
echo.

where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] python found via where.
    goto PY_OK
)

set "PY_PATH="
for %%D in ("%LOCALAPPDATA%\Programs\Python\*" "%ProgramFiles%\Python*" "%ProgramFiles(x86)%\Python*") do (
    for /d %%P in (%%~D) do (
        if exist "%%P\python.exe" (
            set "PY_PATH=%%P"
            goto :FOUND_PY_PATH
        )
    )
)

:FOUND_PY_PATH
if defined PY_PATH (
    echo [INFO] python.exe found at: "!PY_PATH!\python.exe"
    echo [INFO] Adding folder to PATH for the current session...
    set "PATH=!PY_PATH!;!PATH!"
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [INFO] Python is available in the current session.
        goto PY_OK
    )
)

color 0E
echo.
echo [INFO] Python appears to be installed but is not available in this console.
echo Close this terminal window, open a new one and run install_dependencies.bat again.
echo.
pause
exit /b 1

:PY_OK
color 0A
echo [INFO] Python detected:
python --version
echo.

:CHECK_FFMPEG
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 goto FFMPEG_OK

color 0E
echo [INFO] FFmpeg was not found on this system.
echo Trying to install FFmpeg automatically using winget...
echo.

winget install --id Gyan.FFmpeg -e --source winget --accept-package-agreements --accept-source-agreements
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] FFmpeg could not be installed automatically.
    echo Install FFmpeg manually and ensure ffmpeg.exe is in PATH.
    echo.
    pause
    exit /b 1
)

echo [INFO] FFmpeg installed (winget reported success). Refreshing PATH for this session...
set "PATH=%PATH%;%ProgramFiles%\FFmpeg\bin;%ProgramFiles(x86)%\FFmpeg\bin;%LOCALAPPDATA%\Microsoft\WinGet\Links"

ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo [INFO] FFmpeg appears installed but is not available in this console yet.
    echo Close this terminal window, open a new one and run install_dependencies.bat again.
    echo.
    pause
    exit /b 1
)

:FFMPEG_OK
color 0A
echo [INFO] FFmpeg detected:
ffmpeg -version | findstr /r /c:"^ffmpeg version"
echo.

echo [INFO] Updating pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Failed to update pip. Check your Python installation.
    pause
    exit /b 1
)

echo [INFO] Installing packages from requirements.txt...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ===================================================
    echo   [ERROR] There was a problem during installation.
    echo   Check the messages above for more details.
    echo ===================================================
    echo.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo   Installation completed successfully!
echo   Launching normalizador.py...
echo ===================================================

start "" python normalizador.py

if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] The program could not be launched automatically.
    echo Please run: python normalizador.py
)

echo.
pause
endlocal
exit /b 0
