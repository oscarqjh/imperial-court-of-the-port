#!/usr/bin/env python3
"""
Script to install missing async database dependencies
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Install missing async database dependencies"""
    print("🔧 Installing missing async database dependencies...")
    
    # Required packages for async database operations
    packages = [
        "asyncpg>=0.28.0",           # For postgresql+asyncpg://
        "psycopg[async]>=3.1.0",    # For postgresql+psycopg://
        "crewai>=0.22.0",           # CrewAI framework
        "crewai-tools>=0.4.0",      # CrewAI tools
    ]
    
    all_success = True
    
    for package in packages:
        print(f"\n📦 Installing {package}...")
        if not install_package(package):
            all_success = False
    
    if all_success:
        print("\n✅ All packages installed successfully!")
        print("💡 You may need to restart your application for changes to take effect.")
    else:
        print("\n❌ Some packages failed to install. Please check the error messages above.")
    
    return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
