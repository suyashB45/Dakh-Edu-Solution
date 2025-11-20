# Flask backend for Contact & Application submissions

This project adds a small Flask backend to accept contact messages and applications from the frontend, save them to Excel files, and optionally send notification emails.

Quick setup

1. Install Python dependencies (recommended to use a virtualenv):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill SMTP settings (if you want email notifications):

```powershell
copy .env.example .env
# then edit .env in an editor
```

3. Run the backend:

```powershell
python app.py
```

4. Open `index.html` in a browser (or serve it) and fill forms. The frontend posts to `http://localhost:5000/submit` and `/apply`.

Notes
- Submissions are stored in `messages.xlsx` and `applications.xlsx` in the project folder.
- If SMTP is not configured the app will still save submissions but will return a message indicating email wasn't sent.
- For production, run behind a proper WSGI server and secure credentials.

If you'd like I can also add a small PowerShell script to serve the static site, or configure the forms to use relative URLs when deployed. Tell me how you want to receive messages (email or SMS) and I can wire that up (Twilio or other provider). 
