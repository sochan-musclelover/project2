@echo off
REM コンテナの起動
cd ../..
docker-compose -f docker/docker-compose.yml up -d
pause
