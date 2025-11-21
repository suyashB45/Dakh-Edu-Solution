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

# Office / Visit address used in site and emails
OFFICE_ADDRESS = 'Sri Sai Ram Engineering College, West Tambaram, Chennai, Tamil Nadu, India'

SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT') or 0)
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')


def save_to_excel(path, columns, row_values):
    # Ensure a stable column order when writing rows to Excel.
    # `columns` should be the desired column ordering list.
    new_row = pd.DataFrame([row_values])
    # Reindex new_row to have all desired columns (missing columns will be created)
    new_row = new_row.reindex(columns=columns)

    if os.path.exists(path):
        try:
            df = pd.read_excel(path)
            # Ensure existing dataframe has the desired columns (add missing)
            for c in columns:
                if c not in df.columns:
                    df[c] = None
            # Reorder existing df to desired columns
            df = df[columns]
            # Append new row
            df = pd.concat([df, new_row], ignore_index=True, sort=False)
        except Exception:
            df = new_row
    else:
        df = new_row
    # Write using the specified column order
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
        # Use fixed column ordering for messages
        msg_cols = ['timestamp', 'name', 'email', 'interest', 'message']
        save_to_excel(MESSAGES_FILE, msg_cols, row)
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
        # Use fixed column ordering for applications
        app_cols = ['timestamp', 'name', 'phone', 'email', 'college', 'resume', 'role']
        save_to_excel(APPLICATIONS_FILE, app_cols, row)
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
