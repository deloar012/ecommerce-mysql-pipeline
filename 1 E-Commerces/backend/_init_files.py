"""
Create all necessary __init__.py files
Run this if you get import errors
"""

import os

def create_init_files():
    """Create __init__.py files in all necessary directories"""
    
    init_files = {
        'backend/__init__.py': '"""ShopHub E-Commerce Backend Package"""\n__version__ = "1.0.0"\n',
        'backend/models/__init__.py': '"""Database models package"""\n',
        'backend/routes/__init__.py': '"""API routes package"""\n',
        'backend/utils/__init__.py': '"""Utility functions package"""\n'
    }
    
    for filepath, content in init_files.items():
        # Ensure directory exists
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        
        # Create or update __init__.py
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created: {filepath}")
    
    print("\n✅ All __init__.py files created successfully!")

if __name__ == "__main__":
    print("Creating __init__.py files...\n")
    create_init_files()