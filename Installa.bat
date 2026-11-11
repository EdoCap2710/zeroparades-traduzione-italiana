@echo off
rem Traduzione italiana amatoriale di ZERO PARADES - avvio su Windows.
rem Doppio clic per installare. Questo file non scarica nulla: avvia soltanto installa.py.
setlocal
cd /d "%~dp0"
set "PY=py -3"
%PY% --version >nul 2>nul
if errorlevel 1 set "PY=python"
%PY% --version >nul 2>nul
if errorlevel 1 (
  echo Python 3 non trovato. Installalo da https://www.python.org/downloads/
  echo e nella prima schermata spunta "Add python.exe to PATH". Poi rilancia questo file.
  pause
  exit /b 1
)
%PY% -c "import UnityPy, lz4.block" >nul 2>nul
if errorlevel 1 (
  echo Manca la libreria UnityPy, che serve a leggere e riscrivere il file dei testi.
  echo Installala una volta sola: apri il Prompt dei comandi e scrivi
  echo.
  echo     %PY% -m pip install UnityPy==1.25.4
  echo.
  echo Poi rilancia Installa.bat.
  pause
  exit /b 1
)
%PY% installa.py %*
exit /b %errorlevel%
