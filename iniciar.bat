@echo off
title CopyMart ERP - Iniciador
color 0A

echo.
echo ========================================
echo    CopyMart ERP - Sistema Integrado
echo ========================================
echo.

cd /d "%~dp0"

echo [*] Verificando directorios...
if not exist "app" (
    echo [ERROR] No se encuentra el directorio del backend
    pause
    exit /b 1
)

if not exist "copy-mart" (
    echo [ERROR] No se encuentra el directorio del frontend
    pause
    exit /b 1
)

echo [OK] Directorios verificados
echo.

echo [*] Iniciando Backend (FastAPI)...
start "CopyMart Backend" cmd /k "cd /d %~dp0 && uvicorn app.main:app --reload"

timeout /t 3 /nobreak >nul

echo [*] Iniciando Frontend (Vue.js)...
start "CopyMart Frontend" cmd /k "cd /d %~dp0\copy-mart && npm run dev"

echo.
echo ========================================
echo    Aplicacion iniciada correctamente
echo ========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo.
echo Presiona cualquier tecla para cerrar este mensaje...
pause >nul
