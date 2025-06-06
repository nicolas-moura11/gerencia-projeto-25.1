@echo off
echo Iniciando os servicos da aplicacao (PostgreSQL e FastAPI)...
echo.

REM 
docker-compose up --build -d

pause