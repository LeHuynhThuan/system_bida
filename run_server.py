import uvicorn
import sys
import io

# Force stdout/stderr to UTF-8 on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

if __name__ == "__main__":
    print("=== KHOI DONG BIDA API SERVER (DUAL STACK IPv4 + IPv6) ===")
    # host=None giúp Uvicorn tự động lắng nghe trên cả 0.0.0.0 (IPv4) và [::] (IPv6)
    uvicorn.run(
        "main:app",
        host=None,
        port=8888,
        reload=False,
        workers=1,                 # Single worker (multi-worker khong tuong thich voi WebSocket/in-memory state)
        timeout_keep_alive=30,     # Keep-alive timeout 30s
        timeout_graceful_shutdown=10,
        loop="asyncio"
    )
