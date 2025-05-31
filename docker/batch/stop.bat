@echo off
REM コンテナの停止
cd ../..
docker-compose -f docker/docker-compose.yml down
