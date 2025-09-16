from flask import Flask, render_template, request
from flask_mail import Mail, Message # type: ignore
from dotenv import load_dotenv # type: ignore
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load environment variables
load_dotenv()

# Flask-Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USER")
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASS")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("EMAIL_USER")

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message_body = request.form['message']

    msg = Message(subject=f"New Contact from {name}",
                  recipients=[os.getenv("EMAIL_USER")],
                  body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_body}")

    try:
        mail.send(msg)
        return render_template("index.html", message="Thank you! I'll reach out shortly.")
    except Exception as e:
        print(f"Error: {e}")
        return render_template("index.html", message="Oops! Something went wrong.")
    

if __name__ == '__main__':
    app.run(debug=True)
