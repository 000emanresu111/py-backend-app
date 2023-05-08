from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from app import models
from app.database import engine
from app.routers import root, registration, login, verify_2fa

try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
routers = [root.router, registration.router, login.router, verify_2fa.router]

for router in routers:
    app.include_router(router)
