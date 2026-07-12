# 🔒 Intelligent Encrypted Cloud Log Monitoring with Machine Learning-Based Anomaly Detection

## 📌 Project Overview

This project is a secure cloud log monitoring system developed to detect abnormal activities and potential cyber threats using Machine Learning. The application continuously monitors cloud log data, encrypts sensitive information, and identifies suspicious behavior to improve cloud security.

The system combines machine learning techniques with encrypted log storage to ensure both accurate threat detection and secure data management.

---

## 🎯 Objectives

- Monitor cloud log data in real time.
- Detect anomalies using Machine Learning.
- Protect sensitive log data through encryption.
- Improve cloud security by identifying suspicious activities.
- Provide early alerts for potential cyber threats.

## Quick Start (VS Code)

### Step 1 — Open Terminal in VS Code
```
Ctrl + ` (backtick)
```

### Step 2 — Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Start the Backend Server
```bash
uvicorn main:app --reload
```

You should see:
```
[DB]  Database initialised → threat_logs.db
[ML]  Isolation Forest trained on 500 baseline samples
[APP] Server ready at http://127.0.0.1:8000
[APP] Dashboard at  http://127.0.0.1:8000/dashboard
```

### Step 5 — Open the Dashboard
Open your browser and go to:
```
http://127.0.0.1:8000/dashboard
```

---

## Email Alerts (Optional)

To enable real email alerts, edit these lines in `main.py`:

```python
EMAIL_SENDER   = "your_email@gmail.com"
EMAIL_PASSWORD = "your_gmail_app_password"   # NOT your regular password
EMAIL_RECEIVER = "receiver@gmail.com"
SEND_EMAILS    = True
```

**How to get a Gmail App Password:**
1. Go to myaccount.google.com → Security
2. Enable 2-Step Verification
3. Search "App Passwords" → Generate one for "Mail"
4. Use that 16-character password above

---

## API Endpoints

| Method | Endpoint           | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | /                  | Health check + endpoint list         |
| GET    | /dashboard         | Serve frontend HTML                  |
| GET    | /simulate          | Simulate 1 traffic event             |
| GET    | /simulate/burst    | Simulate N events (?count=10)        |
| GET    | /logs              | Get logs (?limit=50)                 |
| GET    | /stats             | Aggregate statistics                 |
| GET    | /graph             | Matplotlib chart as base64 PNG       |
| DELETE | /logs/clear        | Clear all database logs              |

### Test via Browser (API Docs)
FastAPI auto-generates interactive API docs at:
```
http://127.0.0.1:8000/docs
```

---

## How the ML Works

1. **Training**: At startup, 500 "normal" traffic samples are generated from typical activities (Login, API, DNS) and used to train the Isolation Forest model.

2. **Feature Vector** per event:
   - Activity type (label-encoded)
   - IP type (internal=1, external=0)
   - Port range (high port=1)
   - Bytes transferred (normalised)
   - Hour of day (normalised)

3. **Scoring**: The Isolation Forest assigns an anomaly score. Combined with per-activity threat probability, a final score is computed.

4. **Classification**: Score ≥ 0.55 → **THREAT**, else **NORMAL**

---

## Demo Flow (for Review Presentation)

1. Start server: `uvicorn main:app --reload`
2. Open: `http://127.0.0.1:8000/dashboard`
3. Click **[ SIMULATE TRAFFIC ]** — show single event detection
4. Click **[ BURST ×10 ]** — show live table + chart update
5. Click **[ BURST ×25 ]** — show statistics populate
6. Click **[ GENERATE GRAPH ]** — show Matplotlib visualization
7. Open `http://127.0.0.1:8000/docs` — show FastAPI Swagger UI
8. Show `threat_logs.db` in VS Code with SQLite Viewer extension

---

## Technologies Used

| Layer          | Technology                    |
|----------------|-------------------------------|
| Backend        | Python, FastAPI, Uvicorn      |
| ML Model       | Isolation Forest (scikit-learn)|
| Database       | SQLite (built-in)             |
| Visualization  | Matplotlib                    |
| Frontend       | HTML, CSS, JavaScript         |
| Charts (UI)    | Chart.js                      |
| Alert System   | SMTP (Gmail)                  |
| API Testing    | FastAPI Swagger UI /docs      |

---

## VS Code Extensions (Recommended)

- **Python** (Microsoft)
- **SQLite Viewer** — to inspect threat_logs.db
- **REST Client** — to test API endpoints
- **Pylance** — Python IntelliSense

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `uvicorn not found` | Run `pip install -r requirements.txt` |
| `CORS error` in browser | Make sure backend is running on port 8000 |
| `ModuleNotFoundError` | Activate your virtual environment first |
| Email not sending | Check Gmail App Password + set SEND_EMAILS=True |
| Charts not loading | Check browser console, ensure Chart.js CDN loads |

---

## 💡 Future Enhancements

- Real-time cloud deployment
- Advanced deep learning models
- Multi-cloud support
- Interactive dashboard
- Email and SMS alert notifications


## 👨‍💻 Author

**Sudharsan M M**

📧 Email: Sudharsan.m.m344@gmail.com

🔗 LinkedIn: https://www.linkedin.com/in/sudharsan344

💻 GitHub: https://github.com/sudharsan344

