import os
import json
import csv
import io
import time
import re
import math
from datetime import datetime
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
import redis as redis_lib
from database.database import SessionLocal
from database.models import BilliardTable, PlaySession, SessionOrderItem, Product
from api.websocket_server import websocket_manager

# Token generator helper
import hashlib
SECRET_KEY = "BIDA_AI_SECURE_KEY_2026"
def generate_table_token(table_id: int) -> str:
    return hashlib.md5(f"{SECRET_KEY}_{table_id}".encode()).hexdigest()[:8]

CLIPS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "clips")
client_messages_store = {}

router = APIRouter(prefix="/api", tags=["Reports & Media"])

@router.get("/reports/revenue")
async def get_revenue_report(start_date: str = None, end_date: str = None):
    db = SessionLocal()
    try:
        query = db.query(PlaySession).filter(PlaySession.status == "COMPLETED")
        
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                query = query.filter(PlaySession.start_time >= start_dt)
            except ValueError:
                pass
                
        if end_date:
            try:
                end_dt = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
                query = query.filter(PlaySession.start_time <= end_dt)
            except ValueError:
                pass
                
        sessions = query.order_by(PlaySession.start_time.desc()).all()
        
        output = io.StringIO()
        output.write('\ufeff')
        
        writer = csv.writer(output, delimiter=';')
        writer.writerow(["Mã Hóa Đơn", "Tên Bàn", "Giờ Vào", "Giờ Ra", "Tổng Thời Gian (phút)", "Tiền Giờ (VNĐ)", "Tiền Dịch Vụ (VNĐ)", "Tổng Cộng (VNĐ)"])
        
        for session in sessions:
            table = db.query(BilliardTable).filter(BilliardTable.id == session.table_id).first()
            table_name = table.name if table else f"Bàn {session.table_id}"
            
            service_total = sum([item.total_price for item in session.order_items])
            total_bill = (session.play_fee or 0) + service_total
            
            start_time_str = session.start_time.strftime("%Y-%m-%d %H:%M:%S") if session.start_time else ""
            end_time_str = session.end_time.strftime("%Y-%m-%d %H:%M:%S") if session.end_time else ""
            
            writer.writerow([
                f"HD{session.id}", 
                table_name,
                start_time_str,
                end_time_str,
                int(session.total_minutes or 0),
                int(session.play_fee or 0),
                int(service_total or 0),
                int(total_bill or 0)
            ])
            
        output.seek(0)
        
        filename = f"bao_cao_doanh_thu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers=headers)
    finally:
        db.close()

@router.post("/clip/{table_id}")
async def trigger_clip(table_id: int):
    try:
        r = redis_lib.Redis(host='127.0.0.1', port=6379, db=0, socket_timeout=0.2, socket_connect_timeout=0.2)
        payload = json.dumps({"command": "save_clip", "table_id": table_id, "timestamp": time.time()})
        r.publish('bida_commands', payload)
        return JSONResponse({"status": "ok", "message": f"Da phat lenh trich xuat highlight cho ban {table_id}"})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@router.get("/clip-status/{table_id}")
async def get_clip_status(table_id: int):
    try:
        r = redis_lib.Redis(host='127.0.0.1', port=6379, db=0, socket_timeout=0.2, socket_connect_timeout=0.2)
        val = r.get(f"clip_status_table_{table_id}")
        if val:
            return JSONResponse(json.loads(val.decode('utf-8')))
    except Exception:
        pass
    return JSONResponse({"status": "idle"})

@router.post("/highlight-past/{table_id}")
async def trigger_past_highlight(table_id: int, payload: dict = None):
    seconds = 60
    if payload and "seconds" in payload:
        seconds = int(payload["seconds"])
    try:
        r = redis_lib.Redis(host='127.0.0.1', port=6379, db=0, socket_timeout=0.2, socket_connect_timeout=0.2)
        cmd_data = {
            "command": "save_past_highlight",
            "table_id": table_id,
            "seconds": seconds,
            "timestamp": time.time()
        }
        r.publish('bida_commands', json.dumps(cmd_data))
        return JSONResponse({"status": "ok", "message": f"Da gui lenh lay highlight {seconds}s qua cho ban {table_id}"})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@router.delete("/clip/{filename}")
async def delete_clip(filename: str):
    filepath = os.path.join(CLIPS_DIR, filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            return JSONResponse({"status": "ok", "message": f"Da xoa {filename}"})
        except Exception as e:
            return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
    return JSONResponse({"status": "error", "message": "File khong ton tai"}, status_code=404)

@router.get("/live/{table_id}")
async def get_live_frame(table_id: int):
    live_file = os.path.join(CLIPS_DIR, f"live_{table_id}.jpg")
    if os.path.exists(live_file):
        return FileResponse(live_file, media_type="image/jpeg", headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return Response(status_code=404)

@router.get("/clips")
async def list_clips():
    clips = []
    if os.path.exists(CLIPS_DIR):
        for f in sorted(os.listdir(CLIPS_DIR), reverse=True):
            if f.endswith(".mp4"):
                filepath = os.path.join(CLIPS_DIR, f)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                clips.append({"filename": f, "url": f"/clips/{f}", "size_mb": round(size_mb, 2)})
    return JSONResponse(clips)
