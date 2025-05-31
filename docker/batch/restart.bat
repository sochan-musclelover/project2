@echo off
REM 再起動用バッチ
cd /d %~dp0..
docker compose restart
pause
