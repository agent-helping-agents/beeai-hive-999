#!/usr/bin/env python3
"""
Cash Activation Protocol - Automated Stripe → Supabase → Email Fulfillment
© 2025 Bakery Street Project

Architecture:
1. GitHub CLI authentication (non-interactive)
2. Clone/sync smoothoperator and email-agent repositories
3. Poll Stripe for completed checkout sessions
4. Generate personalized PDF documentation (Pandoc → WeasyPrint)
5. Provision Supabase user with custom JWT
6. Deliver via Gmail SMTP (PDF + API key)

WATERMARK: PRIMAX-AI-BSP-2025
"""

import os
import sys
import time
import subprocess
import requests
import smtplib
import jwt
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# ============================================================================
# CONFIGURATION & ENVIRONMENT LOADING
# ============================================================================

class Config:
    """Load and validate environment configuration"""

    def __init__(self):
        self.GH_TOKEN = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
        self.STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
        self.SUPABASE_URL = os.getenv('SUPABASE_URL')
        self.SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
        self.SUPABASE_JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET')
        self.GMAIL_EMAIL = os.getenv('GMAIL_EMAIL')
        self.GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

        # Poll interval in seconds
        self.POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', '60'))

        # Working directory for repos
        self.WORK_DIR = Path.home() / 'cash_activation_workspace'
        self.WORK_DIR.mkdir(exist_ok=True)

    def validate(self):
        """Validate all required credentials are present"""
        required = {
            'GH_TOKEN': self.GH_TOKEN,
            'STRIPE_SECRET_KEY': self.STRIPE_SECRET_KEY,
            'SUPABASE_URL': self.SUPABASE_URL,
            'SUPABASE_SERVICE_KEY': self.SUPABASE_SERVICE_KEY,
            'SUPABASE_JWT_SECRET': self.SUPABASE_JWT_SECRET,
            'GMAIL_EMAIL': self.GMAIL_EMAIL,
            'GMAIL_APP_PASSWORD': self.GMAIL_APP_PASSWORD
        }

        missing = [k for k, v in required.items() if not v]

        if missing:
            print(f"❌ Missing required environment variables: {', '.join(missing)}")
            print()
            print("Set them via:")
            for var in missing:
                print(f"  export {var}='your-value-here'")
            sys.exit(1)

        print("✅ All environment variables validated")
        return True


# ============================================================================
# GITHUB REPOSITORY AUTOMATION
# ============================================================================

class GitHubManager:
    """Handle GitHub CLI authentication and repository operations"""

    def __init__(self, config):
        self.config = config
        self.repos = ['smoothoperator', 'email-agent']

    def authenticate(self):
        """Non-interactive GitHub CLI authentication via token"""
        print("🔐 Authenticating with GitHub...")

        try:
            # Pipe token to gh auth login
            process = subprocess.Popen(
                ["gh", "auth", "login", "--with-token"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.config.WORK_DIR
            )

            stdout, stderr = process.communicate(input=self.config.GH_TOKEN)

            if process.returncode != 0:
                raise Exception(f"GitHub auth failed: {stderr}")

            # Configure HTTPS protocol for token usage
            subprocess.run(
                ["gh", "config", "set", "git_protocol", "https"],
                check=True,
                cwd=self.config.WORK_DIR
            )

            print("✅ GitHub CLI authenticated")
            return True

        except Exception as e:
            print(f"❌ GitHub authentication error: {e}")
            return False

    def sync_repositories(self):
        """Idempotent clone/pull of required repositories"""
        print("📦 Syncing repositories...")

        os.chdir(self.config.WORK_DIR)

        for repo in self.repos:
            repo_path = self.config.WORK_DIR / repo

            if repo_path.exists():
                print(f"  ↻ Updating {repo}...")
                try:
                    subprocess.run(
                        ["git", "-C", str(repo_path), "pull"],
                        check=False,
                        capture_output=True
                    )
                except Exception as e:
                    print(f"  ⚠️  Update failed for {repo}: {e}")
            else:
                print(f"  ⬇️  Cloning {repo}...")
                try:
                    subprocess.run(
                        ["gh", "repo", "clone", f"Bakery-street-project/{repo}"],
                        check=True,
                        cwd=self.config.WORK_DIR
                    )
                except Exception as e:
                    print(f"  ❌ Clone failed for {repo}: {e}")
                    return False

        print("✅ Repositories synchronized")
        return True


# ============================================================================
# STRIPE PAYMENT DETECTION
# ============================================================================

class StripeMonitor:
    """Poll Stripe for completed checkout sessions using cursor pagination"""

    def __init__(self, config):
        self.config = config
        self.checkpoint = None  # Cursor for pagination

    def initialize_checkpoint(self):
        """Get most recent session ID to establish starting point"""
        print("🔍 Initializing Stripe checkpoint...")

        try:
            import stripe
            stripe.api_key = self.config.STRIPE_SECRET_KEY

            # Fetch single most recent session
            sessions = stripe.checkout.Session.list(limit=1)

            if sessions.data:
                self.checkpoint = sessions.data[0].id
                print(f"✅ Checkpoint: {self.checkpoint}")
            else:
                print("ℹ️  No previous sessions found (new account)")

        except Exception as e:
            print(f"⚠️  Checkpoint initialization error: {e}")

    def poll_new_sessions(self):
        """Poll for new sessions created after checkpoint"""
        try:
            import stripe
            stripe.api_key = self.config.STRIPE_SECRET_KEY

            # Query sessions created after checkpoint
            if self.checkpoint:
                sessions = stripe.checkout.Session.list(
                    starting_after=self.checkpoint,
                    limit=100
                )
            else:
                sessions = stripe.checkout.Session.list(limit=100)

            # Filter for valid completed payments
            valid_sessions = [
                s for s in sessions.data
                if s.status == 'complete' and s.payment_status == 'paid'
            ]

            # Update checkpoint to latest session
            if sessions.data:
                self.checkpoint = sessions.data[0].id

            return valid_sessions

        except Exception as e:
            print(f"❌ Stripe polling error: {e}")
            return []


# ============================================================================
# PDF GENERATION PIPELINE
# ============================================================================

class PDFGenerator:
    """Generate personalized PDF documentation via Pandoc → WeasyPrint"""

    def __init__(self, config):
        self.config = config
        self.template_path = config.WORK_DIR / 'template.md'
        self.css_path = config.WORK_DIR / 'dark_mode.css'

        # Create default template if missing
        self._ensure_template()

    def _ensure_template(self):
        """Create default Markdown template with dark mode CSS"""

        if not self.template_path.exists():
            template = """# Welcome to Smoothoperator Access
**Customer:** {{ customer_name }}
**Activation Date:** {{ activation_date }}
**Transaction:** {{ session_id }}

---

## Your API Credentials

**API Key:**
```
{{ api_key }}
```

**Supabase URL:** `{{ supabase_url }}`

## Quick Start

1. Clone the repository:
   ```bash
   gh repo clone Bakery-street-project/smoothoperator
   ```

2. Configure your environment:
   ```bash
   export SUPABASE_URL="{{ supabase_url }}"
   export SUPABASE_KEY="{{ api_key }}"
   ```

3. Run the automation:
   ```bash
   python smoothoperator/main.py
   ```

## Support

Email: support@bakerystreet.dev
Documentation: https://github.com/Bakery-street-project/smoothoperator

---

© 2025 Bakery Street Project
PRIMAX-AI-BSP-2025
"""
            self.template_path.write_text(template)

        if not self.css_path.exists():
            css = """/* Forced Dark Mode for WeasyPrint PDF */
@page {
    size: A4;
    margin: 2.5cm;
    @top-right {
        content: "Cash Activation Protocol - Confidential";
        font-size: 9pt;
        color: #888;
    }
    @bottom-center {
        content: "Page " counter(page);
        font-size: 9pt;
    }
}

:root {
    --background-color: #1E1F21;
    --text-color: #EEEFF1;
    --accent-color: #00D9FF;
}

html {
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
}

h1, h2, h3 {
    color: var(--accent-color);
    border-bottom: 1px solid #333;
    padding-bottom: 0.3em;
}

code {
    background-color: #2A2B2D;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Monaco', 'Courier New', monospace;
}

pre {
    background-color: #2A2B2D;
    padding: 1em;
    border-left: 3px solid var(--accent-color);
    overflow-x: auto;
}
"""
            self.css_path.write_text(css)

    def generate(self, customer_name, customer_email, session_id, api_key):
        """Generate PDF from template with injected data"""
        print(f"📄 Generating PDF for {customer_name}...")

        try:
            # Read template
            template_content = self.template_path.read_text()

            # Inject variables
            content = template_content.replace('{{ customer_name }}', customer_name)
            content = content.replace('{{ activation_date }}', datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
            content = content.replace('{{ session_id }}', session_id)
            content = content.replace('{{ api_key }}', api_key)
            content = content.replace('{{ supabase_url }}', self.config.SUPABASE_URL)

            # Write populated markdown
            populated_md = self.config.WORK_DIR / f'activation_{session_id}.md'
            populated_md.write_text(content)

            # Convert Markdown → HTML via Pandoc
            html_path = self.config.WORK_DIR / f'activation_{session_id}.html'
            subprocess.run([
                'pandoc',
                str(populated_md),
                '-o', str(html_path),
                '--standalone'
            ], check=True)

            # Render HTML → PDF via WeasyPrint with dark CSS
            pdf_path = self.config.WORK_DIR / f'activation_{session_id}.pdf'

            # Install weasyprint if needed (via pip)
            try:
                from weasyprint import HTML, CSS
            except ImportError:
                print("  📦 Installing WeasyPrint...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'weasyprint'], check=True)
                from weasyprint import HTML, CSS

            HTML(filename=str(html_path)).write_pdf(
                str(pdf_path),
                stylesheets=[CSS(filename=str(self.css_path))]
            )

            print(f"✅ PDF generated: {pdf_path}")
            return pdf_path

        except Exception as e:
            print(f"❌ PDF generation error: {e}")
            return None


# ============================================================================
# SUPABASE USER PROVISIONING
# ============================================================================

class SupabaseManager:
    """Create users and mint custom JWT tokens"""

    def __init__(self, config):
        self.config = config

    def create_user(self, email, name, stripe_session_id):
        """Provision new user with email confirmation bypassed"""
        print(f"👤 Creating Supabase user for {email}...")

        try:
            from supabase import create_client

            supabase = create_client(
                self.config.SUPABASE_URL,
                self.config.SUPABASE_SERVICE_KEY
            )

            # Create user via Admin API
            response = supabase.auth.admin.create_user({
                'email': email,
                'email_confirm': True,  # Skip verification email
                'user_metadata': {
                    'name': name,
                    'stripe_session_id': stripe_session_id,
                    'plan': 'premium',
                    'activated_at': datetime.utcnow().isoformat()
                }
            })

            user_id = response.user.id
            print(f"✅ User created: {user_id}")
            return user_id

        except Exception as e:
            # User may already exist - try to fetch
            print(f"  ℹ️  User creation note: {e}")
            print(f"  → User may already exist, attempting fetch...")

            try:
                # Query existing user
                result = supabase.auth.admin.list_users()
                for user in result:
                    if user.email == email:
                        print(f"✅ Found existing user: {user.id}")
                        return user.id
            except Exception as fetch_error:
                print(f"❌ User fetch error: {fetch_error}")
                return None

    def mint_api_token(self, user_id):
        """Generate long-lived JWT for API access"""
        print(f"🔑 Minting API token for user {user_id}...")

        try:
            payload = {
                "role": "authenticated",
                "iss": "supabase",
                "aud": "authenticated",
                "sub": user_id,
                "exp": int(time.time()) + (365 * 24 * 60 * 60)  # 1 year validity
            }

            encoded_jwt = jwt.encode(
                payload,
                self.config.SUPABASE_JWT_SECRET,
                algorithm="HS256"
            )

            print("✅ JWT token generated")
            return encoded_jwt

        except Exception as e:
            print(f"❌ JWT generation error: {e}")
            return None


# ============================================================================
# EMAIL DELIVERY SYSTEM
# ============================================================================

class EmailDelivery:
    """Send MIME multipart emails via Gmail SMTP with PDF attachments"""

    def __init__(self, config):
        self.config = config

    def send_activation_email(self, to_email, customer_name, api_key, pdf_path):
        """Construct and send activation email with PDF attachment"""
        print(f"📧 Sending activation email to {to_email}...")

        try:
            # Construct MIME multipart message
            msg = MIMEMultipart('mixed')
            msg['From'] = self.config.GMAIL_EMAIL
            msg['To'] = to_email
            msg['Subject'] = "🎉 Your Smoothoperator Access is Ready!"

            # HTML body
            html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #00D9FF;">Welcome to Smoothoperator, {customer_name}!</h2>

    <p>Your premium access has been activated. Here's your API key:</p>

    <div style="background: #f4f4f4; padding: 15px; border-left: 4px solid #00D9FF; font-family: monospace;">
        <code style="color: #333;">{api_key}</code>
    </div>

    <h3>Quick Start</h3>
    <ol>
        <li>Download the attached PDF documentation</li>
        <li>Clone the repository: <code>gh repo clone Bakery-street-project/smoothoperator</code></li>
        <li>Set your API key in the environment</li>
        <li>Start automating!</li>
    </ol>

    <p><strong>Need help?</strong> Email us at support@bakerystreet.dev</p>

    <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
    <p style="color: #888; font-size: 0.9em;">
        © 2025 Bakery Street Project | PRIMAX-AI-BSP-2025
    </p>
</body>
</html>
"""

            msg.attach(MIMEText(html_body, 'html'))

            # Attach PDF
            if pdf_path and pdf_path.exists():
                with open(pdf_path, 'rb') as f:
                    pdf_attachment = MIMEBase('application', 'pdf')
                    pdf_attachment.set_payload(f.read())
                    encoders.encode_base64(pdf_attachment)
                    pdf_attachment.add_header(
                        'Content-Disposition',
                        f'attachment; filename="smoothoperator_activation.pdf"'
                    )
                    msg.attach(pdf_attachment)

            # Connect to Gmail SMTP (SSL on port 465)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.config.GMAIL_EMAIL, self.config.GMAIL_APP_PASSWORD)
                server.send_message(msg)

            print("✅ Email sent successfully")
            return True

        except Exception as e:
            print(f"❌ Email delivery error: {e}")
            return False


# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================

class CashActivationProtocol:
    """Main orchestration class binding all components"""

    def __init__(self):
        self.config = Config()
        self.github = GitHubManager(self.config)
        self.stripe = StripeMonitor(self.config)
        self.pdf_gen = PDFGenerator(self.config)
        self.supabase = SupabaseManager(self.config)
        self.email = EmailDelivery(self.config)

    def initialize(self):
        """Initialize all subsystems"""
        print("=" * 70)
        print("💰 CASH ACTIVATION PROTOCOL - INITIALIZING")
        print("=" * 70)
        print()

        # Validate configuration
        self.config.validate()
        print()

        # Authenticate GitHub
        if not self.github.authenticate():
            sys.exit(1)
        print()

        # Sync repositories
        if not self.github.sync_repositories():
            sys.exit(1)
        print()

        # Initialize Stripe checkpoint
        self.stripe.initialize_checkpoint()
        print()

        print("=" * 70)
        print("✅ INITIALIZATION COMPLETE - ENTERING EVENT LOOP")
        print("=" * 70)
        print()

    def process_session(self, session):
        """Execute full activation workflow for a single session"""
        print()
        print("🎯 NEW PAYMENT DETECTED")
        print(f"   Session: {session.id}")
        print(f"   Amount: ${session.amount_total / 100:.2f}")
        print()

        try:
            # Extract customer data
            customer_email = session.customer_details.email
            customer_name = session.customer_details.name or "Valued Customer"

            if not customer_email:
                print("⚠️  No customer email - skipping (requires manual intervention)")
                return False

            # 1. Create Supabase user
            user_id = self.supabase.create_user(
                customer_email,
                customer_name,
                session.id
            )

            if not user_id:
                print("❌ User provisioning failed - aborting")
                return False

            # 2. Mint API token
            api_key = self.supabase.mint_api_token(user_id)

            if not api_key:
                print("❌ Token generation failed - aborting")
                return False

            # 3. Generate PDF
            pdf_path = self.pdf_gen.generate(
                customer_name,
                customer_email,
                session.id,
                api_key
            )

            # 4. Send email
            email_sent = self.email.send_activation_email(
                customer_email,
                customer_name,
                api_key,
                pdf_path
            )

            if email_sent:
                print()
                print("=" * 70)
                print(f"✅ ACTIVATION COMPLETE: {customer_email}")
                print("=" * 70)
                return True
            else:
                print("⚠️  Email delivery failed - credentials issued but not sent")
                return False

        except Exception as e:
            print(f"❌ Session processing error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def run(self):
        """Main event loop - poll Stripe and process new sessions"""
        self.initialize()

        print(f"🔁 Polling every {self.config.POLL_INTERVAL} seconds...")
        print("   Press Ctrl+C to stop")
        print()

        try:
            while True:
                # Poll for new sessions
                new_sessions = self.stripe.poll_new_sessions()

                if new_sessions:
                    print(f"📬 Found {len(new_sessions)} new payment(s)")

                    for session in new_sessions:
                        self.process_session(session)

                # Sleep until next poll
                time.sleep(self.config.POLL_INTERVAL)

        except KeyboardInterrupt:
            print()
            print("⏹️  Cash Activation Protocol stopped by user")
            print()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    protocol = CashActivationProtocol()
    protocol.run()
