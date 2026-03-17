from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from twilio.rest import Client
import random
import time
import os

app = FastAPI()

# ─────────────────────────────────────────────
# CORS
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# TWILIO — loaded from Railway environment variables ONLY
# Set in Railway dashboard → your service → Variables:
#   TWILIO_ACCOUNT_SID   = ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#   TWILIO_AUTH_TOKEN    = your_auth_token
#   TWILIO_PHONE         = +1xxxxxxxxxx
# ─────────────────────────────────────────────
ACCOUNT_SID  = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN   = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE")

_twilio_client = None
if ACCOUNT_SID and AUTH_TOKEN:
    _twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

# ─────────────────────────────────────────────
# OTP STORE
# ─────────────────────────────────────────────
otp_store: dict = {}
OTP_EXPIRY = 120


class SendOTP(BaseModel):
    mobile: str


class VerifyOTP(BaseModel):
    mobile: str
    otp: str


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


# ─────────────────────────────────────────────
# API ROUTES
# ─────────────────────────────────────────────
@app.post("/send-otp")
def send_otp(data: SendOTP):
    otp = generate_otp()
    otp_store[data.mobile] = {"otp": otp, "expiry": time.time() + OTP_EXPIRY}
    if not _twilio_client or not TWILIO_PHONE:
        return {"status": "OTP_SENT", "_dev_otp": otp}
    try:
        _twilio_client.messages.create(
            body=f"Your PayTrust OTP is {otp}",
            from_=TWILIO_PHONE,
            to="+91" + data.mobile,
        )
        return {"status": "OTP_SENT"}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


@app.post("/verify-otp")
def verify_otp(data: VerifyOTP):
    record = otp_store.get(data.mobile)
    if not record:
        return {"status": "NO_OTP"}
    if time.time() > record["expiry"]:
        return {"status": "OTP_EXPIRED"}
    if record["otp"] == data.otp:
        del otp_store[data.mobile]
        return {"status": "SUCCESS"}
    return {"status": "INVALID"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ─────────────────────────────────────────────
# SERVE FRONTEND
# ─────────────────────────────────────────────
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static-assets", StaticFiles(directory=STATIC_DIR), name="static-assets")


@app.get("/")
def serve_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/{full_path:path}")
def serve_spa(full_path: str):
    requested = os.path.join(STATIC_DIR, full_path)
    if os.path.isfile(requested):
        return FileResponse(requested)
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
