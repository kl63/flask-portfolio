from flask import Flask, render_template, url_for, request, flash, redirect
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Configure Flask-Mail
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    # Your projects list remains the same
    projects = [
        {
            "title": "Project 1",
            "description": "Description of your first project",
            "image": "img/project1.jpg",
            "technologies": ["Python", "Flask", "HTML/CSS"],
            "github": "https://github.com/yourusername/project1",
            "live": "https://project1-demo.com"
        },
        # ... other projects ...
    ]
    return render_template("projects.html", projects=projects)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        
        # Create email message
        msg = Message(
            subject=f"Portfolio Contact: {subject}",
            recipients=[os.getenv("MAIL_RECIPIENT", os.getenv("MAIL_USERNAME"))],
            body=f"""
New message from your portfolio website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
            """,
            sender=os.getenv("MAIL_DEFAULT_SENDER")
        )
        
        # Add reply-to header so you can reply directly to the sender
        msg.reply_to = email
        
        try:
            mail.send(msg)
            flash("Your message has been sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
            flash("An error occurred while sending your message. Please try again later.")
        
        return redirect(url_for("contact"))
        
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)