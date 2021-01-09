# TODO: 
# Add more utils to the project
from threading import Thread
from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_async_email(app, msg):
    with app.app_context():
        sg = SendGridAPIClient(app.config['SENDGRID_API_KEY'])
        res = sg.send(msg)
            
# Function to send mail using SendGridAPIClient
# TODO: Write a better func to send email
def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Mail(from_email=app.config['FROM_EMAIL'], 
                    to_emails=to, 
                    subject=subject, html_content=template)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
