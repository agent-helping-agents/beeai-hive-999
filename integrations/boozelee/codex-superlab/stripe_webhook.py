#!/usr/bin/env python3
import os
import stripe
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import smtplib
from email.mime.text import MIMEText

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
DISCORD_INVITE = os.environ.get("DISCORD_INVITE_LINK")
SUPPORT_EMAIL = "kiliaanv2@gmail.com"

def send_onboarding_email(email):
    body = f'''
Hi,

Thank you for joining Codex SuperLab!

Access:
- Discord: {DISCORD_INVITE}
- Repo: https://github.com/BoozeLee/codex-superlab

Need help? Reply to this email.

- BoozeLee'''

    msg = MIMEText(body)
    msg['Subject'] = 'Welcome to Codex SuperLab!'
    msg['From'] = SUPPORT_EMAIL
    msg['To'] = email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SUPPORT_EMAIL, os.environ.get('SMTP_PASSWORD'))
        server.sendmail(SUPPORT_EMAIL, [email], msg.as_string())

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['content-length'])
        payload = self.rfile.read(content_length)
        sig = self.headers['stripe-signature']
        try:
            event = stripe.Webhook.construct_event(payload, sig, endpoint_secret)
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Webhook error')
            return

        if event['type'] == 'checkout.session.completed':
            email = event['data']['object']['customer_email']
            print(f"💸 Purchase: {email}")
            if DISCORD_INVITE:
                send_onboarding_email(email)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'success')

if __name__ == "__main__":
    os.chdir('/home/boozelee/codex-superlab')  # Ensure working dir
    server = HTTPServer(('0.0.0.0', 3000), WebhookHandler)
    print("Listening on port 3000 for Stripe webhooks")
    server.serve_forever()
