import sys
import os

# Add parent directory to path so we can import from database
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import SessionLocal
from database.models import BilliardTable

db = SessionLocal()
try:
    if db.query(BilliardTable).filter(BilliardTable.name.like('%Bida Lỗ%')).count() == 0:
        db.add(BilliardTable(name="Bàn 5 (Bida Lỗ)", camera_url="4", price_per_hour=60000.0, table_tier="STANDARD", table_type="POOL"))
        db.add(BilliardTable(name="Bàn 6 (Bida Lỗ VIP)", camera_url="5", price_per_hour=80000.0, table_tier="VIP", table_type="POOL"))
        db.commit()
        print("Đã thêm 2 bàn Bida Lỗ vào CSDL.")
    else:
        print("Bàn Bida Lỗ đã tồn tại.")
finally:
    db.close()
