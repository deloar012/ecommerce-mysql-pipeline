# 🚀 ShopHub E-Commerce - Complete Setup Guide

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] Python 3.8 or higher installed
- [ ] MySQL 8.0 or higher installed and running
- [ ] pip package manager installed
- [ ] A text editor or IDE (VS Code recommended)

## 🔧 Step-by-Step Installation

### Step 1: Verify Python Installation

```bash
python --version
# Should show Python 3.8 or higher

pip --version
# Should show pip version
```

### Step 2: Verify MySQL Installation

```bash
mysql --version
# Should show MySQL version 8.0 or higher
```

Test MySQL connection:
```bash
mysql -u root -p
# Enter your MySQL password
```

### Step 3: Create MySQL Database

In MySQL command line:
```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verify database was created
SHOW DATABASES;

-- Exit MySQL
EXIT;
```

### Step 4: Navigate to Project Directory

```bash
cd "D:\1 E-Commerces"
```

### Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-3.0.0 flask-cors-4.0.0 mysql-connector-python-8.2.0 bcrypt-4.1.2 PyJWT-2.8.0 python-dotenv-1.0.0
```

### Step 6: Configure Database Connection

Open `backend/config.py` and update:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',              # Your MySQL username
    'password': 'YOUR_PASSWORD',  # Change this to your MySQL password
    'database': 'ecommerce_db',
    'port': 3306
}
```

### Step 7: Initialize Database

```bash
python init_database.py
```

**Expected output:**
```
==================================================
ShopHub E-Commerce Database Initialization
==================================================

1. Creating database tables...
✓ MySQL Connection Pool created successfully
✓ Database tables created successfully

2. Inserting sample products...
✓ Inserted 12 sample products

3. Inserting sample user...
✓ Inserted sample user (email: test@example.com, password: Test@1234)

==================================================
Database initialization complete!
==================================================

You can now:
1. Run the Flask app: python backend/app.py
2. Login with: test@example.com / Test@1234
3. Access API at: http://localhost:5000
```

### Step 8: Start the Flask Server

```bash
python backend/app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
Press CTRL+C to quit
```

### Step 9: Test the API

Open a new terminal and test:

```bash
curl http://localhost:5000/
```

**Expected response:**
```json
{
  "success": true,
  "message": "ShopHub E-Commerce API v1.0",
  "endpoints": {
    "auth": "/api/auth",
    "products": "/api/products",
    "cart": "/api/cart",
    "orders": "/api/orders",
    "payments": "/api/payments",
    "profile": "/api/profile"
  }
}
```

### Step 10: Open Frontend

**Option A: Direct File Opening**
1. Navigate to `D:\1 E-Commerces\frontend`
2. Double-click `index.html`

**Option B: Using Python Server (Recommended)**
```bash
cd frontend
python -m http.server 8000
```

Then open: http://localhost:8000

## ✅ Verification Checklist

After setup, verify everything works:

### Backend Tests:

1. **Health Check**
```bash
curl http://localhost:5000/health
```
Expected: `{"success": true, "status": "healthy"}`

2. **Get Products**
```bash
curl http://localhost:5000/api/products
```
Expected: JSON with 12 products

3. **Get Categories**
```bash
curl http://localhost:5000/api/products/categories
```
Expected: JSON with product categories

### Frontend Tests:

1. **Registration**
   - Go to: http://localhost:8000/register.html
   - Fill form with valid data
   - Should show verification code input

2. **Login**
   - Go to: http://localhost:8000/login.html
   - Use: test@example.com / Test@1234
   - Should redirect to home page

3. **Browse Products**
   - Go to: http://localhost:8000/index.html
   - Should see 12 sample products
   - Search should work

4. **Add to Cart**
   - Click "Add to Cart" on any product
   - Should show success message
   - Cart count should increase

## 🐛 Troubleshooting Common Issues

### Issue 1: "Module not found" Error

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue 2: MySQL Connection Error

**Check MySQL is running:**
```bash
# Windows
sc query MySQL80

# Linux
sudo systemctl status mysql
```

**Start MySQL if stopped:**
```bash
# Windows
net start MySQL80

# Linux
sudo systemctl start mysql
```

**Test connection:**
```bash
mysql -u root -p
```

### Issue 3: Port 5000 Already in Use

**Find and kill process:**

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:5000 | xargs kill -9
```

**Or use different port:**
Edit `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

### Issue 4: CORS Error in Browser

**Solution:**
1. Verify Flask-CORS is installed:
```bash
pip install flask-cors
```

2. Check `backend/app.py` has:
```python
from flask_cors import CORS
CORS(app)
```

### Issue 5: Database Tables Not Created

**Manual table creation:**
```bash
python
>>> from backend.models.db import init_database
>>> init_database()
```

### Issue 6: Email Verification Not Working

**For development:**
- Verification codes are displayed in the API response
- Check browser console for the code
- No actual email is sent in development mode

**To enable real emails:**
Edit `backend/config.py`:
```python
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-specific-password'  # Not regular password!
```

Then uncomment in `backend/routes/auth_routes.py`:
```python
# Change this:
# send_verification_email(email, code)

# To this:
send_verification_email(email, code)
```

### Issue 7: Products Not Showing

**Check database has products:**
```sql
mysql -u root -p
USE ecommerce_db;
SELECT COUNT(*) FROM products;
```

**If no products, re-run:**
```bash
python init_database.py
```

## 📊 Database Verification

Verify all tables were created:

```sql
mysql -u root -p
USE ecommerce_db;
SHOW TABLES;
```

**Expected tables:**
- addresses
- cart
- login_attempts
- order_items
- orders
- products
- users
- verification_codes

**Check sample data:**
```sql
-- Check users
SELECT email FROM users;

-- Check products
SELECT name, price, stock FROM products LIMIT 5;
```

## 🎯 Next Steps After Setup

1. **Register a New Account**
   - Go to register page
   - Use your real email
   - Complete verification

2. **Explore Products**
   - Browse catalog
   - Use search and filters
   - View product details

3. **Test Shopping Flow**
   - Add products to cart
   - Update quantities
   - Apply promo codes (try: SAVE10, SAVE20, WELCOME)
   - Complete checkout

4. **Test User Features**
   - Update profile
   - Change password
   - Add addresses
   - View order history

## 🔒 Security Notes

### For Development:
- Default passwords are weak (change them)
- Email verification codes are visible in API
- No rate limiting enabled
- Debug mode is ON

### For Production:
- Change all secret keys
- Enable real email sending
- Add rate limiting
- Set DEBUG = False
- Use HTTPS
- Add input sanitization
- Enable logging
- Add monitoring

## 📞 Support

If you encounter issues:

1. Check this troubleshooting guide
2. Verify all prerequisites are met
3. Check error messages in terminal
4. Verify MySQL is running
5. Check browser console for errors

## 🎉 Success!

If you can:
- ✅ Access http://localhost:5000 without errors
- ✅ See products in frontend
- ✅ Login with test account
- ✅ Add items to cart

**Congratulations! Your e-commerce platform is ready!** 🚀