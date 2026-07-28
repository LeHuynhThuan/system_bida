@echo off
echo Dang khoi dong He Thong Bida AI...
cd /d "%~dp0"
start "Bida API Server" cmd /k "python run_server.py"
start "Bida AI Workers" cmd /k "python run_workers.py"
start "Cloudflare Tunnel" cmd /k "cloudflared.exe tunnel --url http://127.0.0.1:8888"
echo He thong da chay thanh cong!
