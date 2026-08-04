from typing import Optional
from fastapi import Header, HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from domain.store.value_objects import Role
from api.auth import verify_token

security = HTTPBearer(auto_error=False)

class StoreContext:
    def __init__(self, store_id: Optional[int], role: Role, user_id: Optional[int] = None):
        self.store_id = store_id
        self.role = role
        self.user_id = user_id
        
    def require_write_permission(self):
        """Kiểm tra quyền ghi, nếu là Trụ sở (HQ) sẽ từ chối 403."""
        if self.role.is_hq():
            raise HTTPException(status_code=403, detail="Máy Mẹ (HQ) chỉ có quyền đọc dữ liệu, không được phép ghi/sửa dữ liệu nghiệp vụ.")

def get_store_context(
    request: Request,
    auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> StoreContext:
    token = None
    if auth_credentials and auth_credentials.credentials:
        token = auth_credentials.credentials
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        
    if token:
        token = token.split(",")[0].replace("Bearer ", "").strip()
        
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = verify_token(token)
    
    role_str = str(payload.get("role", "STORE_MANAGER")).upper()
    try:
        role = Role(role_str)
    except ValueError:
        role = Role.STORE_MANAGER
        
    user_id = payload.get("user_id")
    
    if role.is_hq():
        ctx = StoreContext(store_id=None, role=role, user_id=user_id)
    else:
        store_id = payload.get("store_id")
        if store_id is None:
            store_id = 1
        else:
            store_id = int(store_id)
        ctx = StoreContext(store_id=store_id, role=role, user_id=user_id)
        
    request.state.store_context = ctx
    request.state.store_id = ctx.store_id
    request.state.user_role = str(ctx.role.value) if ctx.role else "STORE_MANAGER"
    return ctx
