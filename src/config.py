"""Configuration settings for the Solana Paper Trading Bot"""
import os
from decimal import Decimal

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, that's fine
    pass

# Bot Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
SOLANA_RPC_URL = os.getenv('SOLANA_RPC_URL', 'https://api.mainnet-beta.solana.com')
STARTING_BALANCE = Decimal(os.getenv('STARTING_BALANCE', '10.0'))
DATA_FILE = os.getenv('DATA_FILE', 'trading_data.json')

# API Configuration
DEXSCREENER_BASE_URL = 'https://api.dexscreener.com/latest/dex'
REQUEST_TIMEOUT = 10

# Trading Configuration
SOL_PRICE_USD = 100  # Default SOL price for calculations (can be fetched in real-time)

# Popular tokens for market overview
POPULAR_TOKENS = [
    ("BONK", "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"),
    ("WEN", "WENWENvqqNya429ubCdR81ZmD69brwQaaBYY6p3LCpk"),
    ("POPCAT", "7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr"),
    ("PNUT", "A8C3xuqscfmyLrte3VmTqrAq8kgMASius9AFNANwpump"),
]

# Market cap categories
MARKET_CAP_CATEGORIES = {
    'large': {'min': 1000000000, 'emoji': '🦄', 'name': 'Large Cap'},
    'mid': {'min': 100000000, 'emoji': '🐂', 'name': 'Mid Cap'},
    'small': {'min': 10000000, 'emoji': '🐱', 'name': 'Small Cap'},
    'micro': {'min': 1000000, 'emoji': '🐭', 'name': 'Micro Cap'},
    'nano': {'min': 0, 'emoji': '🦐', 'name': 'Nano Cap'},
}

# Trading thresholds
LIQUIDITY_THRESHOLDS = {
    'high': 100000,
    'medium': 10000,
}

VOLUME_THRESHOLDS = {
    'high': 50000,
    'medium': 5000,
}
