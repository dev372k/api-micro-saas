from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from commons.security import Security

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = Security.verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload

def require_admin(current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user

def require_user(current_user=Depends(get_current_user)):
    print("Payload:", current_user)  # Debugging line to print the payload
    if current_user.get("role") != "user":
        raise HTTPException(
            status_code=403,
            detail="User access required"
        )
    return current_user