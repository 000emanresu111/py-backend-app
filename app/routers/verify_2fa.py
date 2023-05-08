from fastapi import APIRouter, Depends, HTTPException, status, Form


router = APIRouter()


# TODO: implement verification logic
@router.post("/verify_otp")
async def verify_otp(otp_code: str):
    if otp_code:
        return "OK"
