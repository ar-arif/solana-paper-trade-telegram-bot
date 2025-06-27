"""Basic command handlers (start, help)"""
import logging
from telebot import types

from ..config import STARTING_BALANCE

logger = logging.getLogger(__name__)


class BasicHandlers:
    """Handles basic commands like start and help"""
    
    def __init__(self, bot, solana_api, data_manager):
        self.bot = bot
        self.solana = solana_api
        self.data_manager = data_manager
    
    async def handle_start_command(self, message):
        """Handle /start command"""
        try:
            user_id = message.from_user.id
            account = self.data_manager.get_or_create_account(user_id)
            
            welcome_text = f"""🚀 <b>Welcome to Solana Paper Trading Bot!</b>

📈 <b>REAL-TIME MEME COIN TRADING</b>
Trade popular Solana tokens with live DexScreener data, comprehensive market analysis, and interactive buttons!

🎯 <b>KEY FEATURES:</b>
• 🔄 <b>Live Prices</b> - Real-time DexScreener integration
• 📊 <b>Market Analysis</b> - MC, volume, liquidity, signals
• 🎮 <b>Interactive UI</b> - Tap buttons for instant actions
• 📱 <b>Smart Trading</b> - Contract address-based trading
• 💎 <b>Portfolio Tracking</b> - Real-time PnL and analytics

💰 <b>Starting Balance:</b> {STARTING_BALANCE} SOL

🚀 <b>QUICK START:</b>
1️⃣ /market - See trending tokens with quick actions
2️⃣ /search &lt;symbol&gt; - Find any token (sorted by market cap)  
3️⃣ Tap token buttons for instant buy/info actions
4️⃣ /portfolio - Track your positions &amp; PnL

💡 <b>Use interactive buttons throughout the bot for faster trading!</b>
📊 <b>All data is real-time from DexScreener API</b>

Type /help for full command list or /market to start trading!

Happy trading! 🎯
            """
            
            # Add quick start buttons
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("📈 Market", callback_data="market"),
                types.InlineKeyboardButton("💰 Portfolio", callback_data="portfolio")
            )
            markup.add(
                types.InlineKeyboardButton("🔍 Search Help", callback_data="help_search"),
                types.InlineKeyboardButton("💡 Buy Guide", callback_data="help_buy")
            )
            
            await self.bot.reply_to(message, welcome_text, parse_mode='HTML', reply_markup=markup)
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await self.bot.reply_to(message, "❌ Error processing start command.")
    
    async def handle_help_command(self, message):
        """Handle /help command"""
        try:
            help_text = """🤖 <b>Solana Paper Trading Bot Commands</b>

🎯 <b>TRADING COMMANDS:</b>
• /search &lt;symbol&gt; - Find tokens (sorted by market cap)
• /info &lt;address&gt; - Comprehensive token analysis
• /price &lt;address&gt; - Real-time price + 24h change
• /buy &lt;address&gt; &lt;amount_in_sol&gt; - Buy tokens (SOL amount)
• /sell &lt;address&gt; &lt;percentage%&gt; - Sell tokens (percentage)

📊 <b>PORTFOLIO COMMANDS:</b>
• /balance - Quick portfolio overview
• /positions - List positions with addresses
• /portfolio - Detailed portfolio view (table format)
• /market - Market overview of popular tokens

📈 <b>INTERACTIVE FEATURES:</b>
• 🎮 <b>Quick Action Buttons</b> - Instant buy/sell/info
• 📊 <b>Real-time Data</b> - Live DexScreener integration
• 🎯 <b>Smart Sorting</b> - Results by market cap
• 💡 <b>Trading Signals</b> - Liquidity &amp; volume analysis
• 📱 <b>Modern UI</b> - Tap buttons for fast actions

💡 <b>EXAMPLES:</b>
• /search BONK (find BONK token)
• /buy &lt;address&gt; 1.5 (buy with 1.5 SOL)
• /sell &lt;address&gt; 50% (sell 50% of position)
• /portfolio (view table format)
• Tap any token button for instant actions!

🚀 <b>Pro Tips:</b>
• Use buttons instead of typing commands
• Check liquidity before big trades
• Results sorted by market cap
• All data is real-time from DexScreener!
            """
            
            # Add help navigation buttons
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("📈 Try Market", callback_data="market"),
                types.InlineKeyboardButton("🔍 Search Guide", callback_data="help_search")
            )
            markup.add(
                types.InlineKeyboardButton("💰 Buy Guide", callback_data="help_buy"),
                types.InlineKeyboardButton("💼 Portfolio", callback_data="portfolio")
            )
            
            await self.bot.reply_to(message, help_text, parse_mode='HTML', reply_markup=markup)
            
        except Exception as e:
            logger.error(f"Error in help command: {e}")
            await self.bot.reply_to(message, "❌ Error processing help command.")
