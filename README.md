# First Priority Logistics Company Website

A responsive Flask + Jinja2 website for First Priority Logistics Company with Tailwind styling, SEO meta tags, and working contact/hiring forms. Built and tested on **Python 3.12**.

## Features
- Pages: Home, About, Services, Events, Hiring, and Contact.
- Tailwind CSS via CDN with responsive navigation and accessible controls.
- JSON-LD organization schema, page-specific meta titles and descriptions.
- Contact form with SMTP support (falls back to local storage when email is offline).
- Hiring form storing applications locally.
- Sample hero and team-building images in `static/images/`.
- Dockerfile for containerized deployment on port 8000.

## Project Structure
```
app.py                # Flask app and routes
requirements.txt      # Python dependencies
templates/            # Jinja2 templates
static/css, js, images
config/README.md      # SMTP environment variable guidance
data/                 # Created at runtime for stored messages/applications
```

## Setup (local)
1. Ensure Python 3.12 is installed.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Configure SMTP using environment variables in a `.env` file (see `config/README.md`).
5. Run the app:
   ```bash
   flask --app app run --host 0.0.0.0 --port 8000
   ```

## Docker
Build and run the container (listening on port 8000):
```bash
docker build -t first-priority-logistics .
docker run -p 8000:8000 --env-file .env first-priority-logistics
```

## Contact Form Behavior
- If SMTP is fully configured, submissions are emailed to `SMTP_RECEIVER`.
- If SMTP is missing or fails, submissions are stored in `data/messages.json` with a success notice shown to the user.

### Test with curl
```bash
curl -X POST http://localhost:8000/contact \
  -d "name=Test User" \
  -d "email=test@example.com" \
  -d "message=Hello from curl"
```

## Hiring Applications
- Submissions are stored in `data/applications.json`.

## Environment Variables
See `config/README.md` for SMTP and Flask secret key options.

## License
Sample content provided for demonstration purposes.
