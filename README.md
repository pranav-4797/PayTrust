# PayTrust — Railway Deployment Guide

## Folder Structure
```
paytrust-deploy/
├── main.py             ← FastAPI backend + static file server
├── requirements.txt    ← Python dependencies
├── Procfile            ← Railway start command
├── railway.json        ← Railway configuration
├── .gitignore
├── README.md
└── static/
    ├── index.html      ← React frontend (SPA)
    ├── favicon.png
    ├── logo.png
    └── loginbg.jpg
```

## How It Works
One Railway service handles EVERYTHING:
- `/send-otp` and `/verify-otp` → FastAPI OTP endpoints
- `/` and all other routes → Serves the React SPA from `static/`

The frontend uses `window.location.origin` as the API base URL,
so it automatically points to the correct Railway domain.

---

## Step-by-Step Railway Deployment

### Step 1 — Create a GitHub repository
1. Go to https://github.com/new
2. Create a new repository (e.g. `paytrust`)
3. Set it to **Public** or **Private** (either works)

### Step 2 — Push this folder to GitHub
Open a terminal in this folder and run:

```bash
git init
git add .
git commit -m "Initial PayTrust deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/paytrust.git
git push -u origin main
```

### Step 3 — Deploy on Railway
1. Go to https://railway.app and sign in (use GitHub login)
2. Click **"New Project"**
3. Click **"Deploy from GitHub repo"**
4. Select your `paytrust` repository
5. Railway will auto-detect Python and start deploying

### Step 4 — Set Environment Variables (optional but recommended)
In Railway dashboard → your service → **Variables** tab, add:

| Variable             | Value                        |
|----------------------|------------------------------|
| TWILIO_ACCOUNT_SID   | ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| TWILIO_AUTH_TOKEN    | your_twilio_auth_token       |
| TWILIO_PHONE         | +1xxxxxxxxxx                 |

> If you skip this, the hardcoded values in main.py will be used.

### Step 5 — Get your live URL
Once deployment succeeds (green status):
- Click your service → **Settings** → **Domains**
- Click **"Generate Domain"**
- Your app is live at: `https://paytrust-xxxx.up.railway.app`

---

## Test Users
| Name            | Mobile     | PIN  | Balance  |
|-----------------|------------|------|----------|
| Chirayu Mahajan | 9340228345 | 1167 | ₹84,250  |
| Pranav Chopade  | 9158763151 | 2611 | ₹32,780  |
| Farhan Farooqui | 9766876442 | 1234 | ₹15,400  |
| Mehul Patil     | 9876543210 | 9876 | ₹67,120  |
| Vedant Deshmukh | 9699189866 | 2805 | ₹51,900  |

---

## Verify Deployment
After deployment, open your Railway URL and check:
- ✅ App loads correctly
- ✅ `/health` returns `{"status": "ok"}`
- ✅ Login works with test users
- ✅ OTP is sent via Twilio on payment

---

## Troubleshooting
| Issue | Fix |
|-------|-----|
| Build fails | Check Railway build logs for missing package |
| OTP not sending | Check TWILIO env variables are set correctly |
| App shows blank page | Check browser console, ensure `static/` folder has index.html |
| Port error | Railway sets `$PORT` automatically — Procfile handles it |
