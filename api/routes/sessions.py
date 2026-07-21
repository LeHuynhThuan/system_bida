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

router = APIRouter(prefix="/api", tags=["Sessions & Orders"])

@router.post("/customer-order/{table_id}/{token}")
async def customer_order(table_id: int, token: str, payload: dict):
    if token != generate_table_token(table_id):
        return JSONResponse({"status": "error", "message": "Mã xác thực không hợp lệ. Vui lòng quét lại QR!"}, status_code=403)
        
    items = payload.get("items", [])
    note = payload.get("note", "").strip()
    phone = payload.get("customer_phone", payload.get("phone", "")).strip()
    customer_name = payload.get("customer_name", "").strip()
    
    if not items:
        return JSONResponse({"status": "error", "message": "Giỏ hàng trống"}, status_code=400)
        
    if phone and not re.match(r"^(0|\+84|84)[35789]\d{8}$", phone):
        return JSONResponse({"status": "error", "message": "Số điện thoại Việt Nam không hợp lệ (hỗ trợ định dạng 09..., 84..., +84...)!"}, status_code=400)
        
    db = SessionLocal()
    try:
        table = db.query(BilliardTable).filter(BilliardTable.id == table_id).first()
        if not table:
            return JSONResponse({"status": "error", "message": "Bàn không tồn tại"}, status_code=404)
        if table.current_status != "PLAYING":
            return JSONResponse({"status": "error", "message": "Bàn chưa được bắt đầu tính giờ chơi. Vui lòng báo nhân viên bật bàn trước!"}, status_code=400)
            
        active_session = db.query(PlaySession).filter(
            PlaySession.table_id == table_id,
            PlaySession.status == "ACTIVE"
        ).first()
        if not active_session:
            return JSONResponse({"status": "error", "message": "Bàn chưa được bật chơi. Vui lòng báo nhân viên bật bàn trước!"}, status_code=400)
            
        normalized_items = []
        for item in items:
            item_name = item.get("item_name", item.get("name", "")).strip()
            quantity = int(item.get("quantity", item.get("qty", 1)))
            price = float(item.get("price", 0))
            item_note = item.get("note", "").strip()
            
            if not item_name or quantity <= 0:
                continue
                
            product = db.query(Product).filter(Product.name == item_name).first()
            if product:
                product.stock -= quantity
                if product.stock < 0: product.stock = 0

            existing_item = db.query(SessionOrderItem).filter(
                SessionOrderItem.session_id == active_session.id,
                SessionOrderItem.item_name == item_name
            ).first()
            
            if existing_item:
                existing_item.quantity += quantity
                existing_item.total_price = existing_item.quantity * existing_item.price
            else:
                new_item = SessionOrderItem(
                    session_id=active_session.id,
                    product_id=product.id if product else None,
                    item_name=item_name,
                    quantity=quantity,
                    price=price,
                    total_price=quantity * price
                )
                db.add(new_item)
                
            normalized_items.append({
                "item_name": item_name,
                "name": item_name,
                "quantity": quantity,
                "qty": quantity,
                "price": price,
                "total_price": quantity * price,
                "note": item_note
            })
            
        db.commit()

        name_label = f" ({customer_name})" if customer_name else ""
        has_paid_item = any(it.get("price", 0) > 0 for it in normalized_items)
        message_text = f"Khách {table.name}{name_label} vừa gọi đồ..." if has_paid_item else f"Khách {table.name}{name_label} đã yêu cầu:"

        event_data = {
            "id": f"evt_{time.time()}",
            "table_id": table_id,
            "event_type": "CUSTOMER_ORDER",
            "message": message_text,
            "customer_phone": phone,
            "customer_name": customer_name,
            "note": note,
            "items": normalized_items
        }
        
        try:
            await websocket_manager.broadcast(json.dumps(event_data))
        except Exception:
            pass

        return JSONResponse({"status": "ok", "message": "Gửi yêu cầu thành công!", "items": normalized_items})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
    finally:
        db.close()

@router.post("/session/start/{table_id}")
async def start_session(table_id: int):
    db = SessionLocal()
    try:
        table = db.query(BilliardTable).filter(BilliardTable.id == table_id).first()
        if not table:
            return JSONResponse({"status": "error", "message": "Khong tim thay ban"}, status_code=404)
        if table.current_status == "PLAYING":
            return JSONResponse({"status": "error", "message": "Ban dang choi roi"}, status_code=400)
            
        table.current_status = "PLAYING"
        new_session = PlaySession(table_id=table_id)
        db.add(new_session)
        db.commit()
        return JSONResponse({"status": "ok", "message": "Da bat dau tinh gio ban", "session_id": new_session.id})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
    finally:
        db.close()

@router.post("/session/add-item/{table_id}")
async def add_item_to_session(table_id: int, payload: dict):
    item_name = payload.get("item_name", "").strip()
    quantity = int(payload.get("quantity", 1))
    price = float(payload.get("price", 0))
    
    if not item_name or quantity <= 0 or price < 0:
        return JSONResponse({"status": "error", "message": "Du lieu mon an khong hop le"}, status_code=400)
        
    db = SessionLocal()
    try:
        active_session = db.query(PlaySession).filter(
            PlaySession.table_id == table_id,
            PlaySession.status == "ACTIVE"
        ).first()
        
        if not active_session:
            return JSONResponse({"status": "error", "message": "Ban chua duoc bat tinh gio"}, status_code=400)
            
        existing_item = db.query(SessionOrderItem).filter(
            SessionOrderItem.session_id == active_session.id,
            SessionOrderItem.item_name == item_name
        ).first()
        
        if existing_item:
            existing_item.quantity += quantity
            existing_item.total_price = existing_item.quantity * existing_item.price
        else:
            new_item = SessionOrderItem(
                session_id=active_session.id,
                item_name=item_name,
                quantity=quantity,
                price=price,
                total_price=quantity * price
            )
            db.add(new_item)
            
        db.commit()
        return JSONResponse({"status": "ok", "message": f"Da them mon vao ban"})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
    finally:
        db.close()

@router.post("/session/add-items/{table_id}")
async def add_items_to_session(table_id: int, payload: dict):
    items = payload.get("items", [])
    
    if not items or len(items) == 0:
        return JSONResponse({"status": "error", "message": "Giỏ hàng trống!"}, status_code=400)
        
    db = SessionLocal()
    try:
        table = db.query(BilliardTable).filter(BilliardTable.id == table_id).first()
        if not table:
            return JSONResponse({"status": "error", "message": "Không tìm thấy bàn!"}, status_code=404)
            
        active_session = db.query(PlaySession).filter(
            PlaySession.table_id == table_id,
            PlaySession.status == "ACTIVE"
        ).first()
        
        if not active_session:
            return JSONResponse({"status": "error", "message": "Bàn chưa được bắt đầu tính giờ chơi!"}, status_code=400)
            
        added_count = 0
        for item in items:
            item_name = item.get("item_name", item.get("name", "")).strip()
            quantity = int(item.get("quantity", item.get("qty", 1)))
            price = float(item.get("price", 0))
            
            if not item_name or quantity <= 0 or price < 0:
                continue
                
            product = db.query(Product).filter(Product.name == item_name).first()
            if product:
                product.stock -= quantity
                if product.stock < 0: product.stock = 0

            existing_item = db.query(SessionOrderItem).filter(
                SessionOrderItem.session_id == active_session.id,
                SessionOrderItem.item_name == item_name
            ).first()
            
            if existing_item:
                existing_item.quantity += quantity
                existing_item.total_price = existing_item.quantity * existing_item.price
            else:
                new_item = SessionOrderItem(
                    session_id=active_session.id,
                    product_id=product.id if product else None,
                    item_name=item_name,
                    quantity=quantity,
                    price=price,
                    total_price=quantity * price
                )
                db.add(new_item)
            added_count += 1
                
        db.commit()

        event_data = {
            "id": f"evt_{time.time()}",
            "table_id": table_id,
            "event_type": "CUSTOMER_ORDER",
            "message": f"Thu ngân đã thêm {added_count} món vào hóa đơn {table.name}!",
            "items": items
        }
        try:
            await websocket_manager.broadcast(json.dumps(event_data))
        except Exception:
            pass

        return JSONResponse({"status": "ok", "message": f"Đã thêm {added_count} món vào hóa đơn {table.name}!"})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
    finally:
        db.close()

@router.post("/session/stop/{table_id}")
async def stop_session(table_id: int):
    db = SessionLocal()
    try:
        table = db.query(BilliardTable).filter(BilliardTable.id == table_id).first()
        if not table:
            return JSONResponse({"status": "error", "message": "Khong tim thay ban"}, status_code=404)
        if table.current_status != "PLAYING":
            return JSONResponse({"status": "error", "message": "Ban chua bat tinh gio"}, status_code=400)
            
        active_session = db.query(PlaySession).filter(
            PlaySession.table_id == table_id,
            PlaySession.status == "ACTIVE"
        ).first()
        if not active_session:
            return JSONResponse({"status": "error", "message": "Khong tim thay phien choi active"}, status_code=400)
            
        end_time = datetime.now()
        duration = end_time - active_session.start_time
        total_minutes = max(1, math.ceil(duration.total_seconds() / 60))
        
        play_fee = math.ceil((total_minutes / 60.0) * table.price_per_hour)
        
        active_session.end_time = end_time
        active_session.total_minutes = total_minutes
        active_session.play_fee = play_fee
        active_session.status = "COMPLETED"
        
        table.current_status = "EMPTY"
        db.commit()
        
        items = db.query(SessionOrderItem).filter(SessionOrderItem.session_id == active_session.id).all()
        service_total = sum(i.total_price for i in items)
        total_bill = play_fee + service_total
        
        return JSONResponse({
            "status": "ok",
            "message": "Da thanh toan phien choi",
            "bill": {
                "session_id": active_session.id,
                "table_name": table.name,
                "start_time": active_session.start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "total_minutes": total_minutes,
                "play_fee": play_fee,
                "service_total": service_total,
                "total_bill": total_bill,
                "items": [{"name": i.item_name, "quantity": i.quantity, "total_price": i.total_price} for i in items]
            }
        })
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
    finally:
        db.close()

@router.post("/client-notify/{table_id}")
async def notify_client(table_id: int, payload: dict):
    message = payload.get("message", "")
    msg_type = payload.get("type", "info")
    redirect_url = payload.get("redirect_url", "")
    
    data = {
        "message": message,
        "type": msg_type,
        "redirect_url": redirect_url,
        "timestamp": time.time()
    }
    client_messages_store[table_id] = data
    try:
        r = redis_lib.Redis(host='localhost', port=6379, db=0, socket_timeout=0.2, socket_connect_timeout=0.2)
        r.set(f"client_msg_{table_id}", json.dumps(data))
        r.expire(f"client_msg_{table_id}", 300)
    except Exception:
        pass
    return JSONResponse({"status": "ok"})

@router.get("/client-poll/{table_id}")
async def poll_client(table_id: int):
    data = None
    if table_id in client_messages_store:
        data = client_messages_store.pop(table_id)
    try:
        r = redis_lib.Redis(host='localhost', port=6379, db=0, socket_timeout=0.2, socket_connect_timeout=0.2)
        if data:
            r.delete(f"client_msg_{table_id}")
        else:
            msg = r.get(f"client_msg_{table_id}")
            if msg:
                r.delete(f"client_msg_{table_id}")
                data = json.loads(msg)
    except Exception:
        pass
        
    if data:
        return JSONResponse({"has_message": True, "data": data})
    return JSONResponse({"has_message": False})

@router.post("/session/transfer/{from_table_id}/{to_table_id}")
async def transfer_session(from_table_id: int, to_table_id: int):
    db = SessionLocal()
    try:
        if from_table_id == to_table_id:
            return JSONResponse({"status": "error", "message": "Không thể chuyển sang cùng bàn!"}, status_code=400)
            
        from_table = db.query(BilliardTable).filter(BilliardTable.id == from_table_id).first()
        to_table = db.query(BilliardTable).filter(BilliardTable.id == to_table_id).first()
        
        if not from_table or not to_table:
            return JSONResponse({"status": "error", "message": "Bàn không tồn tại!"}, status_code=404)
            
        if from_table.current_status != "PLAYING":
            return JSONResponse({"status": "error", "message": f"{from_table.name} không ở trạng thái đang chơi!"}, status_code=400)
            
        if to_table.current_status == "PLAYING":
            return JSONResponse({"status": "error", "message": f"{to_table.name} đã có khách chơi, không thể chuyển sang!"}, status_code=400)
            
        active_session = db.query(PlaySession).filter(
            PlaySession.table_id == from_table_id,
            PlaySession.status == "ACTIVE"
        ).first()
        
        if not active_session:
            return JSONResponse({"status": "error", "message": "Không tìm thấy phiên chơi active!"}, status_code=404)
            
        active_session.table_id = to_table_id
        from_table.current_status = "EMPTY"
        to_table.current_status = "PLAYING"
        
        db.commit()

        to_token = generate_table_token(to_table_id)
        new_url = f"/menu/{to_table_id}/{to_token}"
        
        notify_data = {
            "message": f"Yêu cầu đổi bàn đã được chấp nhận! Bạn đã được chuyển từ {from_table.name} sang {to_table.name}.",
            "type": "redirect",
            "redirect_url": new_url,
            "timestamp": time.time()
        }
        client_messages_store[from_table_id] = notify_data
        
        try:
            r = redis_lib.Redis(host='localhost', port=6379, db=0, socket_timeout=0.2, socket_connect_timeout=0.2)
            r.set(f"client_msg_{from_table_id}", json.dumps(notify_data))
            r.expire(f"client_msg_{from_table_id}", 300)
        except Exception:
            pass
            
        return JSONResponse({
            "status": "ok",
            "message": f"Đã chuyển phiên chơi thành công từ {from_table.name} sang {to_table.name}!"
        })
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
    finally:
        db.close()

@router.get("/poll")
async def poll_events():
    return JSONResponse({"status": "ok", "events": []})

@router.get("/history")
async def get_history():
    db = SessionLocal()
    try:
        now = datetime.now()
        sessions = db.query(PlaySession).filter(PlaySession.status == "COMPLETED").order_by(PlaySession.end_time.desc()).all()
        
        result = []
        for s in sessions:
            table = db.query(BilliardTable).filter(BilliardTable.id == s.table_id).first()
            items = db.query(SessionOrderItem).filter(SessionOrderItem.session_id == s.id).all()
            
            service_total = sum(i.total_price for i in items)
            total_bill = (s.play_fee or 0) + service_total
            
            can_delete = False
            if s.end_time:
                diff_hours = (now - s.end_time).total_seconds() / 3600.0
                if diff_hours <= 2.0:
                    can_delete = True
                    
            result.append({
                "id": s.id,
                "table_id": s.table_id,
                "table_name": table.name if table else f"Bàn {s.table_id}",
                "start_time": s.start_time.isoformat() + "Z",
                "end_time": s.end_time.isoformat() + "Z" if s.end_time else None,
                "total_minutes": s.total_minutes or 0,
                "play_fee": s.play_fee or 0,
                "service_total": service_total,
                "total_bill": total_bill,
                "can_delete": can_delete,
                "items": [{"item_name": i.item_name, "quantity": i.quantity, "total_price": i.total_price} for i in items]
            })
        return JSONResponse(result)
    finally:
        db.close()

@router.delete("/history")
async def delete_history(payload: dict):
    ids = payload.get("ids", [])
    if not ids:
        return JSONResponse({"status": "error", "message": "Không có hóa đơn nào được chọn"}, status_code=400)
        
    db = SessionLocal()
    try:
        now = datetime.now()
        deleted_count = 0
        cannot_delete_count = 0
        
        for hid in ids:
            session = db.query(PlaySession).filter(PlaySession.id == hid, PlaySession.status == "COMPLETED").first()
            if not session:
                continue
                
            if session.end_time:
                diff_hours = (now - session.end_time).total_seconds() / 3600.0
                if diff_hours > 2.0:
                    cannot_delete_count += 1
                    continue
                    
            db.query(SessionOrderItem).filter(SessionOrderItem.session_id == session.id).delete()
            db.delete(session)
            deleted_count += 1
            
        db.commit()
        
        msg = f"Đã xóa thành công {deleted_count} hóa đơn."
        if cannot_delete_count > 0:
            msg += f" (Bỏ qua {cannot_delete_count} hóa đơn đã quá 2 giờ)"
            
        return JSONResponse({"status": "ok", "message": msg})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
    finally:
        db.close()
