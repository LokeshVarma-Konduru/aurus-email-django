# Aurus AI — Django OTP Email Service

Sends beautifully branded OTP emails with CID-embedded logo.
Works correctly in **Gmail**, **Zoho Mail**, and **Outlook**.

---

## Project Structure

```
aurus-email/
├── .env                          ← Your secrets (never commit this)
├── .gitignore
├── manage.py
├── requirements.txt
│
├── aurus_email/                  ← Django project config
│   ├── settings.py
│   └── urls.py
│
└── otp_service/                  ← Main app
    ├── models.py                 ← OTPRecord database model
    ├── views.py                  ← API endpoints (send, verify, health)
    ├── urls.py                   ← Route definitions
    ├── serializers.py            ← Request validation
    ├── email_service.py          ← CID logo embedding logic
    ├── admin.py                  ← Admin panel config
    │
    ├── static/images/            ← ⭐ PUT YOUR LOGO FILES HERE
    │   ├── logo-black.jpeg
    │   ├── logo-white.jpeg
    │   ├── aurus-black.jpeg
    │   └── aurus-white.jpeg
    │
    ├── templates/emails/
    │   └── otp_email.html        ← Email template (Aurus dark-navy design)
    │
    └── management/commands/
        └── test_email.py         ← Terminal test command
```

---

## Step 1 — Copy Your Logo Files

Copy all 4 logos from your `aurus-email` folder into:
```
otp_service/static/images/
```

Your logos (from the folder you showed):
```
logo-black.jpeg   →  otp_service/static/images/logo-black.jpeg
logo-white.jpeg   →  otp_service/static/images/logo-white.jpeg
aurus-black.jpeg  →  otp_service/static/images/aurus-black.jpeg
aurus-white.jpeg  →  otp_service/static/images/aurus-white.jpeg
```

The email uses `logo-white.jpeg` by default (white logo on dark background).
Change `EMAIL_LOGO_KEY` in `settings.py` to switch logos.

---

## Step 2 — Get Gmail App Password

> ⚠️ Gmail blocks regular passwords for SMTP. You MUST use an App Password.

1. Go to: **https://myaccount.google.com/security**
2. Enable **2-Step Verification** (if not already on)
3. Go to: **https://myaccount.google.com/apppasswords**
4. Select app: **Mail** | Select device: **Windows Computer**
5. Click **Generate**
6. Copy the **16-character password** (e.g. `abcd efgh ijkl mnop`)

---

## Step 3 — Update .env File

Open `.env` and update:
```env
EMAIL_HOST_USER=loki1432varma@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop   ← paste your App Password (no spaces)
DEFAULT_FROM_EMAIL=Aurus AI <loki1432varma@gmail.com>
```

---

## Step 4 — Create Virtual Environment & Install

Open terminal in the project folder and run:

```bash
# Windows (Command Prompt or PowerShell)
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Then install dependencies:
```bash
pip install -r requirements.txt
```

---

## Step 5 — Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

You should see:
```
Applying otp_service.0001_initial... OK
```

---

## Step 6 — Quick Email Test (No Server Needed)

Before starting the server, test email directly:

```bash
python manage.py test_email --to loki1432varma@gmail.com
```

Or test with a specific OTP code:
```bash
python manage.py test_email --to loki1432varma@gmail.com --code 123456
```

**Expected output:**
```
📧 Sending test OTP email to: loki1432varma@gmail.com
   OTP Code: 993773

✅ Email sent successfully to loki1432varma@gmail.com!

Check your inbox and verify:
  [ ] Gmail      → logo shows as proper icon
  [ ] Zoho Mail  → logo shows (not "Au")
  [ ] Outlook    → logo shows (not "A")
```

---

## Step 7 — Start the Server

```bash
python manage.py runserver
```

Server runs at: **http://localhost:8000**

---

## Step 8 — Test the API

### Option A: Browser (Health Check only)
Open: **http://localhost:8000/api/otp/health/**

### Option B: PowerShell (Windows)

**Send OTP:**
```powershell
$body = '{"email": "loki1432varma@gmail.com"}'
Invoke-RestMethod -Uri "http://localhost:8000/api/otp/send/" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**Verify OTP:**
```powershell
$body = '{"email": "loki1432varma@gmail.com", "code": "993773"}'
Invoke-RestMethod -Uri "http://localhost:8000/api/otp/verify/" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

### Option C: curl (Git Bash / WSL / macOS)

**Send OTP:**
```bash
curl -X POST http://localhost:8000/api/otp/send/ \
  -H "Content-Type: application/json" \
  -d '{"email": "loki1432varma@gmail.com"}'
```

**Verify OTP:**
```bash
curl -X POST http://localhost:8000/api/otp/verify/ \
  -H "Content-Type: application/json" \
  -d '{"email": "loki1432varma@gmail.com", "code": "993773"}'
```

### Option D: Postman / Bruno / Thunder Client

| Field | Value |
|---|---|
| Method | POST |
| URL | `http://localhost:8000/api/otp/send/` |
| Headers | `Content-Type: application/json` |
| Body | `{"email": "loki1432varma@gmail.com"}` |

---

## API Reference

### POST `/api/otp/send/`

**Request:**
```json
{ "email": "user@example.com" }
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "OTP sent to user@example.com",
  "expires_in": 10
}
```

**Error Response (400 — bad email):**
```json
{
  "success": false,
  "errors": { "email": ["Enter a valid email address."] }
}
```

---

### POST `/api/otp/verify/`

**Request:**
```json
{ "email": "user@example.com", "code": "993773" }
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "OTP verified successfully."
}
```

**Error Responses (400):**
```json
{ "success": false, "message": "Invalid OTP. Please try again." }
{ "success": false, "message": "OTP has expired. Please request a new one." }
{ "success": false, "message": "No active OTP found for this email." }
```

---

### GET `/api/otp/health/`

**Response (200):**
```json
{
  "status": "ok",
  "service": "Aurus AI OTP Service",
  "timestamp": "2026-07-23T11:27:00+05:30"
}
```

---

## Logo Switching

To change which logo appears in emails, update `settings.py`:

```python
# Options: 'logo_white', 'logo_black', 'aurus_white', 'aurus_black'
EMAIL_LOGO_KEY = 'logo_white'    # ← default (white logo, dark background)
```

| Key | File | Best Used When |
|---|---|---|
| `logo_white` | logo-white.jpeg | Dark background email (default) |
| `logo_black` | logo-black.jpeg | Light background email |
| `aurus_white` | aurus-white.jpeg | Full wordmark, dark bg |
| `aurus_black` | aurus-black.jpeg | Full wordmark, light bg |

---

## Troubleshooting

### ❌ "Authentication failed" or "Username and Password not accepted"
- You used your regular Gmail password instead of App Password
- Generate App Password at: https://myaccount.google.com/apppasswords
- 2FA must be enabled first

### ❌ "SMTPServerDisconnected" or connection timeout
- Port 587 might be blocked on your network (try from hotspot)
- Or try `EMAIL_PORT = 465` with `EMAIL_USE_SSL = True` (change in settings.py)

### ❌ Logo shows as attachment, not inline
- Check logo file exists in `otp_service/static/images/`
- Check filename matches exactly (case-sensitive)
- Check `EMAIL_LOGO_KEY` in settings.py

### ❌ "No module named 'decouple'"
- Run `pip install -r requirements.txt` again
- Make sure virtual environment is activated

### ❌ Logo shows in Gmail but not Zoho/Outlook
- CID embedding is working but client is filtering
- Open email and click "Display Images" or "Load Images"
- Forward the test email within Zoho and check rendering

---

## Handing Off to Boss (aurusai70@gmail.com)

When it's working on your side, these are the only changes needed:

1. Update `.env`:
   ```env
   EMAIL_HOST_USER=aurusai70@gmail.com
   EMAIL_HOST_PASSWORD=<boss's app password>
   DEFAULT_FROM_EMAIL=Aurus AI <aurusai70@gmail.com>
   ```

2. Generate new App Password on the boss's Google account (same steps as above)

3. Run `python manage.py test_email --to aurusai70@gmail.com`

4. Done ✅ — no code changes needed

---

## Admin Panel

View all OTP records:
1. Run: `python manage.py createsuperuser`
2. Open: http://localhost:8000/admin/
3. Login with your superuser credentials
4. Click **OTP Records** to see all sent OTPs, their status, and expiry

---

## Next Steps (For Production)

- [ ] Switch `DEBUG = False`
- [ ] Set a proper `SECRET_KEY`
- [ ] Restrict `ALLOWED_HOSTS` to your domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Add rate limiting per IP (currently 5/minute per endpoint)
- [ ] Add Celery for async email sending
- [ ] Add proper logging to file

