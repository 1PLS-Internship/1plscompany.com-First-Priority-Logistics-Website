import json
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


services_content = [
    {
        "title": "Freight Services",
        "description": "Coordinated sea and land freight designed for hotel, retail, and food-service timelines.",
        "features": [
            "Routing options with contingency planning",
            "Driver briefings for special handling",
            "Status updates at pickup, port, and delivery",
        ],
        "tag": "Freight",
    },
    {
        "title": "Container Logistics (20' & 40')",
        "description": "FCL and LCL loading with verified seals, time-stamped photos, and yard coordination.",
        "features": [
            "FCL (Full Container Load) support",
            "LCL (Less-than-Container Load) consolidation",
            "Secure stacking and blocking for stability",
        ],
        "tag": "Containers",
    },
    {
        "title": "Customs Clearance & Bureau of Customs Documentation",
        "description": "Complete document preparation, submissions, and approvals to keep shipments compliant.",
        "features": [
            "Pre-clearance validation of invoices and permits",
            "Processing of duties, taxes, and exemptions",
            "Representation for Bureau of Customs approvals",
        ],
        "tag": "Compliance",
    },
    {
        "title": "Container Handling (20ft & 40ft)",
        "description": "On-site lift, staging, and secure latching for both 20-foot and 40-foot units.",
        "features": [
            "Calibrated equipment with safety checks",
            "Seal verification before dispatch",
            "Incident-free yard maneuvering",
        ],
        "tag": "Handling",
    },
    {
        "title": "Local Delivery Services",
        "description": "Scheduled drop-offs across Metro Manila with POD and courteous drivers.",
        "features": [
            "Pre-route alerts and ETAs",
            "Proof of delivery with signatures",
            "Refrigerated vehicle options",
        ],
        "tag": "Local",
    },
    {
        "title": "Same-day Delivery",
        "description": "Priority deliveries for time-sensitive cargo handled by trusted dispatch riders and drivers.",
        "features": [
            "Real-time dispatch coordination",
            "Direct-to-recipient confirmation",
            "After-hours support for urgent runs",
        ],
        "tag": "Express",
    },
]


events_content = [
    {
        "name": "Harbor Safety Summit",
        "date": "April 2024",
        "location": "Port Area, Manila",
        "status": "Past",
        "description": "Shared best practices on container locking, cargo integrity, and dock teamwork.",
    },
    {
        "name": "Client Partnership Night",
        "date": "June 2024",
        "location": "Makati",
        "status": "Past",
        "description": "Celebrated milestones with 1GPF and TVIP partners and aligned growth plans.",
    },
    {
        "name": "Fleet Readiness Drill",
        "date": "September 2024",
        "location": "Navotas",
        "status": "Upcoming",
        "description": "Hands-on readiness drill for drivers, mechanics, and logistics coordinators.",
    },
    {
        "name": "Team Building: Logistics Race",
        "date": "November 2024",
        "location": "Tagaytay",
        "status": "Upcoming",
        "description": "Crew challenges that simulate port-to-door handoffs to sharpen communication.",
    },
]


jobs_content = [
    {
        "title": "Logistics Coordinator",
        "summary": "Coordinate container schedules, driver dispatch, and client updates for daily runs.",
        "details": [
            "Comfortable working with port and warehouse teams",
            "Can draft clear status updates for clients",
            "Experience with customs or freight preferred",
        ],
    },
]


def store_entry(file_path: Path, entry: dict) -> None:
    data = []
    if file_path.exists():
        try:
            data = json.loads(file_path.read_text())
        except json.JSONDecodeError:
            data = []
    data.append(entry)
    file_path.write_text(json.dumps(data, indent=2))


def send_email(subject: str, body: str) -> tuple[bool, str]:
    host = os.getenv("SMTP_HOST")
    port = os.getenv("SMTP_PORT")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_SENDER")
    recipient = os.getenv("SMTP_RECEIVER")
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    if not all([host, port, sender, recipient]):
        return False, "SMTP settings are incomplete."

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content(body)

    try:
        with smtplib.SMTP(host, int(port)) as server:
            if use_tls:
                server.starttls()
            if user and password:
                server.login(user, password)
            server.send_message(message)
        return True, "Email sent."
    except Exception as exc:  # noqa: BLE001
        app.logger.warning("Email send failed: %s", exc)
        return False, str(exc)


@app.route("/")
def home():
    return render_template(
        "home.html",
        meta_title="First Priority Logistics Company | Reliable Freight & Customs",
        meta_description="Trusted logistics partner for freight, container handling, customs clearance, and same-day delivery in Metro Manila.",
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        meta_title="About | First Priority Logistics Company",
        meta_description="Learn about First Priority Logistics Company's history, leadership, and partnerships with 1GPF and TVIP.",
    )


@app.route("/services")
def services():
    return render_template(
        "services.html",
        services=services_content,
        meta_title="Services | Freight, Containers, Customs, and Delivery",
        meta_description="Explore freight services, FCL and LCL container logistics, customs clearance, and local delivery options.",
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    error_message = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message_body = request.form.get("message", "").strip()

        missing_fields = [field for field, value in {"Name": name, "Email": email, "Message": message_body}.items() if not value]
        if missing_fields:
            error_message = f"Please complete the following fields: {', '.join(missing_fields)}."
        else:
            email_sent, _status = send_email(
                subject=f"New inquiry from {name}",
                body=f"From: {name} <{email}>\n\n{message_body}",
            )

            entry = {"name": name, "email": email, "message": message_body}
            if not email_sent:
                store_entry(DATA_DIR / "messages.json", entry)
                flash("Message received. Email is offline, but we stored your details and will respond soon.")
            else:
                flash("Message sent successfully. We will get back to you shortly.")

            return redirect(url_for("contact"))

    return render_template(
        "contact.html",
        meta_title="Contact | First Priority Logistics Company",
        meta_description="Get in touch for freight quotes, customs documentation, and delivery coordination.",
        error_message=error_message,
    )


@app.route("/hiring", methods=["GET", "POST"])
def hiring():
    error_message = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message_body = request.form.get("message", "").strip()
        missing_fields = [field for field, value in {"Name": name, "Email": email, "Message": message_body}.items() if not value]
        if missing_fields:
            error_message = f"Please complete the following fields: {', '.join(missing_fields)}."
        else:
            store_entry(
                DATA_DIR / "applications.json",
                {"name": name, "email": email, "message": message_body},
            )
            flash("Application submitted. Our coordinators will reach out soon.")
            return redirect(url_for("hiring"))

    return render_template(
        "hiring.html",
        jobs=jobs_content,
        meta_title="Hiring | Careers at First Priority Logistics Company",
        meta_description="Apply for logistics coordinator and operations roles at First Priority Logistics Company.",
        error_message=error_message,
    )


@app.route("/events")
def events():
    return render_template(
        "events.html",
        events=events_content,
        meta_title="Events | First Priority Logistics Company",
        meta_description="See upcoming and past logistics and team-building events from First Priority Logistics Company.",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)), debug=True)
