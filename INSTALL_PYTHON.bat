@echo off
REM PINACO Smart Advisor - Python Installation Helper
REM This script helps install Python on Windows

title PINACO Smart Advisor - Python Setup
color 0F
cls

echo.
echo ============================================================
echo     PINACO Smart Advisor - Python Installation Helper
echo ============================================================
echo.
echo Your system does not have Python installed.
echo.
echo This script will download and install Python 3.11
echo.

REM Check if .NET/Windows is recent enough
echo Checking system compatibility...

REM Offer manual download option
echo.
echo ============================================================
echo OPTION 1: Download Python Yourself (Manual)
echo ============================================================
echo.
echo 1. Go to: https://www.python.org/downloads/
echo 2. Click "Download Python 3.11" (or latest 3.x)
echo 3. Run the installer
echo 4. IMPORTANT: Check "Add Python to PATH" during setup
echo 5. Click "Install Now"
echo 6. After installation, run START_APP.bat again
echo.

REM Try to open browser
echo Attempting to open python.org in your browser...
timeout /t 2 /nobreak

REM Use powershell to open browser
powershell -Command "Start-Process 'https://www.python.org/downloads/' -ErrorAction SilentlyContinue" 2>nul

echo.
echo ============================================================
echo OPTION 2: Use installer from Microsoft Store
echo ============================================================
echo.
echo 1. Open Microsoft Store
echo 2. Search for "Python"
echo 3. Click "Get" or "Install"
echo 4. Wait for installation to complete
echo 5. Run START_APP.bat again
echo.

echo.
echo ============================================================
echo After installing Python:
echo ============================================================
echo 1. Open Command Prompt or PowerShell
echo 2. Run:  python --version
echo    (Should show Python 3.x.x)
echo 3. Then run: START_APP.bat
echo.

pause
