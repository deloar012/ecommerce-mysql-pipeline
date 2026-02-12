"""
Simple run script for ShopHub E-Commerce Platform
This handles the import paths correctly
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import and run the Flask app
from backend.app import app

if __name__ == "__main__":
    print("="*60)
    print("  ShopHub E-Commerce Platform")
    print("="*60)
    print("\n✓ Server starting...")
    print("✓ API available at: http://localhost:5000")
    print("✓ Press CTRL+C to stop\n")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)