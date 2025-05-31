@echo off
REM Webコンテナに入る
cd ../..
echo === コンテナにログインします ===
docker exec -it sim_web /bin/bash
pause
