@echo off
title Inicializando do Receita Facil...

echo ==========================================
echo Iniciando os servicos da aplicacao:
echo - PostgreSQL
echo - FastAPI
echo ==========================================
echo.

REM 
docker --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERRO] Docker não esta instalado ou nao esta no PATH.
    pause
    exit /b
)

REM 
echo [INFO] Construindo e iniciando os containers com docker-compose...
docker-compose up --build -d

IF ERRORLEVEL 1 (
    echo [ERRO] Falha ao iniciar os containers.
    pause
    exit /b
)

echo.
echo [OK] Servicos iniciados com sucesso!
echo Voce pode acessar em: http://localhost:8070/home
echo.

pause
