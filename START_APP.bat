@echo off
REM Quick Start - Double-click to setup and run Flask app

cd /d "%~dp0"

REM Check Python installation
python --version > nul 2>&1
if errorlevel 1 (
	title Python Not Found
	color 0C
	echo.
	echo ============================================
	echo ERROR: Python is not installed or not in PATH
	echo ============================================
	echo.
	echo Please install Python first:
	echo https://www.python.org/downloads/
	echo.
	echo During installation, MUST CHECK:
	echo "Add Python to PATH"
	echo.
	echo After installation, run this file again.
	echo.
	pause
	exit /b 1
)

REM Check if .venv exists, create if not
if not exist ".venv" (
	echo Creating virtual environment...
	python -m venv .venv
	if errorlevel 1 (
		echo ERROR: Failed to create virtual environment
		pause
		exit /b 1
	)
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install/Update packages
echo Installing required packages...
pip install --quiet --upgrade pip
pip install --quiet Flask==3.1.1 Werkzeug==3.1.3 Flask-Bcrypt==1.0.1 Flask-MySQLdb==2.0.0 Flask-Cors==4.0.0 python-dateutil==2.9.0

if errorlevel 1 (
	echo.
	echo ERROR: Failed to install packages
	echo Make sure MySQL development libraries are installed
	pause
	exit /b 1
)

REM Change to app directory and run
cd perpex
title Flask Asset Management - Running on http://localhost:5000
echo.
echo ============================================
echo Flask app is starting...
echo ============================================
echo.
echo Open your browser and go to:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

python app.py

pause
