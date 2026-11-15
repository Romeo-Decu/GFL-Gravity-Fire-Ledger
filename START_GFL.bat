@echo off
rem Gravity Fire Ledger: starts the dashboard on this computer. Needs Python 3.10 or later. Nothing is installed.
cd /d "%~dp0"
set PY=python
where python >nul 2>nul || set PY=py -3
%PY% --version >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.10 or later from https://www.python.org/downloads/ and run this file again.
  pause
  exit /b 1
)
echo Gravity Fire Ledger is starting at http://localhost:8137/visualization/gfl.html
echo Keep this window open while you use the page. Close it to stop.
start "" "http://localhost:8137/visualization/gfl.html"
%PY% -m http.server 8137 --bind 127.0.0.1
pause
