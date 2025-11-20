from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime
import smtplib
import ssl
from dotenv import load_dotenv
from flask import send_from_directory

load_dotenv()

app = Flask(__name__)
CORS(app)

MESSAGES_FILE = 'messages.xlsx'
APPLICATIONS_FILE = 'applications.xlsx'

SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT') or 0)
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')


def save_to_excel(path, columns, row_values):
    # row_values should be a dict matching columns
    if os.path.exists(path):
        try:
            df = pd.read_excel(path)
            df = df.append(row_values, ignore_index=True)
        except Exception:
            df = pd.DataFrame([row_values], columns=columns)
    else:
        df = pd.DataFrame([row_values], columns=columns)
    df.to_excel(path, index=False)


def send_email(subject, body):
    if not (SMTP_HOST and SMTP_PORT and SMTP_USER and SMTP_PASS and RECIPIENT_EMAIL):
        return False, 'SMTP not configured'
    message = f"Subject: {subject}\n\n{body}"
    try:
        context = ssl.create_default_context()
        # common ports: 465 (SSL), 587 (STARTTLS)
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(SMTP_USER, RECIPIENT_EMAIL, message)
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls(context=context)
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(SMTP_USER, RECIPIENT_EMAIL, message)
        return True, 'Email sent'
    except Exception as e:
        return False, str(e)


@app.route('/submit', methods=['POST'])
def submit_message():
    data = request.get_json() or {}
    name = data.get('name') or data.get('Name') or ''
    email = data.get('email') or data.get('Email') or ''
    interest = data.get('interest') or data.get('Interest') or ''
    message = data.get('message') or data.get('Message') or ''
    ts = datetime.utcnow().isoformat()

    row = {
        'timestamp': ts,
        'name': name,
        'email': email,
        'interest': interest,
        'message': message
    }
    try:
        save_to_excel(MESSAGES_FILE, list(row.keys()), row)
    except Exception as e:
        return jsonify(success=False, message=f'Failed to save: {e}'), 500

    subject = f'New message from {name or "Website"}'
    body = f"Time: {ts}\nName: {name}\nEmail: {email}\nInterest: {interest}\n\nMessage:\n{message}"
    ok, info = send_email(subject, body)
    if not ok:
        # still return success but inform about email
        return jsonify(success=True, message='Saved but email not sent: ' + info)
    return jsonify(success=True, message='Saved and notification sent')


@app.route('/apply', methods=['POST'])
def apply():
    data = request.get_json() or {}
    name = data.get('name') or ''
    phone = data.get('phone') or ''
    email = data.get('email') or ''
    college = data.get('college') or ''
    resume = data.get('resume') or data.get('resume_link') or data.get('resume_link') or ''
    role = data.get('role') or ''
    ts = datetime.utcnow().isoformat()

    row = {
        'timestamp': ts,
        'name': name,
        'phone': phone,
        'email': email,
        'college': college,
        'resume': resume,
        'role': role
    }
    try:
        save_to_excel(APPLICATIONS_FILE, list(row.keys()), row)
    except Exception as e:
        return jsonify(success=False, message=f'Failed to save: {e}'), 500

    subject = f'New application: {role} - {name}'
    body = "\n".join([f"{k}: {v}" for k, v in row.items()])
    ok, info = send_email(subject, body)
    if not ok:
        return jsonify(success=True, message='Saved but email not sent: ' + info)
    return jsonify(success=True, message='Application saved and notification sent')


if __name__ == '__main__':
    # When running in development, serve static files from project root
    @app.route('/')
    def index():
        return send_from_directory('.', 'index.html')

    @app.route('/<path:filename>')
    def serve_file(filename):
        # Only serve files that actually exist in the project folder
        filepath = os.path.join('.', filename)
        if os.path.exists(filepath):
            return send_from_directory('.', filename)
        return jsonify({'error': 'Not Found'}), 404

    app.run(host='0.0.0.0', port=5000, debug=True)
