# ==================================================
#   Asset Manager — PowerShell Server Launcher
# ==================================================

$Host.UI.RawUI.WindowTitle = "Asset Manager Local Server"

Write-Host ""
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host "    🚀 ASSET MANAGER — Local Web Server          " -ForegroundColor Yellow
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host ""

$WorkspaceDir = $PSScriptRoot
if (-not $WorkspaceDir) {
    $WorkspaceDir = Get-Location
}

Write-Host "📍 Working Directory : $WorkspaceDir" -ForegroundColor Gray
Write-Host "🌐 Server URL       : http://127.0.0.1:5000" -ForegroundColor Green
Write-Host ""

# Set Environment Variables
$env:FLASK_APP = "app.py"
$env:FLASK_DEBUG = "1"

# Check Python availability
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "▶ Starting Flask server using 'python run.py'..." -ForegroundColor Cyan
    python "$WorkspaceDir\run.py"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    Write-Host "▶ Starting Flask server using 'py run.py'..." -ForegroundColor Cyan
    py "$WorkspaceDir\run.py"
} else {
    Write-Host "❌ Error: Python is not installed or not found in system PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.9+ or add Python to PATH and try again." -ForegroundColor Yellow
}
