# backend/utils/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from datetime import datetime, timedelta

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "deloarhossen8172@gmail.com"  # Replace with your Gmail
SENDER_PASSWORD = "jvzi vcvt enyb aogc"   # Replace with your Gmail App Password

# Store verification codes temporarily (in production, use Redis or database)
verification_codes = {}

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))

def send_verification_email(recipient_email, code):
    """
    Send verification code via Gmail SMTP
    
    Args:
        recipient_email: Email address to send the code to
        code: 6-digit verification code
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "ShopHub - Email Verification Code"
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email

        # HTML email template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .code-box {{
                    background-color: #f8f9fa;
                    border: 2px dashed #667eea;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    margin: 30px 0;
                }}
                .code {{
                    font-size: 36px;
                    font-weight: bold;
                    color: #667eea;
                    letter-spacing: 8px;
                    font-family: 'Courier New', monospace;
                }}
                .info {{
                    color: #666;
                    font-size: 14px;
                    line-height: 1.6;
                    margin: 20px 0;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    color: #856404;
                }}
                .footer {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🛍️ ShopHub</h1>
                    <p>Email Verification</p>
                </div>
                <div class="content">
                    <h2>Welcome to ShopHub!</h2>
                    <p class="info">Thank you for registering with ShopHub. To complete your registration, please use the verification code below:</p>
                    
                    <div class="code-box">
                        <div class="code">{code}</div>
                        <p style="color: #999; margin-top: 10px;">This code will expire in 5 minutes</p>
                    </div>
                    
                    <p class="info">Enter this code on the registration page to verify your email address and activate your account.</p>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong><br>
                        If you didn't request this code, please ignore this email. Never share this code with anyone.
                    </div>
                </div>
                <div class="footer">
                    <p>© 2024 ShopHub E-Commerce. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Plain text version (fallback)
        text_content = f"""
        ShopHub - Email Verification
        
        Welcome to ShopHub!
        
        Your verification code is: {code}
        
        This code will expire in 5 minutes.
        
        If you didn't request this code, please ignore this email.
        
        © 2024 ShopHub E-Commerce
        """

        # Attach both HTML and plain text versions
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS encryption
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        
        print(f"✅ Verification email sent to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

def send_password_reset_email(recipient_email, reset_token):
    """
    Send password reset link via Gmail SMTP
    
    Args:
        recipient_email: Email address to send the reset link to
        reset_token: Password reset token
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "ShopHub - Password Reset Request"
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email

        # Reset link (adjust the URL to your frontend)
        reset_link = f"http://localhost:5000/reset-password.html?token={reset_token}"

        # HTML email template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 40px;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .info {{
                    color: #666;
                    font-size: 14px;
                    line-height: 1.6;
                    margin: 20px 0;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    color: #856404;
                }}
                .footer {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🛍️ ShopHub</h1>
                    <p>Password Reset Request</p>
                </div>
                <div class="content">
                    <h2>Reset Your Password</h2>
                    <p class="info">We received a request to reset your password. Click the button below to create a new password:</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_link}" class="button">Reset Password</a>
                    </div>
                    
                    <p class="info">This link will expire in 1 hour for security reasons.</p>
                    
                    <p class="info">If the button doesn't work, copy and paste this link into your browser:</p>
                    <p style="color: #667eea; word-break: break-all;">{reset_link}</p>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong><br>
                        If you didn't request a password reset, please ignore this email. Your password will remain unchanged.
                    </div>
                </div>
                <div class="footer">
                    <p>© 2024 ShopHub E-Commerce. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Plain text version (fallback)
        text_content = f"""
        ShopHub - Password Reset Request
        
        We received a request to reset your password.
        
        Click this link to reset your password:
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you didn't request a password reset, please ignore this email.
        
        © 2024 ShopHub E-Commerce
        """

        # Attach both versions
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        
        print(f"✅ Password reset email sent to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

def store_verification_code(email, code):
    """Store verification code with expiry time"""
    expiry_time = datetime.now() + timedelta(minutes=5)
    verification_codes[email] = {
        'code': code,
        'expiry': expiry_time
    }

def verify_code(email, code):
    """Verify if the code is correct and not expired"""
    if email not in verification_codes:
        return False
    
    stored_data = verification_codes[email]
    
    # Check if expired
    if datetime.now() > stored_data['expiry']:
        del verification_codes[email]
        return False
    
    # Check if code matches
    if stored_data['code'] == code:
        del verification_codes[email]  # Remove after successful verification
        return True
    
    return False

def cleanup_expired_codes():
    """Remove expired verification codes"""
    current_time = datetime.now()
    expired_emails = [
        email for email, data in verification_codes.items()
        if current_time > data['expiry']
    ]
    for email in expired_emails:
        del verification_codes[email]
