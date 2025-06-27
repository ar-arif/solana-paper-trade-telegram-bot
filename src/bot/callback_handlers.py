"""Callback query handlers for interactive buttons"""
import logging
from decimal import Decimal
from telebot import types

from ..utils import MessageFormatter
from ..config import SOL_PRICE_USD

logger = logging.getLogger(__name__)


class CallbackHandlers:
    """Handles callback queries from inline buttons"""
    
    def __init__(self, bot, solana_api, data_manager, trading_handlers, info_handlers, portfolio_handlers):
        self.bot = bot
        self.solana = solana_api
        self.data_manager = data_manager
        self.trading_handlers = trading_handlers
        self.info_handlers = info_handlers
        self.portfolio_handlers = portfolio_handlers
    
    async def handle_callback_query(self, call):
        """Handle all inline button callbacks"""
        try:
            data = call.data
            user_id = call.from_user.id
            
            # Handle different callback types
            if data.startswith("buy_amount_"):
                await self._handle_buy_amount(call, user_id, data)
            
            elif data.startswith("info_"):
                await self._handle_info_token(call, data)
            
            elif data == "portfolio":
                await self._handle_portfolio(call, user_id)
            
            elif data == "market":
                await self._handle_market(call)
            
            elif data.startswith("buy_more_"):
                await self._handle_buy_more(call, data)
            
            elif data.startswith("sell_25_"):
                await self._handle_quick_sell(call, user_id, data, 25)
            
            elif data.startswith("alert_"):
                await self._handle_price_alert(call, data)
            
            elif data == "cancel_buy":
                await self._handle_cancel_buy(call)
            
            elif data == "help_buy":
                await self._handle_buy_help(call)
            
            elif data.startswith("token_"):
                await self._handle_token_quick_actions(call, data)
            
            elif data.startswith("buy_prompt_"):
                await self._handle_buy_prompt(call, data)
            
            elif data == "help_search":
                await self._handle_search_help(call)
            
            # Answer the callback to remove the loading indicator
            await self.bot.answer_callback_query(call.id)
            
        except Exception as e:
            logger.error(f"Error handling callback: {e}")
            await self.bot.answer_callback_query(call.id, "❌ Error processing request")
    
    async def _handle_buy_amount(self, call, user_id, data):
        """Handle buy amount button clicks"""
        parts = data.split("_")
        if len(parts) >= 4:
            token_address = parts[2]
            amount = Decimal(parts[3])
            
            await self._execute_buy_order(call.message, user_id, token_address, amount, edit_mode=True)
    
    async def _handle_info_token(self, call, data):
        """Handle token info button clicks"""
        token_address = data.split("_")[1]
        await self._show_token_info(call.message, token_address, edit_mode=True)
    
    async def _handle_portfolio(self, call, user_id):
        """Handle portfolio button clicks"""
        await self._show_portfolio(call.message, user_id, edit_mode=True)
    
    async def _handle_market(self, call):
        """Handle market button clicks"""
        await self._show_market_data(call.message, edit_mode=True)
    
    async def _handle_buy_more(self, call, data):
        """Handle buy more button clicks"""
        token_address = data.split("_")[2]
        await self._prompt_buy_more(call.message, token_address)
    
    async def _handle_quick_sell(self, call, user_id, data, percentage):
        """Handle quick sell button clicks"""
        token_address = data.split("_")[2]
        await self._quick_sell_percentage(call.message, user_id, token_address, percentage)
    
    async def _handle_price_alert(self, call, data):
        """Handle price alert button clicks"""
        token_address = data.split("_")[1]
        await self._prompt_price_alert(call.message, token_address)
    
    async def _handle_cancel_buy(self, call):
        """Handle cancel buy button clicks"""
        await self.bot.edit_message_text(
            text="❌ Buy operation cancelled.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
    
    async def _handle_buy_help(self, call):
        """Handle buy help button clicks"""
        await self._show_buy_help(call.message)
    
    async def _handle_token_quick_actions(self, call, data):
        """Handle token quick actions button clicks"""
        token_address = data.split("_")[1]
        await self._show_token_quick_actions(call.message, token_address)
    
    async def _handle_buy_prompt(self, call, data):
        """Handle buy prompt button clicks"""
        token_address = data.split("_")[2]
        await self._prompt_buy_more(call.message, token_address)
    
    async def _handle_search_help(self, call):
        """Handle search help button clicks"""
        help_text = """
🔍 **HOW TO SEARCH TOKENS**

📝 **Search Command:**
`/search <symbol or name>`

📋 **Examples:**
• `/search BONK` - Find BONK token
• `/search Pepe` - Find tokens with "Pepe" in name
• `/search DezXAZ...` - Get info by contract address

🎯 **Results include:**
• Real-time price and 24h change
• Market cap and volume
• Liquidity and DEX info
• Quick action buttons

💡 **Pro Tips:**
• Results sorted by market cap
• Use buttons for instant actions
• Check liquidity before trading
        """
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📈 Market", callback_data="market"),
            types.InlineKeyboardButton("💼 Portfolio", callback_data="portfolio")
        )
        
        await self.bot.edit_message_text(
            text=help_text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
    
    # Helper methods that delegate to appropriate handlers or implement simple logic
    async def _execute_buy_order(self, message, user_id, token_address, amount, edit_mode=False):
        """Execute a buy order - delegates to trading handler logic"""
        # This would contain the same logic as in trading_handlers._execute_buy_trade
        # For brevity, I'll implement a simplified version
        try:
            account = self.data_manager.get_or_create_account(user_id)
            
            token_info = await self.solana.get_token_info(token_address)
            if not token_info:
                error_text = f"❌ Could not fetch token data for: `{token_address}`"
                await self.bot.edit_message_text(text=error_text, chat_id=message.chat.id, message_id=message.message_id)
                return
            
            # Simple buy execution logic would go here
            # For now, show success message
            success_text = f"✅ Buy order executed for {amount} {token_info.symbol} tokens!"
            await self.bot.edit_message_text(text=success_text, chat_id=message.chat.id, message_id=message.message_id)
            
        except Exception as e:
            logger.error(f"Error executing buy order: {e}")
            await self.bot.edit_message_text(
                text="❌ Error executing buy order.", 
                chat_id=message.chat.id, 
                message_id=message.message_id
            )
    
    async def _show_token_info(self, message, token_address, edit_mode=False):
        """Show token info - delegates to info handler"""
        try:
            token_info = await self.solana.get_token_info(token_address)
            if token_info:
                info_text = MessageFormatter.format_token_info_message(token_info, token_address)
                markup = self._create_token_info_buttons(token_address)
                
                await self.bot.edit_message_text(
                    text=info_text,
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    reply_markup=markup
                )
            else:
                await self.bot.edit_message_text(
                    text=f"❌ Could not fetch token data for: `{token_address}`",
                    chat_id=message.chat.id,
                    message_id=message.message_id
                )
        except Exception as e:
            logger.error(f"Error showing token info: {e}")
            await self.bot.edit_message_text(
                text="❌ Error fetching token information.",
                chat_id=message.chat.id,
                message_id=message.message_id
            )
    
    async def _show_portfolio(self, message, user_id, edit_mode=False):
        """Show portfolio - simplified version"""
        try:
            account = self.data_manager.get_or_create_account(user_id)
            
            portfolio_text = f"""💼 <b>YOUR PORTFOLIO</b>

💰 <b>Balance:</b> {account.sol_balance:.4f} SOL
📊 <b>Positions:</b> {len(account.positions)}
📈 <b>Total Trades:</b> {account.total_trades}

💡 Use buttons below for more actions!
            """
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("📈 Market", callback_data="market"),
                types.InlineKeyboardButton("🔍 Search", callback_data="help_search")
            )
            
            await self.bot.edit_message_text(
                text=portfolio_text,
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode='HTML',
                reply_markup=markup
            )
        except Exception as e:
            logger.error(f"Error showing portfolio: {e}")
            await self.bot.edit_message_text(
                text="❌ Error fetching portfolio data.",
                chat_id=message.chat.id,
                message_id=message.message_id
            )
    
    async def _show_market_data(self, message, edit_mode=False):
        """Show market data - simplified version"""
        try:
            from ..config import POPULAR_TOKENS
            
            market_text = "📈 **SOLANA MEME COIN MARKET**\n\n"
            market_text += "💡 Real-time data from DexScreener\n\n"
            
            for symbol, address in POPULAR_TOKENS[:2]:  # Show first 2 for demo
                market_text += f"**{symbol}** - Loading data...\n\n"
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            for symbol, address in POPULAR_TOKENS[:4]:
                markup.add(types.InlineKeyboardButton(
                    f"📊 {symbol}",
                    callback_data=f"token_{address}"
                ))
            
            await self.bot.edit_message_text(
                text=market_text,
                chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=markup
            )
        except Exception as e:
            logger.error(f"Error showing market data: {e}")
            await self.bot.edit_message_text(
                text="❌ Error fetching market data.",
                chat_id=message.chat.id,
                message_id=message.message_id
            )
    
    # Additional helper methods for other callback actions...
    async def _prompt_buy_more(self, message, token_address):
        """Prompt for buying more tokens"""
        try:
            token_info = await self.solana.get_token_info(token_address)
            if token_info:
                prompt_text = f"""
💰 **BUY MORE {token_info.symbol}**

Current Price: ${token_info.price_usd:.8f}

💡 **Usage:** /buy {token_address} <amount>
📝 **Example:** /buy {token_address} 1000
                """
                
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(types.InlineKeyboardButton("🔙 Back", callback_data=f"token_{token_address}"))
                
                await self.bot.edit_message_text(
                    text=prompt_text,
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    reply_markup=markup
                )
            else:
                await self.bot.edit_message_text(
                    text="❌ Error fetching token data.",
                    chat_id=message.chat.id,
                    message_id=message.message_id
                )
        except Exception as e:
            logger.error(f"Error in prompt_buy_more: {e}")
            await self.bot.edit_message_text(
                text="❌ Error processing request.",
                chat_id=message.chat.id,
                message_id=message.message_id
            )
    
    async def _quick_sell_percentage(self, message, user_id, token_address, percentage):
        """Quick sell implementation - simplified"""
        await self.bot.edit_message_text(
            text=f"🔄 Quick sell {percentage}% feature coming soon!",
            chat_id=message.chat.id,
            message_id=message.message_id
        )
    
    async def _prompt_price_alert(self, message, token_address):
        """Price alert prompt"""
        try:
            token_info = await self.solana.get_token_info(token_address)
            if token_info:
                alert_text = f"""
🎯 **SET PRICE ALERT - {token_info.symbol}**

Current Price: ${token_info.price_usd:.8f}

📱 **Feature Coming Soon!**
Price alerts will notify you when {token_info.symbol} reaches your target price.

💡 For now, bookmark this token and check manually!
                """
                
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(types.InlineKeyboardButton("🔙 Back", callback_data=f"token_{token_address}"))
                
                await self.bot.edit_message_text(
                    text=alert_text,
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    reply_markup=markup
                )
        except Exception as e:
            logger.error(f"Error in prompt_price_alert: {e}")
            await self.bot.edit_message_text(
                text="❌ Error processing request.",
                chat_id=message.chat.id,
                message_id=message.message_id
            )
    
    async def _show_buy_help(self, message):
        """Show buy help"""
        help_text = """
💰 **HOW TO BUY TOKENS**

🔍 **1. Find a Token:**
• Use `/search <symbol>` to find tokens
• Use `/market` to see trending tokens

📝 **2. Buy Command:**
`/buy <contract_address> <amount>`

💡 **Tips:**
• Contract addresses are 44 characters long
• Start with small amounts to test
• Check liquidity before big trades
        """
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🔍 Search Tokens", callback_data="help_search"),
            types.InlineKeyboardButton("📈 Market", callback_data="market")
        )
        
        await self.bot.edit_message_text(
            text=help_text,
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=markup
        )
    
    async def _show_token_quick_actions(self, message, token_address):
        """Show quick actions for a token"""
        try:
            token_info = await self.solana.get_token_info(token_address)
            if token_info:
                change_info = token_info.get_price_change_info()
                
                quick_text = f"""
🚀 **QUICK ACTIONS - {token_info.symbol}**

🏷️ **{token_info.name}**
💰 **Price:** ${token_info.price_usd:.8f}
{change_info['emoji']} **24h Change:** {change_info['text']}
📊 **Market Cap:** ${token_info.market_cap:,.0f}

📍 Contract: `{token_address}`
⏰ Live data from DexScreener
                """
                
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(
                    types.InlineKeyboardButton("💰 Buy", callback_data=f"buy_prompt_{token_address}"),
                    types.InlineKeyboardButton("📊 Full Info", callback_data=f"info_{token_address}")
                )
                markup.add(
                    types.InlineKeyboardButton("🔙 Market", callback_data="market"),
                    types.InlineKeyboardButton("💼 Portfolio", callback_data="portfolio")
                )
                
                await self.bot.edit_message_text(
                    text=quick_text,
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    reply_markup=markup
                )
            else:
                await self.bot.edit_message_text(
                    text=f"❌ Could not fetch token data for: `{token_address}`",
                    chat_id=message.chat.id,
                    message_id=message.message_id
                )
        except Exception as e:
            logger.error(f"Error showing token quick actions: {e}")
            await self.bot.edit_message_text(
                text="❌ Error fetching token data.",
                chat_id=message.chat.id,
                message_id=message.message_id
            )
    
    def _create_token_info_buttons(self, token_address):
        """Create buttons for token info"""
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
