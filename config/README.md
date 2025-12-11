# SMTP and App Configuration

Set these environment variables (e.g., in a `.env` file) to enable email sending:

```
SMTP_HOST=smtp.yourprovider.com
SMTP_PORT=587
SMTP_USER=your_username
SMTP_PASSWORD=your_password
SMTP_SENDER=notifications@firstprioritylogistics.com
SMTP_RECEIVER=operations@firstprioritylogistics.com
SMTP_USE_TLS=true
FLASK_SECRET_KEY=change-this-secret
PORT=8000
```

If SMTP variables are missing, contact form submissions are stored in `data/messages.json` and a friendly success message is shown. Hiring applications are stored in `data/applications.json`.
