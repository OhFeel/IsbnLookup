#!/usr/bin/env python3
"""
Setup script for ISBN Lookup Tool
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def create_sample_files():
    """Create sample input files if they don't exist"""
    if not os.path.exists("isbn.txt"):
        print("Creating sample isbn.txt file...")
        with open("isbn.txt", "w") as f:
            f.write("# Add your ISBN numbers here, one per line\n")
            f.write("# Example ISBNs (you can remove these):\n")
            f.write("9780132350884\n")
            f.write("9780134685991\n")
            f.write("9781449355739\n")
        print("✅ Sample isbn.txt created")
    
    print("✅ Setup complete!")

def main():
    """Main setup function"""
    print("Setting up ISBN Lookup Tool...")
    
    if not install_requirements():
        sys.exit(1)
    
    create_sample_files()
    
    print("\nSetup complete! You can now:")
    print("1. Edit isbn.txt to add your ISBN numbers")
    print("2. Run: python isbn_lookup.py")
    print("3. Or test single ISBN: python isbn_lookup.py 9780132350884")

if __name__ == "__main__":
    main()
