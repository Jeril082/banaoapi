import logging
import os
import json
import requests

# Retrieve SendGrid API key from Azure Function environment variables
SENDGRID_API_KEY = os.getenv('banaoapi')
SENDGRID_API_URL = 'https://api.sendgrid.com/v3/mail/send'

def send_email(receiver_email, subject, body_text):
    headers = {
        'Authorization': f'Bearer {SENDGRID_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'personalizations': [
            {
                'to': [{'email': receiver_email}],
                'subject': subject,
            },
        ],
        'from': {'email': 'jeriljoseph02@gmail.com'},  
        'content': [{'type': 'text/plain', 'value': body_text}],
    }
    response = requests.post(SENDGRID_API_URL, headers=headers, json=data)
    return response.status_code == 202

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        receiver_email = req_body.get('receiver_email')
        subject = req_body.get('subject')
        body_text = req_body.get('body_text')

        if not receiver_email or not subject or not body_text:
            return func.HttpResponse(
                "Please provide receiver_email, subject, and body_text in the request body.",
                status_code=400
            )

        if send_email(receiver_email, subject, body_text):
            return func.HttpResponse("Email sent successfully.", status_code=200)
        else:
            return func.HttpResponse("Failed to send email.", status_code=500)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse("Internal server error.", status_code=500)
