@echo off
setlocal
cd /d "%~dp0"
if exist "EnglishTermsScreensaver.scr" (
  start "" "%~dp0EnglishTermsScreensaver.scr" /s
  exit /b
)
py -3 -c "import tkinter" >nul 2>&1
if not errorlevel 1 (
  py -3 "%~dp0screensaver.py" /s
  if errorlevel 1 pause
  exit /b
)
python -c "import tkinter" >nul 2>&1
if not errorlevel 1 (
  python "%~dp0screensaver.py" /s
  if errorlevel 1 pause
  exit /b
)
echo Python with Tkinter was not found.
echo Install Python 3.10+ from https://www.python.org/downloads/
echo Enable 'Add Python to PATH', or use the standalone .scr release.
pause
exit /b 1
