@echo off
echo Dang khoi dong He Thong Bida AI...
cd /d "%~dp0"
start "Bida API Server" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 8888 --reload"
start "Bida AI Workers" cmd /k "python run_workers.py"
start "Cloudflare Tunnel" cmd /k "cloudflared.exe tunnel --url http://localhost:8888"
echo He thong da chay thanh cong!
