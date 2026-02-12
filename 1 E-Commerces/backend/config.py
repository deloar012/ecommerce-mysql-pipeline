import os
from datetime import timedelta

# Flask Configuration
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production-2024'
DEBUG = True

# Database Configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'deloar@8172'),  # CHANGE THIS!
    'database': os.environ.get('DB_NAME', 'ecommerce_db'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

# JWT Configuration
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production-2024'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# Email Configuration (for verification codes)
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'your-app-password')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@shophub.com')

# Security
PASSWORD_MIN_LENGTH = 9
PASSWORD_REQUIRE_LETTER = True
PASSWORD_REQUIRE_NUMBER = True
PASSWORD_REQUIRE_SPECIAL = True

# Verification
VERIFICATION_CODE_EXPIRY = 300  # 5 minutes in seconds
VERIFICATION_CODE_LENGTH = 6

# Login Security
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_DURATION = 900  # 15 minutes in seconds

# CORS Configuration
CORS_ORIGINS = [
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    'http://localhost:3000',
]

# File Upload
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Pagination
ITEMS_PER_PAGE = 12
MAX_ITEMS_PER_PAGE = 100