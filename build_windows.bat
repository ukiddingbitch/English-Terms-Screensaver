@echo off
setlocal
cd /d "%~dp0"
py -3 -c "import tkinter" >nul 2>&1
if not errorlevel 1 (
  py -3 build_windows.py
) else (
  python build_windows.py
)
if errorlevel 1 (
  echo Build failed. See the error above.
  pause
  exit /b 1
)
echo Ready: dist\EnglishTermsScreensaver.scr
pause
