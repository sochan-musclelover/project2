@echo off
REM Dockerイメージのビルド
cd ../..
docker-compose -f docker/docker-compose.yml build
