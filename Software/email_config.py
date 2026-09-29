# ===== EMAIL CONFIGURATION =====
# Users can edit these settings to configure CPM report sending

# Email settings for sending reports
SENDER_EMAIL = "your_email@gmail.com"  # Your email address
SENDER_PASSWORD = "your_app_password"  # Gmail app-specific password (not your regular password!)
RECIPIENT_EMAIL = "your_email@gmail.com"  # Where to send reports
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Report settings
INCLUDE_SCREENSHOTS = False  # Set to True to include screenshots in report
REPORT_FORMAT = "csv"  # 'csv' or 'both' (csv + summary)

# Optional: Add your name to reports
USER_NAME = "User"

# ===== INSTRUCTIONS =====
# For Gmail:
# 1. Go to myaccount.google.com
# 2. Enable 2-Step Verification
# 3. Go to myaccount.google.com/apppasswords
# 4. Select "Mail" and "Windows Computer"
# 5. Copy the generated password and paste it in SENDER_PASSWORD above
#
# For Outlook/Hotmail:
# SMTP_SERVER = "smtp-mail.outlook.com"
# SMTP_PORT = 587
#
# For Yahoo:
# SMTP_SERVER = "smtp.mail.yahoo.com"
# SMTP_PORT = 587
