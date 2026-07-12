def send_email(event):
    try:
        print("📧 EMAIL FUNCTION TRIGGERED")

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
        msg["From"] = crazykiddo48@gmailcom
        msg["To"] = sudharsan.m.m344@gmail.com

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1)   # 🔥 IMPORTANT
        server.starttls()

        print("🔐 Logging into Gmail...")
        server.login(crazykiddo48@gmail.com, qazplm123890)

        print("📤 Sending email...")
        server.send_message(msg)

        server.quit()

        print("✅ EMAIL SENT SUCCESSFULLY")

    except Exception as e:
        print("❌ EMAIL FAILED:", e)
