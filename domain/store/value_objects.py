from enum import Enum

class Role(Enum):
    """
    DDD Value Object: Phân quyền người dùng trong hệ thống Multi-Store.
    """
    SUPER_ADMIN = "SUPER_ADMIN"
    STORE_MANAGER = "STORE_MANAGER"
    CASHIER = "CASHIER"
    
    def is_hq(self) -> bool:
        return self == Role.SUPER_ADMIN

class StoreStatus(Enum):
    """
    DDD Value Object: Trạng thái hoạt động của cửa hàng.
    """
    ACTIVE = "ACTIVE"
    MAINTENANCE = "MAINTENANCE"
    CLOSED = "CLOSED"
