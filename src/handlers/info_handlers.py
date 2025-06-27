"""Information command handlers"""
import logging
from telebot import types
from datetime import datetime

from ..utils import MessageFormatter, Validator
from ..config import POPULAR_TOKENS

logger = logging.getLogger(__name__)


class InfoHandlers:
    """Handles information-related commands"""
    
    def __init__(self, bot, solana_api, data_manager):
        self.bot = bot
        self.solana = solana_api
        self.data_manager = data_manager
    
    async def handle_search_command(self, message):
        """Handle /search command"""
        try:
            args = message.text.split()[1:]
            if not args:
                await self.bot.reply_to(
                    message, 
                    "Usage: /search <symbol or name>\n"
                    "Example: /search BONK"
                )
                return
            
            query = Validator.sanitize_query(' '.join(args))
            if not query:
                await self.bot.reply_to(message, "❌ Invalid search query!")
                return
            
            # Show loading message
            loading_msg = await self.bot.reply_to(message, f"🔍 Searching for '{query}'...")
            
            # Check if it's a direct contract address lookup
            if Validator.is_valid_contract_address(query):
                token_info = await self.solana.get_token_info(query)
                if token_info:
                    info_text = MessageFormatter.format_token_info_message(token_info, query)
                    markup = self._create_token_info_buttons(query)
                    
                    await self.bot.edit_message_text(
                        text=info_text,
                        chat_id=loading_msg.chat.id,
                        message_id=loading_msg.message_id,
                        parse_mode='HTML',
                        reply_markup=markup
                    )
                else:
                    await self.bot.edit_message_text(
                        text=f"❌ Could not find token data for: `{query}`",
                        chat_id=loading_msg.chat.id,
                        message_id=loading_msg.message_id
                    )
            else:
                # Search by symbol
                tokens = await self.solana.search_token(query.upper())
                
                if not tokens:
                    await self.bot.edit_message_text(
                        text=f"❌ No tokens found for '{query}'",
                        chat_id=loading_msg.chat.id,
                        message_id=loading_msg.message_id
                    )
                    return
                
                search_text = MessageFormatter.format_search_results(tokens, query)
                markup = self._create_search_result_buttons(tokens[:4])
                
                await self.bot.edit_message_text(
                    text=search_text,
                    chat_id=loading_msg.chat.id,
                    message_id=loading_msg.message_id,
                    reply_markup=markup
                )
            
        except Exception as e:
            logger.error(f"Error in search command: {e}")
            await self.bot.reply_to(message, "❌ Error searching for token. Please try again.")
    
    async def handle_price_command(self, message):
        """Handle /price command"""
        try:
            args = message.text.split()[1:]
            if not args:
                await self.bot.reply_to(
                    message, 
                    "Please provide a contract address.\n"
                    "Example: /price DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
                )
                return
            
            token_address = args[0]
            
            if not Validator.is_valid_contract_address(token_address):
                await self.bot.reply_to(message, "❌ Invalid contract address format!")
                return
            
            # Show loading message
            loading_msg = await self.bot.reply_to(message, "🔄 Fetching real-time price...")
            
            # Get real-time price and basic info
            token_info = await self.solana.get_token_info(token_address)
            
            if token_info:
                price_text = MessageFormatter.format_price_message(token_info, token_address)
                markup = self._create_price_action_buttons(token_address)
                
                await self.bot.edit_message_text(
                    text=price_text,
                    chat_id=loading_msg.chat.id,
                    message_id=loading_msg.message_id,
                    reply_markup=markup
                )
            else:
                await self.bot.edit_message_text(
                    text=f"❌ Could not fetch real-time price for: `{token_address}`\nPlease verify the contract address.",
                    chat_id=loading_msg.chat.id,
                    message_id=loading_msg.message_id
                )
                
        except Exception as e:
            logger.error(f"Error in price command: {e}")
            await self.bot.reply_to(message, "❌ Error fetching price. Please try again.")
    
    async def handle_info_command(self, message):
        """Handle /info command"""
        try:
            args = message.text.split()[1:]
            if not args:
                await self.bot.reply_to(
                    message, 
                    "Please provide a contract address.\n"
                    "Example: /info DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
                )
                return
            
            token_address = args[0]
            
            if not Validator.is_valid_contract_address(token_address):
                await self.bot.reply_to(message, "❌ Invalid contract address format!")
                return
            
            # Show loading message
            loading_msg = await self.bot.reply_to(message, "📊 Analyzing token... Fetching comprehensive data...")
            
            # Get comprehensive token information
            token_info = await self.solana.get_token_info(token_address)
            
            if token_info:
                info_text = MessageFormatter.format_token_info_message(token_info, token_address)
                markup = self._create_token_info_buttons(token_address)
                
                await self.bot.edit_message_text(
                    text=info_text,
                    chat_id=loading_msg.chat.id,
                    message_id=loading_msg.message_id,
                    reply_markup=markup
                )
            else:
                await self.bot.edit_message_text(
                    text=f"❌ Could not fetch comprehensive data for: `{token_address}`\nPlease verify the contract address.",
                    chat_id=loading_msg.chat.id,
                    message_id=loading_msg.message_id
                )
                
        except Exception as e:
            logger.error(f"Error in info command: {e}")
            await self.bot.reply_to(message, "❌ Error fetching token information. Please try again.")
    
    async def handle_market_command(self, message):
        """Handle /market command"""
        try:
            # Show loading message
            loading_msg = await self.bot.reply_to(message, "📊 Fetching comprehensive market data...")
            
            market_text = "📈 **SOLANA MEME COIN MARKET**\n\n"
            market_text += f"⏰ Updated: {datetime.now().strftime('%H:%M:%S UTC')}\n"
            market_text += "🤖 Source: DexScreener (Real-time)\n\n"
            
            total_market_cap = 0
            
            for symbol, address in POPULAR_TOKENS:
                try:
                    token_info = await self.solana.get_token_info(address)
                    if token_info:
                        change_info = token_info.get_price_change_info()
                        
                        market_text += f"**{symbol}** {change_info['color']}\n"
                        market_text += f"💰 ${token_info.price_usd:.8f} ({change_info['text']})\n"
                        market_text += f"📊 MC: ${token_info.market_cap:,.0f}\n"
                        market_text += f"📈 Vol: ${token_info.volume_24h:,.0f}\n\n"
                        
                        total_market_cap += token_info.market_cap
                    else:
                        market_text += f"**{symbol}**: ❌ Data unavailable\n\n"
                except Exception as e:
                    market_text += f"**{symbol}**: ❌ Error fetching data\n\n"
                    logger.error(f"Error fetching {symbol}: {e}")
            
            market_text += f"🎯 **TOTAL TRACKED MARKET CAP:** ${total_market_cap:,.0f}\n\n"
            market_text += "💡 Tap a token below for quick actions!"
            
            # Create buttons for quick token access
            markup = types.InlineKeyboardMarkup(row_width=2)
            for symbol, address in POPULAR_TOKENS[:4]:  # First 4 tokens
                markup.add(types.InlineKeyboardButton(
                    f"📊 {symbol}",
                    callback_data=f"token_{address}"
                ))
            
            await self.bot.edit_message_text(
                text=market_text,
                chat_id=loading_msg.chat.id,
                message_id=loading_msg.message_id,
                reply_markup=markup
            )
            
        except Exception as e:
            logger.error(f"Error in market command: {e}")
            await self.bot.reply_to(message, "❌ Error fetching market data. Please try again.")
    
    def _create_search_result_buttons(self, tokens):
        """Create quick action buttons for search results"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        for i, token in enumerate(tokens, 1):
            markup.add(types.InlineKeyboardButton(
                f"{i}. {token.symbol} 💰",
                callback_data=f"token_{token.address}"
            ))
        
        markup.add(
            types.InlineKeyboardButton("📈 Market Overview", callback_data="market"),
            types.InlineKeyboardButton("💼 My Portfolio", callback_data="portfolio")
        )
        return markup
    
    def _create_price_action_buttons(self, token_address):
        """Create action buttons for price command"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💰 Buy", callback_data=f"buy_prompt_{token_address}"),
            types.InlineKeyboardButton("📊 Full Info", callback_data=f"info_{token_address}")
        )
        markup.add(
            types.InlineKeyboardButton("📈 Market", callback_data="market"),
            types.InlineKeyboardButton("💼 Portfolio", callback_data="portfolio")
        )
        return markup
    
    def _create_token_info_buttons(self, token_address):
        """Create buttons for token info display"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💰 Buy", callback_data=f"buy_prompt_{token_address}"),
            types.InlineKeyboardButton("💼 Portfolio", callback_data="portfolio")
        )
        markup.add(
            types.InlineKeyboardButton("📈 Market", callback_data="market"),
            types.InlineKeyboardButton("🎯 Set Alert", callback_data=f"alert_{token_address}")
        )
        return markup
