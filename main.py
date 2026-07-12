from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import sqlite3, random, datetime

# 🔥 EMAIL IMPORTS
import smtplib
from email.mime.text import MIMEText

app = FastAPI()
def db():
    conn = sqlite3.connect("logs.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= EMAIL FUNCTION =================
EMAIL_SENDER = "sudharsanchinna344@gmail.com"
EMAIL_PASSWORD = "kdpc nqfh gcal txri"
EMAIL_RECEIVER = "sudharsan.m.m344@gmail.com"

def send_email(event):
    print("📧 EMAIL FUNCTION CALLED")
    try:
        subject = f"🚨 CYBER ALERT: {event['activity']}"

        body = f"""
⚠️ THREAT DETECTED

Time: {event['time']}
IP Address: {event['ip']}
Activity: {event['activity']}
Status: {event['status']}
Score: {event['score']}
"""

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = "sudharsanchinna344@gmail.com"
        msg["To"] = "sudharsan.m.m344@gmail.com"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("sudharsanchinna344@gmail.com","kdpc nqfh gcal txri")
        server.send_message(msg)
        server.quit()

        print("✅ EMAIL SENT")

    except Exception as e:
        print("❌ EMAIL ERROR:", e)

# ================= EVENT GENERATION =================

def generate_event():

    activities = ["Login", "API", "Upload", "SQL Injection", "XSS"]
    activity = random.choice(activities)

    # 🔐 Threat logic
    if activity in ["SQL Injection", "XSS"]:
        status = "THREAT"
        score = round(random.uniform(0.7, 1.0), 2)
    else:
        status = "NORMAL"
        score = round(random.uniform(0.1, 0.5), 2)

    ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
    time = datetime.datetime.now().strftime("%H:%M:%S")

    lat = random.uniform(-60, 60)
    lon = random.uniform(-180, 180)

    # ================= STORE =================

    conn = db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO logs(time, ip, activity, status, score, lat, lon)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (time, ip, activity, status, score, lat, lon))

    conn.commit()
    conn.close()

    # 🔥 EMAIL ALERT ONLY FOR THREAT
    if status == "THREAT":
        send_email({
            "time": time,
            "ip": ip,
            "activity": activity,
            "status": status,
            "score": score
        })

    return {
        "time": time,
        "ip": ip,
        "activity": activity,
        "status": status,
        "score": score,
        "lat": lat,
        "lon": lon
    }

# ================= ROUTES =================

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return RedirectResponse("/dashboard")

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/index.html")

@app.get("/hello")
def hello():
    return {"message": "hello kiddo"}
@app.get("/simulate")
def simulate():
    return generate_event()

@app.get("/simulate/burst")
def burst():
    return [generate_event() for _ in range(10)]
@app.get("/test-email")
def test_email():
    send_email({
        "time": "TEST",
        "ip": "127.0.0.1",
        "activity": "TEST ALERT",
        "status": "THREAT",
        "score": 1.0
    })
    return {"message": "Email triggered"}

@app.get("/logs")
def logs():
    conn = db()
    rows = conn.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 20").fetchall()
    conn.close()
    return {"logs": [dict(r) for r in rows]}

@app.get("/stats")
def stats():
    conn = db()

    total = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
    threats = conn.execute("SELECT COUNT(*) FROM logs WHERE status='THREAT'").fetchone()[0]
    normal = conn.execute("SELECT COUNT(*) FROM logs WHERE status='NORMAL'").fetchone()[0]

    conn.close()

    rate = round((threats / total * 100), 1) if total else 0

    return {
        "total": total,
        "threats": threats,
        "normal": normal,
        "threat_rate_pct": rate
    }

@app.delete("/clear")
def clear():
    conn = db()
    conn.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
    return {"status": "cleared"}

# ================= START =================
def init_db():
    conn = sqlite3.connect("logs.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY,
        time TEXT,
        ip TEXT,
        activity TEXT,
        status TEXT,
        score REAL,
        lat REAL,
        lon REAL
    )
    """)

    conn.commit()
    conn.close()
@app.on_event("startup")
def start():
    init_db()
    print("🚀 SYSTEM READY WITH EMAIL ALERTS")