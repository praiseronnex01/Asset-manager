@echo off
title Asset Manager Local Server
echo ==================================================
echo   Starting Asset Manager Server...
echo ==================================================
echo Workspace: %~dp0
echo Server URL: http://127.0.0.1:5000
echo.
python "%~dp0run.py"
if %ERRORLEVEL% NEQ 0 (
    py "%~dp0run.py"
)
pause
