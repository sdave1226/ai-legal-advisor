import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print(" Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f" Error installing requirements: {e}")
        return False
    return True

def run_streamlit_app():
    """Run the Streamlit application"""
    try:
        print(" Starting AI Legal Advisor...")
        print(" The application will open in your default web browser")
        print(" URL: http://localhost:8501")
        print("\n Important: This is for educational purposes only!")
        print(" Press Ctrl+C to stop the application")
        
        # Set encoding for Windows
        if os.name == 'nt':
            os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        subprocess.run([sys.executable, "-m", "streamlit", "run", "ai_legal_advisor.py"])
    except KeyboardInterrupt:
        print("\n AI Legal Advisor stopped. Thank you for using our service!")

if __name__ == "__main__":
    print(" AI Legal Advisor Setup")
    print("=" * 50)
    
    # Install requirements
    if install_requirements():
        print("\n" + "=" * 50)
        run_streamlit_app()
    else:
        print("❌ Setup failed. Please check your Python environment.")
