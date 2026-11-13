# PowerShell Setup Script for Flask Asset Management App
# Run with: powershell -ExecutionPolicy Bypass -File setup_and_run.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Flask Asset Management Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUTION: Install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "During installation, make sure to check: 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter after installing Python and adding it to PATH"
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists, skipping creation"
} else {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✓ Virtual environment ready" -ForegroundColor Green

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".\.venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host ""
Write-Host "Installing Python packages..." -ForegroundColor Cyan
Write-Host "This may take a minute..." -ForegroundColor Gray
pip install Flask==3.1.1 Flask-Bcrypt==1.0.1 Flask-MySQLdb==2.0.0 Flask-Cors==4.0.0 python-dateutil==2.9.0 Werkzeug==3.1.3

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install packages" -ForegroundColor Red
    exit 1
}
Write-Host "✓ All packages installed successfully" -ForegroundColor Green

# Run the Flask app
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Starting Flask application..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Flask app will be running at: http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

Set-Location "perpex"
python app.py

Read-Host "Press Enter to exit"
