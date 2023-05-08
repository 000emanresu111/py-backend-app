from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

router = APIRouter()

bearer_scheme = HTTPBearer()


@router.get("/")
async def root(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if not credentials.scheme == "Bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    try:
        return {"status": "OK"}
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
