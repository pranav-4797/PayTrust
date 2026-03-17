<div align="center">

<img src="static/logo.png" alt="PayTrust Logo" width="320"/>

# PayTrust — Secure UPI Payment Platform

**AI-powered fraud detection · Real-time OTP verification · Smart risk scoring**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)](https://reactjs.org)
[![Railway](https://img.shields.io/badge/Deploy-Railway-8B5CF6?style=flat-square)](https://railway.app)

</div>

---

## What is PayTrust?

PayTrust is a full-stack UPI payment simulation platform built for fraud detection research and demonstration. It combines a React frontend with a FastAPI backend to simulate real-world payment flows — complete with AI-driven fraud analysis, OTP verification via Twilio, and a live customer support assistant.

---

## Features

### 🔐 Authentication
- **Mobile + PIN login** — 4-digit PIN with lockout after 3 failed attempts
- **OTP verification** — Real SMS via Twilio on every login and high-risk payment
- **Session management** — Auto logout, secure balance reveal behind PIN

### 💸 Send Money
- **UPI ID payment** — Pay by typing any registered UPI address
- **Phone number payment** — Auto-resolves mobile number to UPI ID with live account lookup
- **Real-time balance check** — Blocks payment instantly if amount exceeds available balance
- **Quick amount chips** — One-tap ₹500 / ₹1,000 / ₹5,000 / ₹10,000 presets
- **Payment notes** — Add a description to every transfer

### 🤖 AI Fraud Detection Engine (4-Tier)

Every transaction is scored 0–100 in real time before processing:

| Score | Tier | Action |
|-------|------|--------|
| 0–39 | ✅ Safe | Silent allow — no interruption |
| 40–69 | ⚠️ Caution | Info card shown — user decides freely |
| 70–89 | 🔶 Warning | OTP required before proceeding |
| 90+ | 🚨 Blocked | Transaction blocked + logged |

**Risk signals detected:**
- 🔤 **Keyword Risk Engine** — 40+ weighted suspicious keywords in UPI IDs (`kyc`, `refund`, `helpdesk`, `otp`, `verify`, `bank`, `reward`, `lucky`, `prize`, `lottery` etc.) with HIGH / MEDIUM / LOW tiers
- 📊 **Behavioural Deviation** — Z-score analysis against your transaction history; flags amounts unusually far from your average
- 🎭 **Scam Pattern Classifier** — Detects 3+ simultaneous fraud signals (unknown recipient + large amount + odd hour + suspicious UPI)
- 🌙 **Odd-Hour Detection** — Transactions between 1AM–5AM trigger elevated risk
- 💰 **Balance Drain Analysis** — Flags if a payment uses >65% or >80% of current balance
- 👤 **Recipient Trust System** — Known contacts get reduced risk scores; unknown recipients get higher scores
- 🚩 **Recipient Risk Registry** — Network-wide flagging of recipients involved in blocked transactions
- 📈 **Cumulative Risk Score** — Risk compounds across the session, not just per transaction

### 📬 Payment Requests
- **Receive requests** from other PayTrust users with risk analysis on each
- **Accept with PIN** (low-risk) or **Accept with OTP** (high-risk)
- **Decline or Report** suspicious requests
- **Fraud scoring on requests** — separate engine checks requester history, amount vs average, balance drain, time of request

### 📜 Transaction History
- Full paginated history with Date, Recipient, Amount, Note, Risk Score, Status
- Filter by: All / Debit / Credit / Flagged / Blocked
- Visual risk badges and status chips on every row
- Animated entry for new transactions

### 📊 Fraud Insights
- **Risk Distribution** — Bar chart of Safe / Caution / Warning / Blocked counts
- **Weekly Risk Heatmap** — 7-day bar chart of average daily risk score
- **Payment Profile** — Your average payment, typical range, and total debit count derived from transaction history
- **Top Recipients** — Most frequent payment recipients ranked by transaction count
- **Flagged Transactions** — Quick list of all transactions with risk ≥ 70

### 🛡️ Account Security
- **Account Freeze** — Auto-triggered after repeated suspicious activity; shows countdown timer
- **Cooldown System** — Enforced wait period after burst of rapid transactions
- **Emergency Lock** — Permanent account freeze from Profile page for instant protection
- **Safety Score** — Live score (0–100) based on account risk history, shown on Profile
- **PIN Reset** — Change your 4-digit PIN from inside the app

### 📋 RBI Guidelines
- On-app popup with real RBI digital payment guidelines
- Fraud reporting steps (1930 helpline, cybercrime.gov.in)
- Shown automatically on first login

### 💬 Nexus — AI Support Assistant
- Floating chat widget available on every page
- Powered by keyword intent detection with topic restriction
- Handles: account freeze questions, OTP scams, flagged payments, QR safety, link safety, fraud reporting, UPI safety tips
- Quick-reply chips for common queries
- Off-topic questions are politely declined (restricted to payment safety only)

### 📱 Responsive Design
- Full sidebar navigation on desktop
- Bottom tab bar on mobile
- Optimised layouts for all screen sizes

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 (no build step — pure browser JS) |
| Styling | Custom CSS with DM Sans, CSS variables, animations |
| Backend | FastAPI (Python) |
| OTP | Twilio SMS API |
| Deployment | Railway (single service) |
| Font | Google Fonts — DM Sans |

---

## Test Users

| Name | Mobile | PIN | Balance | UPI |
|------|--------|-----|---------|-----|
| Chirayu Mahajan | 9340228345 | 1167 | ₹84,250 | chirayu@paytrust |
| Pranav Chopade | 9158763151 | 2611 | ₹32,780 | pranav@paytrust |
| Farhan Farooqui | 9766876442 | 1234 | ₹15,400 | farhan@paytrust |
| Mehul Patil | 9876543210 | 9876 | ₹67,120 | mehul@paytrust |
| Vedant Deshmukh | 9699189866 | 2805 | ₹51,900 | vedant@paytrust |

---

## Project Structure

```
paytrust-deploy/
├── main.py              ← FastAPI backend (API + static file server)
├── requirements.txt     ← Python dependencies
├── Procfile             ← Railway process definition
├── railway.json         ← Railway build & deploy config
├── .env.example         ← Environment variable template
├── .gitignore
├── README.md
└── static/
    ├── index.html       ← Full React app (single file, no build needed)
    ├── favicon.png
    ├── logo.png
    └── loginbg.jpg
```

---

## Local Development

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/paytrust.git
cd paytrust
pip install -r requirements.txt
```

### 2. Set environment variables

```bash
cp .env.example .env
# Edit .env and fill in your Twilio credentials
```

### 3. Run the server

```bash
uvicorn main:app --reload --port 8000
```

### 4. Open in browser

```
http://localhost:8000
```

> Both the frontend and API run on the same port. No separate frontend server needed.

---

## Railway Deployment

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/paytrust.git
git push -u origin main
```

### Step 2 — Deploy on Railway

1. Go to [railway.app](https://railway.app) → sign in with GitHub
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your `paytrust` repository
4. Railway auto-detects Python and starts deploying

### Step 3 — Add Environment Variables

In Railway dashboard → your service → **Variables** tab:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `TWILIO_PHONE` | Your Twilio phone number (e.g. `+12183665901`) |

### Step 4 — Generate a Domain

Railway dashboard → your service → **Settings** → **Domains** → **Generate Domain**

Your app goes live at: `https://paytrust-xxxx.up.railway.app` 🎉

---

## How the API Works

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the React frontend |
| `/health` | GET | Health check — returns `{"status":"ok"}` |
| `/send-otp` | POST | Generates OTP and sends via Twilio SMS |
| `/verify-otp` | POST | Validates OTP entered by user |

**OTP flow:**
```
Frontend → POST /send-otp { mobile: "9340228345" }
Twilio  → SMS "Your PayTrust OTP is 483921" → user's phone
Frontend → POST /verify-otp { mobile: "9340228345", otp: "483921" }
Backend  → { status: "SUCCESS" }
```

---

## Security Notes

- ✅ All credentials are loaded from environment variables — never hardcoded
- ✅ OTPs expire after 120 seconds
- ✅ `.env` is blocked by `.gitignore` — never committed to git
- ✅ GitHub secret scanning will find no secrets in this repository
- ✅ Twilio client only initialises when credentials are present

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| App shows blank page | Ensure `static/index.html` exists in the repo |
| OTP not sending | Check `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE` are set in Railway Variables |
| Build fails on Railway | Check Railway build logs — usually a missing package in `requirements.txt` |
| Port error | Railway sets `$PORT` automatically — `Procfile` handles it correctly |
| Login fails | Use exact mobile numbers from the Test Users table above |

---

<div align="center">

Built with ❤️ using FastAPI + React · Secured by Twilio · Deployed on Railway

</div>
