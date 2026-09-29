import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import email_config as email_cfg
from datetime import datetime

def send_cpm_report():
    """
    Send the latest CPM statistics CSV file via email
    Returns: (success: bool, message: str)
    """
    try:
        # Get the latest CSV file
        csv_file = os.path.join("analytics", "cpm_statistics.csv")

        if not os.path.exists(csv_file):
            return False, "No CPM data to send. Please complete a Time-In/Out session first."

        # Check if email is configured
        if email_cfg.SENDER_EMAIL == "your_email@gmail.com" or email_cfg.SENDER_PASSWORD == "your_app_password":
            return False, "Email not configured. Please edit email_config.py with your email details."

        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_cfg.SENDER_EMAIL
        msg['To'] = email_cfg.RECIPIENT_EMAIL
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = f"CPM Report - {email_cfg.USER_NAME} - {datetime.now().strftime('%Y-%m-%d')}"

        # Email body
        body = f"""
Hi,

Please find attached the CPM (Characters Per Minute) tracking report for {email_cfg.USER_NAME}.

Session Statistics:
- Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Report Location: {csv_file}

The CSV file contains detailed session information including:
- Date and time
- Total work time
- Keystrokes
- CPM (Characters Per Minute)
- Break information

Best regards,
MEDA: InOut Application
        """

        msg.attach(MIMEText(body, 'plain'))

        # Attach CSV file
        with open(csv_file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(csv_file)}')
            msg.attach(part)

        # Send email
        server = smtplib.SMTP(email_cfg.SMTP_SERVER, email_cfg.SMTP_PORT)
        server.starttls()
        server.login(email_cfg.SENDER_EMAIL, email_cfg.SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True, f"✓ Report sent successfully to {email_cfg.RECIPIENT_EMAIL}"

    except FileNotFoundError:
        return False, "CSV file not found. Please complete a session first."
    except smtplib.SMTPAuthenticationError:
        return False, "Email authentication failed. Check your email and app password in email_config.py"
    except smtplib.SMTPException as e:
        return False, f"Email sending failed: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def send_monthly_report():
    """
    Send all session data as a consolidated report
    Returns: (success: bool, message: str)
    """
    try:
        csv_file = os.path.join("analytics", "cpm_statistics.csv")

        if not os.path.exists(csv_file):
            return False, "No data available to send."

        if email_cfg.SENDER_EMAIL == "your_email@gmail.com":
            return False, "Email not configured in email_config.py"

        msg = MIMEMultipart()
        msg['From'] = email_cfg.SENDER_EMAIL
        msg['To'] = email_cfg.RECIPIENT_EMAIL
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = f"Monthly CPM Report - {email_cfg.USER_NAME}"

        # Read CSV and create summary
        with open(csv_file, 'r') as f:
            lines = f.readlines()
            session_count = len(lines) - 1  # Exclude header

        body = f"""
Monthly CPM Report

User: {email_cfg.USER_NAME}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Sessions: {session_count}

See attached CSV for detailed statistics.
        """

        msg.attach(MIMEText(body, 'plain'))

        # Attach CSV
        with open(csv_file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= monthly_cpm_report.csv')
            msg.attach(part)

        # Send
        server = smtplib.SMTP(email_cfg.SMTP_SERVER, email_cfg.SMTP_PORT)
        server.starttls()
        server.login(email_cfg.SENDER_EMAIL, email_cfg.SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True, "Monthly report sent successfully!"

    except Exception as e:
        return False, f"Failed to send report: {str(e)}"
