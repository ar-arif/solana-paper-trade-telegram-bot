#!/bin/bash

echo "🚀 Setting up Solana Paper Trading Telegram Bot"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check Python version (require 3.8+)
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "❌ Python 3.8+ is required. Current version: $python_version"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "⚙️ Creating environment configuration..."
        cp .env.example .env
        echo "❗ Please edit .env file and add your Telegram bot token!"
        echo "   Get your bot token from @BotFather on Telegram"
    else
        echo "⚙️ Creating .env file from template..."
        cat > .env << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# Solana Configuration
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

# Trading Configuration
STARTING_BALANCE=10.0

# Logging Configuration
LOG_LEVEL=INFO
EOF
        echo "❗ Please edit .env file and add your Telegram bot token!"
        echo "   Get your bot token from @BotFather on Telegram"
    fi
else
    echo "✅ .env file already exists"
fi

# Make scripts executable
chmod +x start.sh 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your bot token:"
echo "   nano .env"
echo "2. Start the bot:"
echo "   ./start.sh"
echo ""
echo "Alternative manual start:"
echo "   source venv/bin/activate && python bot.py"
echo ""
echo "Need help? Check the README.md file!"
