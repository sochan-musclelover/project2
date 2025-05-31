@echo off
REM ログイン用バッチ
cd /d %~dp0..
docker compose exec web bash
