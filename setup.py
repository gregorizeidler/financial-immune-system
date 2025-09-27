#!/usr/bin/env python3
"""
Financial Immune System - Setup Script
======================================

Easy setup and launch script for the Financial Immune System.
"""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3.8, 0):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False


def run_demo():
    """Run the interactive demo"""
    print("\n🚀 Launching Financial Immune System Demo...")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, "demo.py"])
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error running demo: {e}")


def run_dashboard():
    """Run the web dashboard"""
    print("\n🌐 Launching Web Dashboard...")
    print("=" * 60)
    print("The dashboard will open in your web browser.")
    print("If it doesn't open automatically, go to: http://localhost:8501")
    print()
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")


def show_menu():
    """Show the main menu"""
    print("\n🦠 FINANCIAL IMMUNE SYSTEM - SETUP & LAUNCHER")
    print("=" * 60)
    print("Choose an option:")
    print()
    print("1. 🧪 Run Interactive Demo")
    print("2. 🌐 Launch Web Dashboard")
    print("3. 📦 Install/Update Requirements")
    print("4. ℹ️  Show System Information")
    print("5. 🚪 Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                run_demo()
                break
            elif choice == "2":
                run_dashboard()
                break
            elif choice == "3":
                install_requirements()
                input("\nPress Enter to return to menu...")
                show_menu()
                break
            elif choice == "4":
                show_system_info()
                input("\nPress Enter to return to menu...")
                show_menu()
                break
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break


def show_system_info():
    """Show system information"""
    print("\n📊 SYSTEM INFORMATION")
    print("-" * 30)
    
    # Python version
    print(f"Python Version: {sys.version.split()[0]}")
    
    # Current directory
    print(f"Working Directory: {os.getcwd()}")
    
    # Check if files exist
    required_files = [
        "financial_immune_system.py",
        "immune_system_app.py", 
        "dashboard.py",
        "demo.py",
        "requirements.txt",
        "README.md"
    ]
    
    print("\nCore Files:")
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")
    
    # Check installed packages
    print("\nKey Dependencies:")
    key_packages = ["numpy", "pandas", "streamlit", "plotly"]
    
    for package in key_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (not installed)")


def main():
    """Main setup function"""
    print("🦠 Financial Immune System - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if we're in the right directory
    if not Path("financial_immune_system.py").exists():
        print("❌ Error: Core system files not found")
        print("Please run this script from the FRAUDPLD directory")
        sys.exit(1)
    
    print("✅ System files found")
    
    # Check if requirements are installed
    try:
        import numpy, pandas, streamlit, plotly
        print("✅ Core dependencies available")
        show_menu()
    except ImportError:
        print("⚠️  Some dependencies are missing")
        print("Would you like to install them now? (y/n): ", end="")
        
        if input().lower().startswith('y'):
            if install_requirements():
                show_menu()
            else:
                print("❌ Setup failed. Please install dependencies manually:")
                print("pip install -r requirements.txt")
        else:
            print("📝 To install dependencies later, run:")
            print("pip install -r requirements.txt")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        print("Please check the installation and try again")
