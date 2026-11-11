@echo off
rem Rimette i file originali del gioco dal backup creato dall'installer.
cd /d "%~dp0"
call Installa.bat --ripristina %*
