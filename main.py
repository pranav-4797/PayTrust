from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from twilio.rest import Client
from huggingface_hub import hf_hub_download
import pandas as pd
import random
import time
import os
import threading

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
# TWILIO — set in Railway → Variables
# ─────────────────────────────────────────────
ACCOUNT_SID  = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN   = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE")

_twilio_client = None
if ACCOUNT_SID and AUTH_TOKEN:
    _twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

# ─────────────────────────────────────────────
# DATASET — loaded from Hugging Face at startup
# Set in Railway → Variables:
#   HF_TOKEN = hf_xxxxxxxxxxxxxxxxxxxxxxxxxx
# ─────────────────────────────────────────────
HF_TOKEN     = os.environ.get("HF_TOKEN")
HF_REPO_ID   = "pranav4797/PS_20174392719_1491204439457_log"
HF_FILENAME  = "PS_20174392719_1491204439457_log.csv"
CACHE_PATH   = "/tmp/fraud_dataset.csv"

# Global dataframe + status — loaded in background thread
df: pd.DataFrame | None = None
dataset_status = {"ready": False, "error": None, "rows": 0}


def load_dataset():
    """Download dataset from Hugging Face and load into memory."""
    global df
    try:
        print("[Dataset] Starting download from Hugging Face...")

        # Use cached file if already present (Railway container restart)
        if os.path.exists(CACHE_PATH):
            print("[Dataset] Found cached file, loading...")
        else:
            path = hf_hub_download(
                repo_id=HF_REPO_ID,
                filename=HF_FILENAME,
                repo_type="dataset",
                token=HF_TOKEN,
                local_dir="/tmp",
            )
            # Rename to known cache path for clarity
            if path != CACHE_PATH:
                os.rename(path, CACHE_PATH)

        df = pd.read_csv(CACHE_PATH)
        dataset_status["ready"] = True
        dataset_status["rows"]  = len(df)
        print(f"[Dataset] Loaded {len(df):,} rows ✅")

    except Exception as e:
        dataset_status["error"] = str(e)
        print(f"[Dataset] Failed to load: {e}")


# Start loading in background so app starts instantly
_loader = threading.Thread(target=load_dataset, daemon=True)
_loader.start()

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
    """Health check — also returns dataset load status."""
    return {
        "status": "ok",
        "dataset": {
            "ready": dataset_status["ready"],
            "rows":  dataset_status["rows"],
            "error": dataset_status["error"],
        },
    }


@app.get("/api/dataset/status")
def dataset_status_endpoint():
    """Check if the dataset has finished loading."""
    return JSONResponse(dataset_status)


@app.get("/api/dataset/sample")
def dataset_sample(n: int = 5):
    """Return n sample rows from the dataset (for testing)."""
    if not dataset_status["ready"]:
        return JSONResponse(
            {"error": "Dataset not ready yet.", "status": dataset_status},
            status_code=503,
        )
    sample = df.head(n).to_dict(orient="records")
    return {"rows": sample, "total": dataset_status["rows"]}


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
