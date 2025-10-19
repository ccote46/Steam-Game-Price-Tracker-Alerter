import smtplib
from email.message import EmailMessage
import os


def send_email(subject, body, to, fromUsr):
    # Create the email
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = fromUsr
    msg["To"] = to
    msg.set_content(body)

    # Gmail SMTP settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL port

    # Your credentials
    email_address = os.getenv("EMAIL") #put your email here 
    app_password = os.getenv("GMAIL_APP_PWORD") #add your key here 

    # Send the email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
            smtp.login(email_address, app_password)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

    

