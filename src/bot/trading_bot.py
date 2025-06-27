"""Main trading bot class"""
import asyncio
import logging
from telebot.async_telebot import AsyncTeleBot

from ..api import SolanaAPI
from ..utils import DataManager
from ..handlers import BasicHandlers, TradingHandlers, InfoHandlers, PortfolioHandlers
from .callback_handlers import CallbackHandlers

logger = logging.getLogger(__name__)


class TradingBot:
    """Main trading bot class that orchestrates all components"""
    
    def __init__(self, bot_token: str, solana_rpc_url: str):
        self.bot = AsyncTeleBot(bot_token)
        self.solana = SolanaAPI(solana_rpc_url)
        self.data_manager = DataManager()
        
        # Initialize handlers
        self.basic_handlers = BasicHandlers(self.bot, self.solana, self.data_manager)
        self.trading_handlers = TradingHandlers(self.bot, self.solana, self.data_manager)
        self.info_handlers = InfoHandlers(self.bot, self.solana, self.data_manager)
        self.portfolio_handlers = PortfolioHandlers(self.bot, self.solana, self.data_manager)
        
        # Initialize callback handlers
        self.callback_handlers = CallbackHandlers(
            self.bot, self.solana, self.data_manager,
            self.trading_handlers, self.info_handlers, self.portfolio_handlers
        )
        
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all bot command and callback handlers"""
        
        # Basic commands
        @self.bot.message_handler(commands=['start'])
        async def start_command(message):
            await self.basic_handlers.handle_start_command(message)
        
        @self.bot.message_handler(commands=['help'])
        async def help_command(message):
            await self.basic_handlers.handle_help_command(message)
        
        # Trading commands
        @self.bot.message_handler(commands=['buy'])
        async def buy_command(message):
            await self.trading_handlers.handle_buy_command(message)
        
        @self.bot.message_handler(commands=['sell'])
        async def sell_command(message):
            await self.trading_handlers.handle_sell_command(message)
        
        # Info commands
        @self.bot.message_handler(commands=['search'])
        async def search_command(message):
            await self.info_handlers.handle_search_command(message)
        
        @self.bot.message_handler(commands=['price'])
        async def price_command(message):
            await self.info_handlers.handle_price_command(message)
        
        @self.bot.message_handler(commands=['info'])
        async def info_command(message):
            await self.info_handlers.handle_info_command(message)
        
        @self.bot.message_handler(commands=['market'])
        async def market_command(message):
            await self.info_handlers.handle_market_command(message)
        
        # Portfolio commands
        @self.bot.message_handler(commands=['balance'])
        async def balance_command(message):
            await self.portfolio_handlers.handle_balance_command(message)
        
        @self.bot.message_handler(commands=['portfolio'])
        async def portfolio_command(message):
            await self.portfolio_handlers.handle_portfolio_command(message)
        
        @self.bot.message_handler(commands=['positions'])
        async def positions_command(message):
            await self.portfolio_handlers.handle_positions_command(message)
        
        # Callback query handler
        @self.bot.callback_query_handler(func=lambda call: True)
        async def callback_query_handler(call):
            await self.callback_handlers.handle_callback_query(call)
    
    async def run(self):
        """Run the bot"""
        logger.info("Starting Solana Paper Trading Bot...")
        try:
            await self.bot.polling(non_stop=True)
        except Exception as e:
            logger.error(f"Bot error: {e}")
            raise
