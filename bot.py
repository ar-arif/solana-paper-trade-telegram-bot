"""
Solana Paper Trading Telegram Bot

A modern, interactive Telegram bot for paper trading Solana meme coins with real-time data.
"""
import asyncio
import logging
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import BOT_TOKEN, SOLANA_RPC_URL
from src.bot import TradingBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Main function to run the bot"""
    # Validate configuration
    if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ Error: Please set your Telegram bot token!")
        logger.error("Set the TELEGRAM_BOT_TOKEN environment variable or update the .env file")
        logger.error("Example: export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
        return
    
    logger.info("🚀 Initializing Solana Paper Trading Bot...")
    logger.info(f"📡 Solana RPC URL: {SOLANA_RPC_URL}")
    
    # Create and run the bot
    try:
        bot = TradingBot(BOT_TOKEN, SOLANA_RPC_URL)
        logger.info("✅ Bot initialized successfully!")
        logger.info("🔄 Starting polling...")
        
        await bot.run()
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        logger.error("Please check your configuration and try again.")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot shutdown completed")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)
