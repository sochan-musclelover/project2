@echo off
cd /d %~dp0\..

REM dbサービスのコンテナIDを取得
for /f %%i in ('docker compose ps -q db') do set CONTAINER_ID=%%i

if "%CONTAINER_ID%"=="" (
    echo [ERROR] db コンテナが見つかりません。
    pause
    exit /b
)

echo === PostgreSQL コンテナ (%CONTAINER_ID%) にログインします ===
cd ../..
docker exec -it sim_web psql -U simuser -d simulation_db
pause
