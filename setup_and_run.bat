@echo off
REM Setup script for Flask Asset Management App
REM This script will install Python, create a virtual environment, install dependencies, and run the app

echo ==========================================
echo Flask Asset Management Setup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo.
    echo SOLUTION: Install Python from https://www.python.org/downloads/
    echo During installation, check "Add Python to PATH"
    echo.
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

echo ✓ Python found
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo Installing Python packages...
pip install --upgrade pip
pip install Flask==3.1.1 Flask-Bcrypt==1.0.1 Flask-MySQLdb==2.0.0 Flask-Cors==4.0.0 python-dateutil==2.9.0 Werkzeug==3.1.3

if %errorlevel% neq 0 (
    echo Failed to install packages
    pause
    exit /b 1
)
echo ✓ All packages installed successfully
echo.

REM Run the Flask app
echo Starting Flask application...
echo.
echo ==========================================
echo Flask app is running at: http://localhost:5000
echo ==========================================
echo.
echo Press Ctrl+C to stop the server
echo.

cd perpex
python app.py

pause
