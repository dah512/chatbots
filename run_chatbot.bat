@echo off
REM Scientific Chatbot Launcher Script for Windows

echo 🔬 Scientific Chatbot - Claude AI
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📥 Installing dependencies...
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ✅ Dependencies installed
echo.

REM Check for .env file
if not exist ".env" (
    echo ⚠️  No .env file found. You can:
    echo    1. Create a .env file with your ANTHROPIC_API_KEY
    echo    2. Enter your API key in the app's sidebar
    echo.
)

REM Launch the application
echo 🚀 Launching Scientific Chatbot...
echo    The app will open in your browser at http://localhost:8501
echo.
echo    Press Ctrl+C to stop the server
echo.

streamlit run scientific_chatbot.py

pause
