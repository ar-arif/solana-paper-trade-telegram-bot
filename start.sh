#!/bin/bash

# Solana Paper Trading Bot Startup Script
# This script activates the virtual environment and runs the bot

echo "🚀 Starting Solana Paper Trading Bot..."

# Change to the bot directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run setup.sh first to create the virtual environment."
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Copy .env.example to .env and set your TELEGRAM_BOT_TOKEN"
fi

# Install/update dependencies
echo "📦 Checking dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Run the bot
echo "🤖 Starting Telegram bot..."
python bot.py
