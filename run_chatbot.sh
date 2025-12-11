#!/bin/bash

# Scientific Chatbot Launcher Script
# This script guides you through setting up and running the chatbot

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🔬 Scientific Chatbot - Claude AI Setup & Launch Guide  🔬   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Welcome! This script will guide you through running the chatbot."
echo ""

# Function to display a step
display_step() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "STEP $1: $2"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Function to display tips
display_tip() {
    echo "💡 TIP: $1"
    echo ""
}

# Function to display success
display_success() {
    echo "✅ $1"
    echo ""
}

# Function to display error
display_error() {
    echo "❌ $1"
    echo ""
}

# Function to display info
display_info() {
    echo "ℹ️  $1"
    echo ""
}

# Function to wait for user
wait_for_user() {
    echo "Press Enter to continue..."
    read -r
    echo ""
}

# Display introduction
display_step "1" "Introduction"
echo "This chatbot provides expert answers to scientific questions across"
echo "multiple domains including:"
echo "  • Chemistry 🧪"
echo "  • Physics ⚛️"
echo "  • Biology 🧬"
echo "  • Biochemistry 🔬"
echo "  • Physiology ❤️"
echo "  • Mathematics 📐"
echo "  • Geology 🌍"
echo "  • Electricity & Magnetism ⚡"
echo ""
display_tip "You can view the full README for detailed documentation anytime"
echo "Would you like to view the README now? (y/n)"
read -r view_readme
if [[ "$view_readme" == "y" || "$view_readme" == "Y" ]]; then
    if command -v less &> /dev/null; then
        less README.md
    elif command -v more &> /dev/null; then
        more README.md
    else
        cat README.md
    fi
    echo ""
fi

# Check if Python is installed
display_step "2" "Checking Python Installation"
if ! command -v python3 &> /dev/null; then
    display_error "Python 3 is not installed."
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
display_success "Python found: $PYTHON_VERSION"
display_tip "Python 3.8 or higher is required"
wait_for_user

# Check if virtual environment exists
display_step "3" "Setting Up Virtual Environment"
if [ ! -d "venv" ]; then
    display_info "A virtual environment isolates project dependencies"
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        display_success "Virtual environment created successfully"
    else
        display_error "Failed to create virtual environment"
        exit 1
    fi
else
    display_info "Virtual environment already exists"
fi
wait_for_user

# Activate virtual environment
display_step "4" "Activating Virtual Environment"
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -eq 0 ]; then
    display_success "Virtual environment activated"
else
    display_error "Failed to activate virtual environment"
    exit 1
fi
wait_for_user

# Install/update dependencies
display_step "5" "Installing Dependencies"
display_info "Installing required packages: streamlit, anthropic, python-dotenv"
echo "This may take a few moments..."
echo ""
pip install -q --upgrade pip
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    display_success "All dependencies installed successfully"
else
    display_error "Failed to install dependencies"
    exit 1
fi
wait_for_user

# Check for .env file and guide API key setup
display_step "6" "Configuring API Key"
if [ ! -f ".env" ]; then
    display_info "API Key Setup Required"
    echo "To use this chatbot, you need an Anthropic API key."
    echo ""
    echo "You have two options:"
    echo ""
    echo "Option 1: Create a .env file (Recommended)"
    echo "  • Get your API key from: https://console.anthropic.com/"
    echo "  • We'll create the .env file for you now"
    echo ""
    echo "Option 2: Enter it in the app later"
    echo "  • You can skip this step and enter your key in the app's sidebar"
    echo ""
    echo "Would you like to set up your API key now? (y/n)"
    read -r setup_api_key
    
    if [[ "$setup_api_key" == "y" || "$setup_api_key" == "Y" ]]; then
        echo ""
        echo "Please enter your Anthropic API key:"
        echo "(The key will not be displayed as you type)"
        read -rs api_key
        
        if [ -n "$api_key" ]; then
            echo "ANTHROPIC_API_KEY=$api_key" > .env
            display_success "API key saved to .env file"
            display_tip "Your API key is stored securely and will not be committed to git"
        else
            display_info "No API key entered. You can set it up later in the app"
        fi
    else
        display_info "Skipped API key setup. You can enter it in the app's sidebar"
    fi
else
    display_success ".env file already exists with your API key"
fi
echo ""
wait_for_user

# Pre-launch information
display_step "7" "Ready to Launch!"
echo "Everything is set up! Here's what you need to know:"
echo ""
echo "📱 Application Access:"
echo "   • The app will open at: http://localhost:8501"
echo "   • It should open automatically in your browser"
echo "   • If not, manually visit the URL above"
echo ""
echo "🎯 How to Use:"
echo "   1. Select a scientific domain (Chemistry, Physics, etc.)"
echo "   2. Ask your question in the chat input"
echo "   3. Get detailed answers from Claude AI"
echo ""
echo "⚙️  Controls:"
echo "   • Press Ctrl+C to stop the server"
echo "   • Close the browser tab to pause (server keeps running)"
echo "   • Run this script again to restart"
echo ""
echo "📚 Features:"
echo "   • Interactive chat with Claude AI"
echo "   • Category-based scientific domains"
echo "   • Helpful resource links"
echo "   • Chat history tracking"
echo ""
display_tip "First time? Check the sidebar for helpful resources and controls"
echo ""
echo "Ready to launch? (Press Enter to start)"
read -r

# Launch the application
display_step "8" "Launching Application"
echo "🚀 Starting Scientific Chatbot..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Server is starting... Please wait for your browser to open"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

streamlit run scientific_chatbot.py
