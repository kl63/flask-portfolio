from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return "<h2>All About Kevin Lin</h2><p>This is your Flask-powered Pi server 🎉 (COMING SOON!!)</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
