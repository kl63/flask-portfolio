from flask import Flask, render_template, url_for, request, flash, redirect, jsonify
from dotenv import load_dotenv
import os
import requests
from flask_mail import Mail, Message
import openai  # You'll need to install this: pip install openai

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Add this to your .env file

# Configure Flask-Mail
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

# reCAPTCHA configuration
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

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
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        
        # Get the reCAPTCHA response from the form
        recaptcha_response = request.form.get('g-recaptcha-response')
        
        # Verify the reCAPTCHA response
        verify_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
        ).json()
        
        # For debugging
        print(f"reCAPTCHA verification result: {verify_response}")
        
        # Check if reCAPTCHA verification passed and score is acceptable
        if not verify_response.get('success', False) or verify_response.get('score', 0) < 0.5:
            flash("Our security check indicates you might be a bot. Please try again.")
            return redirect(url_for("contact"))
        
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
    
    return render_template("contact.html", recaptcha_site_key=RECAPTCHA_SITE_KEY)

# Add a new route to handle chat requests
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Custom system prompt with information about Kevin and the portfolio
    system_prompt = """You are Kevin Lin's helpful portfolio website assistant. 
    You can help users navigate the site, learn about Kevin's projects, background, skills, 
    and assist with any questions about contacting Kevin.
    
    About Kevin:
    - Developer, designer, and creator with experience in web development
    - Skilled in Python, Flask, HTML/CSS, and other web technologies
    - Portfolio showcases various projects including web applications and design work
    - Available for contact through the contact form or via social media links in the footer
    
    Website Sections:
    - Home: Introduction and overview
    - About: Kevin's background, skills, and experience
    - Projects: Showcase of Kevin's work
    - Contact: Form to reach out to Kevin
    
    Be friendly, helpful, and concise in your responses. If you don't know specific details
    about Kevin that aren't provided here, suggest the visitor check the About page or contact
    Kevin directly through the contact form.
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or your preferred model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )
        
        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return jsonify({"response": "Sorry, I'm having trouble connecting right now. Please try again later."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)