import re
from backend.config import (
    PASSWORD_MIN_LENGTH,
    PASSWORD_REQUIRE_LETTER,
    PASSWORD_REQUIRE_NUMBER,
    PASSWORD_REQUIRE_SPECIAL
)

def validate_email(email: str) -> tuple[bool, str]:
    """Validate email format"""
    if not email:
        return False, "Email is required"
    
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False, "Invalid email format"
    
    return True, ""

def validate_mobile(mobile: str) -> tuple[bool, str]:
    """Validate mobile number"""
    if not mobile:
        return False, "Mobile number is required"
    
    # Remove spaces and special characters
    cleaned_mobile = re.sub(r'[\s\-\(\)]', '', mobile)
    
    # Check if it contains only digits and optional + at start
    if not re.match(r'^\+?\d{10,15}$', cleaned_mobile):
        return False, "Invalid mobile number (10-15 digits required)"
    
    return True, ""

def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    
    if len(password) < PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"
    
    if PASSWORD_REQUIRE_LETTER and not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter"
    
    if PASSWORD_REQUIRE_NUMBER and not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if PASSWORD_REQUIRE_SPECIAL and not re.search(r'[@$!%*?&#]', password):
        return False, "Password must contain at least one special character (@$!%*?&#)"
    
    return True, ""

def validate_full_name(name: str) -> tuple[bool, str]:
    """Validate full name"""
    if not name:
        return False, "Full name is required"
    
    if len(name) < 3:
        return False, "Name must be at least 3 characters long"
    
    if not re.match(r'^[a-zA-Z\s]+$', name):
        return False, "Name can only contain letters and spaces"
    
    return True, ""

def validate_required_field(value, field_name: str) -> tuple[bool, str]:
    """Validate required field"""
    if not value or (isinstance(value, str) and not value.strip()):
        return False, f"{field_name} is required"
    return True, ""

def validate_price(price) -> tuple[bool, str]:
    """Validate price"""
    try:
        price_float = float(price)
        if price_float < 0:
            return False, "Price cannot be negative"
        return True, ""
    except (ValueError, TypeError):
        return False, "Invalid price format"

def validate_quantity(quantity) -> tuple[bool, str]:
    """Validate quantity"""
    try:
        qty = int(quantity)
        if qty < 1:
            return False, "Quantity must be at least 1"
        return True, ""
    except (ValueError, TypeError):
        return False, "Invalid quantity format"