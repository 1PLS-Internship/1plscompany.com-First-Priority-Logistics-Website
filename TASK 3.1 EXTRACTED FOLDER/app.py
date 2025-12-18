from flask import Flask, render_template, request, redirect, url_for, flash
import os, json, smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MESSAGE_STORE = os.path.join(BASE_DIR, "messages.json")

def store_message(data):
    messages = []
    if os.path.exists(MESSAGE_STORE):
        with open(MESSAGE_STORE, "r") as f:
            messages = json.load(f)
    messages.append(data)
    with open(MESSAGE_STORE, "w") as f:
        json.dump(messages, f, indent=2)

def send_email(subject, body, sender):
    host = os.getenv("SMTP_HOST")
    port = os.getenv("SMTP_PORT")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")
    to = os.getenv("SMTP_TO")
    if not all([host, port, user, password, to]):
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP(host, int(port)) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
    return True

@app.route("/")
def home():
    return render_template("home.html", title="First Priority Logistics Company")

@app.route("/about")
def about():
    return render_template("about.html", title="About Us")

@app.route("/services")
def services():
    return render_template("services.html", title="Services")

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "message": request.form.get("message")
        }
        sent = send_email("New Contact Message", str(data), data["email"])
        if not sent:
            store_message(data)
        flash("Your message has been received. Thank you!")
        return redirect(url_for("contact"))
    return render_template("contact.html", title="Contact")

@app.route("/hiring", methods=["GET","POST"])
def hiring():
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "message": request.form.get("message")
        }
        store_message({"job_application": data})
        flash("Application submitted successfully.")
        return redirect(url_for("hiring"))
    return render_template("hiring.html", title="Hiring")

@app.route("/events")
def events():
    return render_template("events.html", title="Events")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
