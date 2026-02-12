"""
Complete Database Setup for ShopHub
Run this file to create all necessary tables
"""

import mysql.connector
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DB_CONFIG
from utils.password_hash import hash_password

def setup_database():
    """Create database and all tables"""
    
    print("\n" + "="*60)
    print("🚀 ShopHub Database Setup")
    print("="*60 + "\n")
    
    try:
        # Connect to MySQL server (without database)
        print("📡 Connecting to MySQL...")
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        cursor = conn.cursor()
        print("✅ Connected to MySQL successfully\n")
        
        # Create database
        print(f"📦 Creating database '{DB_CONFIG['database']}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        print("✅ Database created/selected\n")
        
        # Create users table
        print("👥 Creating 'users' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                mobile VARCHAR(20),
                password_hash VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                is_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_email (email)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Users table created")
        
        # Create verification_codes table (THIS WAS MISSING!)
        print("🔐 Creating 'verification_codes' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_codes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                code VARCHAR(10) NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                used BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_email (email),
                INDEX idx_code (code)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Verification codes table created")
        
        # Create products table
        print("📦 Creating 'products' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                category VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                stock INT DEFAULT 0,
                image_url VARCHAR(500),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_category (category),
                INDEX idx_price (price),
                INDEX idx_active (is_active)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Products table created")
        
        # Create orders table
        print("📋 Creating 'orders' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                order_number VARCHAR(50) UNIQUE NOT NULL,
                status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
                subtotal DECIMAL(10, 2) NOT NULL,
                shipping DECIMAL(10, 2) DEFAULT 0,
                tax DECIMAL(10, 2) DEFAULT 0,
                total DECIMAL(10, 2) NOT NULL,
                shipping_address JSON,
                payment_method VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id),
                INDEX idx_status (status),
                INDEX idx_order_number (order_number)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Orders table created")
        
        # Create order_items table
        print("📦 Creating 'order_items' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                product_name VARCHAR(255) NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                INDEX idx_order_id (order_id),
                INDEX idx_product_id (product_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Order items table created")
        
        # Create cart table
        print("🛒 Creating 'cart' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                UNIQUE KEY unique_user_product (user_id, product_id),
                INDEX idx_user_id (user_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Cart table created")
        
        # Create payments table
        print("💳 Creating 'payments' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                payment_method VARCHAR(50) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
                transaction_id VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                INDEX idx_order_id (order_id),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Payments table created")
        
        conn.commit()
        print("\n" + "="*60)
        print("✅ All tables created successfully!")
        print("="*60 + "\n")
        
        # Insert sample products
        print("📦 Checking for existing products...")
        cursor.execute("SELECT COUNT(*) as count FROM products")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("📦 Inserting sample products...")
            sample_products = [
                ('Wireless Headphones', 'Premium noise-cancelling wireless headphones with 30-hour battery life', 'electronics', 79.99, 25, '🎧'),
                ('Smart Watch', 'Fitness tracker with heart rate monitor and GPS', 'electronics', 199.99, 15, '⌚'),
                ('Running Shoes', 'Lightweight running shoes with advanced cushioning', 'sports', 89.99, 30, '👟'),
                ('Cotton T-Shirt', '100% organic cotton, comfortable and breathable', 'clothing', 24.99, 50, '👕'),
                ('Coffee Maker', 'Programmable coffee maker with thermal carafe', 'home', 129.99, 12, '☕'),
                ('Python Book', 'Complete guide to Python programming for beginners', 'books', 45.99, 20, '📚'),
                ('Bluetooth Speaker', 'Portable waterproof speaker with 12-hour battery', 'electronics', 59.99, 18, '🔊'),
                ('Yoga Mat', 'Non-slip exercise mat with carrying strap', 'sports', 34.99, 40, '🧘'),
                ('Laptop Backpack', 'Durable backpack with padded laptop compartment', 'accessories', 49.99, 22, '🎒'),
                ('Water Bottle', 'Insulated stainless steel bottle, 32oz', 'sports', 29.99, 35, '💧'),
                ('Desk Lamp', 'LED desk lamp with adjustable brightness', 'home', 39.99, 28, '💡'),
                ('Wireless Mouse', 'Ergonomic wireless mouse with precision tracking', 'electronics', 24.99, 45, '🖱️')
            ]
            
            cursor.executemany("""
                INSERT INTO products (name, description, category, price, stock, image_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, sample_products)
            conn.commit()
            print(f"✅ Inserted {len(sample_products)} sample products")
        else:
            print(f"ℹ️  Products table already has {count} products")
        
        # Create admin user
        print("\n👤 Checking for admin user...")
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE email = 'admin@shophub.com'")
        if cursor.fetchone()[0] == 0:
            admin_password = hash_password('Admin@123')
            cursor.execute("""
                INSERT INTO users (full_name, email, mobile, password_hash, is_verified)
                VALUES (%s, %s, %s, %s, %s)
            """, ('Admin User', 'admin@shophub.com', '+1234567890', admin_password, True))
            conn.commit()
            print("✅ Admin user created")
            print("   📧 Email: admin@shophub.com")
            print("   🔑 Password: Admin@123")
        else:
            print("ℹ️  Admin user already exists")
        
        # Summary
        print("\n" + "="*60)
        print("📊 DATABASE SUMMARY")
        print("="*60)
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"✅ {table_name}: {count} rows")
        
        print("\n" + "="*60)
        print("🎉 Database setup completed successfully!")
        print("="*60)
        print("\n📝 Next steps:")
        print("1. Start the server: python backend/run.py")
        print("2. Open browser: http://localhost:5000")
        print("3. Register a new account or login with admin credentials")
        print("\n" + "="*60 + "\n")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"\n❌ Database Error: {err}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure MySQL is running")
        print("2. Check your credentials in backend/config.py:")
        print(f"   Host: {DB_CONFIG['host']}")
        print(f"   User: {DB_CONFIG['user']}")
        print(f"   Port: {DB_CONFIG['port']}")
        print("3. Make sure the MySQL user has proper permissions")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = setup_database()
    if success:
        print("✅ Ready to go! Start your Flask server now.")
    else:
        print("❌ Setup failed. Please fix the errors above and try again.")