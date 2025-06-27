# Solana Meme Coin Paper Trading Telegram Bot 🚀

A modern, interactive Telegram bot for paper trading Solana meme coins without risking real money. Perfect for learning, testing strategies, or having fun with crypto trading!

## Features ✨

- 📈 **Paper Trading**: Trade with virtual SOL (no real money at risk)
- 🔍 **Smart Token Search**: Find Solana tokens by symbol or contract address
- 💰 **Portfolio Management**: Track your positions and P&L in real-time
- 📊 **Live Market Data**: Get current token prices from DexScreener API
- 🎯 **Advanced Position Tracking**: Detailed position management with entry prices
- 💾 **Persistent Storage**: Your trading data is saved between sessions
- 🎮 **Interactive UI**: Inline buttons for quick actions and navigation
- 📈 **Market Overview**: See trending tokens and market data
- 💡 **Price Alerts**: Set alerts for your favorite tokens
- 🔄 **Auto-refresh**: Real-time price updates in portfolio view

## Bot Commands 🤖

### Basic Commands
- `/start` - Initialize your account with starting balance
- `/help` - Show all available commands and navigation
- `/balance` - Quick portfolio overview with total value
- `/portfolio` - Detailed position breakdown with P&L

### Trading Commands
- `/search <symbol>` - Find tokens by symbol (e.g., `/search BONK`)
- `/buy <address> <amount>` - Buy tokens using contract address
- `/sell <address> <amount>` - Sell tokens from your portfolio
- `/info <address>` - Get detailed token information

### Market Commands
- `/market` - View trending tokens and market overview
- `/top` - See top performing tokens

## Setup Instructions 🛠️

### Quick Start (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd solana-paper-trade-telegram-bot
   ```

2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure your bot token**:
   ```bash
   nano .env
   # Add your bot token from @BotFather
   ```

4. **Start the bot**:
   ```bash
   ./start.sh
   ```

### Manual Setup

#### 1. Prerequisites

- Python 3.8+
- A Telegram account
- Internet connection

#### 2. Create a Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Choose a name and username for your bot
4. Save the bot token you receive

#### 3. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

#### 4. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file and add your bot token
nano .env
# Replace YOUR_BOT_TOKEN_HERE with your actual bot token from @BotFather
```

#### 5. Run the Bot

```bash
# Manual start (make sure virtual environment is activated)
source venv/bin/activate
python bot.py

# Or use the convenient start script
./start.sh
```

## Project Structure 📁

The bot now uses a modern, modular architecture:

```
solana-paper-trade-telegram-bot/
├── bot.py                      # Main entry point
├── start.sh                    # Startup script (activates venv)
├── setup.sh                    # Setup and installation script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── src/                       # Source code modules
│   ├── config.py             # Configuration and constants
│   ├── api/                  # External API integrations
│   │   └── solana_api.py    # Solana and DexScreener APIs
│   ├── bot/                  # Core bot logic
│   │   ├── trading_bot.py   # Main bot class
│   │   └── callback_handlers.py # Inline button handlers
│   ├── handlers/             # Command handlers
│   │   ├── basic_handlers.py    # Start, help commands
│   │   ├── trading_handlers.py  # Buy, sell commands
│   │   ├── info_handlers.py     # Search, info commands
│   │   └── portfolio_handlers.py # Balance, portfolio
│   ├── models/               # Data models
│   │   └── data_models.py   # Position, Account classes
│   └── utils/                # Utility functions
│       ├── data_manager.py  # Data persistence
│       ├── formatters.py    # Message formatting
│       └── validators.py    # Input validation
├── trading_data.json          # User data storage
└── main_old_backup.py        # Backup of original file
```

## Configuration Options ⚙️

You can customize the bot by editing the `.env` file:

- `TELEGRAM_BOT_TOKEN` - Your bot token from BotFather (required)
- `SOLANA_RPC_URL` - Solana RPC endpoint (optional, defaults to public mainnet)
- `STARTING_BALANCE` - Starting SOL balance for new users (optional, defaults to 10.0)

## How It Works 🔧

1. **Account Creation**: Each user gets a virtual account with starting SOL balance
2. **Token Search**: Uses DexScreener API to find Solana tokens by symbol or address
3. **Price Data**: Fetches real-time prices from DexScreener API
4. **Position Management**: Tracks buy/sell orders with entry prices and P&L calculation
5. **Data Persistence**: Saves all user data to `trading_data.json`
6. **Interactive UI**: Inline buttons for quick actions and seamless navigation

## Example Usage 📝

1. Start the bot: `/start`
2. Search for a token: `/search BONK` or `/search pump`
3. Buy tokens using contract address: `/buy DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263 1000`
4. Check your portfolio: `/portfolio`
5. Get token info: `/info DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263`
6. View market trends: `/market`
7. Sell when ready: `/sell DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263 500`

## API Endpoints Used 🌐

- **DexScreener API**: For token search, prices, and market data
- **Solana RPC**: For blockchain interaction and token validation
- **Token Lists**: For comprehensive token information

## Data Storage 💾

User data is stored locally in `trading_data.json`. This includes:
- SOL balances and total portfolio value
- Open positions with entry prices and current P&L
- Trading history and timestamps
- Account creation dates and user preferences

## Advanced Features 🌟

- **Interactive Buttons**: Use inline keyboards for quick trading actions
- **Real-time Updates**: Portfolio values update automatically
- **Market Analysis**: Get insights on trending tokens
- **Position Tracking**: Detailed P&L calculations with color coding
- **Error Handling**: Comprehensive error handling and user feedback
- **Modular Design**: Clean, maintainable code structure

## Limitations ⚠️

- This is **paper trading only** - no real money involved
- Prices are from DexScreener and may have slight delays
- Some tokens might not have price data available
- Bot requires internet connection for live data
- Limited to Solana blockchain tokens

## Security Notes 🔒

- Never share your bot token with anyone
- This bot doesn't handle real cryptocurrency
- All trading is simulated for educational purposes
- Your data is stored locally on your server

## Troubleshooting 🔧

### Common Issues:

1. **"Token not found"**: Try using the full contract address instead of symbol
2. **"Unable to fetch price"**: Token might not be listed on DexScreener
3. **Bot not responding**: Check your bot token and internet connection
4. **Import errors**: Make sure virtual environment is activated

### Setup Issues:

```bash
# If you get import errors, ensure you're in the virtual environment
source venv/bin/activate

# If dependencies fail to install
pip install --upgrade pip
pip install -r requirements.txt

# If the bot won't start
python -c "from src.config import BOT_TOKEN; print('Config OK')"
```

### Logs:

Check the console output for detailed error messages and bot activity.

## Development 👨‍💻

### Running in Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run with debug logging
LOG_LEVEL=DEBUG python bot.py
```

### Code Structure

The bot follows modern Python practices:
- **Async/await**: Full asynchronous operation
- **Type hints**: Comprehensive type annotations
- **Error handling**: Robust error handling throughout
- **Logging**: Detailed logging for debugging
- **Modular design**: Clean separation of concerns

## Contributing 🤝

Feel free to submit issues, feature requests, or pull requests!

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Future Enhancements 🚀

- [ ] Price alerts and notifications
- [ ] Trading statistics and analytics
- [ ] Export portfolio data
- [ ] Multi-language support
- [ ] Advanced chart integration
- [ ] Social features (leaderboards)

## Disclaimer ⚖️

This bot is for educational and entertainment purposes only. It simulates trading with virtual money and should not be considered financial advice. Always do your own research before making real investment decisions.

## License 📄

See the LICENSE file for details.

---

**Happy Paper Trading! 📈🎉**

*Made with ❤️ for the Solana community*
