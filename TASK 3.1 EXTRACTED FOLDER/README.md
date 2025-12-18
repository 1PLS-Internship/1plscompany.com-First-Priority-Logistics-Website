# First Priority Logistics Company Website

## Tech
- Python 3.11
- Flask + Jinja2
- Tailwind CSS (CDN)

## Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

## Docker
docker build -t fplc .
docker run -p 8000:8000 fplc

## Contact Form
Uses SMTP if configured, otherwise stores messages in messages.json
