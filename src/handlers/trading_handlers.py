"""Trading command handlers"""
import logging
from decimal import Decimal
from datetime import datetime
from telebot import types

from ..models import Position
from ..utils import MessageFormatter, Validator
from ..config import SOL_PRICE_USD

logger = logging.getLogger(__name__)


class TradingHandlers:
    """Handles trading-related commands"""
    
    def __init__(self, bot, solana_api, data_manager):
        self.bot = bot
        self.solana = solana_api
        self.data_manager = data_manager
    
    async def handle_buy_command(self, message):
        """Handle /buy command"""
        try:
            args = message.text.split()[1:]
            if len(args) < 2:
                await self.bot.reply_to(
                    message, 
                    "📝 <b>Usage:</b> /buy &lt;contract_address&gt; &lt;amount_in_sol&gt;\n"
                    "📋 <b>Example:</b> /buy DezXAZ... 1.5\n\n"
                    "💡 <i>Amount is in SOL (e.g., 1.5 = spend 1.5 SOL)</i>",
                    parse_mode='HTML'
                )
                return
            
            token_address = args[0]
            amount_str = args[1]
            
            # Validate inputs
            if not Validator.is_valid_contract_address(token_address):
                await self.bot.reply_to(message, "❌ Invalid contract address format!")
                return
            
            if not Validator.is_positive_number(amount_str):
                await self.bot.reply_to(message, "❌ Amount must be a positive number!")
                return
            
            amount = Decimal(amount_str)
            user_id = message.from_user.id
            account = self.data_manager.get_or_create_account(user_id)
            
            # Show loading message
            loading_msg = await self.bot.reply_to(
                message, 
                "🔄 **PROCESSING BUY ORDER**\n\n"
                "📊 Fetching real-time market data...\n"
                "💰 Analyzing token metrics...\n"
                "🎯 Calculating optimal entry..."
            )
            
            # Get comprehensive token information
            token_info = await self.solana.get_token_info(token_address)
            if not token_info:
                await self.bot.edit_message_text(
                    text=f"❌ Could not fetch token data for: `{token_address}`",
                    chat_id=loading_msg.chat.id,
                    message_id=loading_msg.message_id
                )
                return
            
            current_price_usd = Decimal(str(token_info.price_usd))
            total_cost_usd = amount * current_price_usd
            total_cost_sol = total_cost_usd / Decimal(str(SOL_PRICE_USD))
            
            # Check balance
            if total_cost_sol > account.sol_balance:
                await self._handle_insufficient_balance(
                    loading_msg, account, token_info, token_address, amount, total_cost_usd
                )
                return
            
            # Execute trade
            await self._execute_buy_trade(
                loading_msg, account, token_info, token_address, amount, 
                current_price_usd, total_cost_usd, total_cost_sol
            )
            
        except ValueError:
            await self.bot.reply_to(message, "❌ Invalid amount. Please enter a valid number.")
        except Exception as e:
            logger.error(f"Error in buy command: {e}")
            await self.bot.reply_to(message, "❌ Error executing buy order. Please try again.")
    
    async def handle_sell_command(self, message):
        """Handle /sell command"""
        try:
            args = message.text.split()[1:]
            if len(args) < 2:
                await self.bot.reply_to(
                    message,
                    "📝 <b>Usage:</b> /sell &lt;contract_address&gt; &lt;percentage%&gt;\n"
                    "📋 <b>Examples:</b>\n"
                    "• /sell DezXAZ... 50% (sell 50% of position)\n"
                    "• /sell DezXAZ... 100% (sell all)\n\n"
                    "💡 <i>Use percentage (e.g., 25%, 50%, 100%)</i>",
                    parse_mode='HTML'
                )
                return
            
            token_address = args[0]
            amount_str = args[1]
            
            # Validate inputs
            if not Validator.is_valid_contract_address(token_address):
                await self.bot.reply_to(message, "❌ Invalid contract address format!")
                return
            
            if not Validator.is_positive_number(amount_str):
                await self.bot.reply_to(message, "❌ Amount must be a positive number!")
                return
            
            amount = Decimal(amount_str)
            user_id = message.from_user.id
            account = self.data_manager.get_or_create_account(user_id)
            
            # Find position
            position = next((p for p in account.positions if p.token_address == token_address), None)
            if not position:
                await self.bot.reply_to(
                    message, 
                    f"❌ You don't have any position for this token!\nContract: `{token_address}`"
                )
                return
            
            if amount > position.amount:
                await self.bot.reply_to(
                    message,
                    f"❌ Insufficient {position.symbol}! You have {position.amount:.4f} "
                    f"but trying to sell {amount:.4f}"
                )
                return
            
            # Execute sell
            await self._execute_sell_trade(message, account, position, amount, token_address)
            
        except ValueError:
            await self.bot.reply_to(message, "❌ Invalid amount. Please enter a valid number.")
        except Exception as e:
            logger.error(f"Error in sell command: {e}")
            await self.bot.reply_to(message, "❌ Error executing sell order. Please try again.")
    
    async def _handle_insufficient_balance(self, loading_msg, account, token_info, token_address, amount, total_cost_usd):
        """Handle insufficient balance scenario"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        max_affordable = int(account.sol_balance * Decimal(str(SOL_PRICE_USD)) / Decimal(str(token_info.price_usd)))
        
        if max_affordable > 0:
            suggested_amounts = [
                max_affordable // 4,
                max_affordable // 2,
                max_affordable * 3 // 4,
                max_affordable
            ]
            
            for amt in suggested_amounts:
                if amt > 0:
                    markup.add(types.InlineKeyboardButton(
                        f"Buy {amt:,.0f} tokens",
                        callback_data=f"buy_amount_{token_address}_{amt}"
                    ))
        
        markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="cancel_buy"))
        
        insufficient_text = f"""
❌ **INSUFFICIENT BALANCE**

💰 **Your Balance:** {account.sol_balance:.4f} SOL (${account.sol_balance * Decimal(str(SOL_PRICE_USD)):,.2f})
💸 **Required:** ${total_cost_usd:.2f}
📊 **Token:** {token_info.symbol} - ${token_info.price_usd:.8f}

🎯 **Suggested Amounts:**
        """
        
        await self.bot.edit_message_text(
            text=insufficient_text,
            chat_id=loading_msg.chat.id,
            message_id=loading_msg.message_id,
            reply_markup=markup
        )
    
    async def _execute_buy_trade(self, loading_msg, account, token_info, token_address, amount, current_price_usd, total_cost_usd, total_cost_sol):
        """Execute the buy trade"""
        # Update account
        account.sol_balance -= total_cost_sol
        account.total_trades += 1
        
        # Add to existing position or create new one
        existing_position = next((p for p in account.positions if p.token_address == token_address), None)
        if existing_position:
            total_amount = existing_position.amount + amount
            total_value = (existing_position.amount * existing_position.entry_price) + (amount * current_price_usd)
            existing_position.entry_price = total_value / total_amount
            existing_position.amount = total_amount
        else:
            new_position = Position(
                symbol=token_info.symbol,
                token_address=token_address,
                amount=amount,
                entry_price=current_price_usd,
                timestamp=datetime.now()
            )
            account.positions.append(new_position)
        
        self.data_manager.save_data()
        
        # Create success message with buttons
        success_text = MessageFormatter.format_buy_success_message(
            token_info, token_address, amount, current_price_usd, total_cost_usd, account
        )
        markup = self._create_post_buy_buttons(token_info, token_address)
        
        await self.bot.edit_message_text(
            text=success_text,
            chat_id=loading_msg.chat.id,
            message_id=loading_msg.message_id,
            parse_mode='HTML',
            reply_markup=markup
        )
    
    async def _execute_sell_trade(self, message, account, position, amount, token_address):
        """Execute the sell trade"""
        # Show loading message
        loading_msg = await self.bot.reply_to(message, "🔄 Fetching real-time price...")
        
        # Get current price
        current_price = await self.solana.get_token_price(position.token_address)
        if not current_price:
            await self.bot.edit_message_text(
                text="❌ Unable to fetch real-time price. Please try again.",
                chat_id=loading_msg.chat.id,
                message_id=loading_msg.message_id
            )
            return
        
        # Calculate proceeds
        proceeds_usd = amount * current_price
        proceeds_sol = proceeds_usd / Decimal(str(SOL_PRICE_USD))
        pnl = (current_price - position.entry_price) * amount
        
        # Execute sell
        account.sol_balance += proceeds_sol
        account.total_trades += 1
        position.amount -= amount
        
        # Remove position if fully sold
        if position.amount <= 0:
            account.positions.remove(position)
        
        self.data_manager.save_data()
        
        success_text = f"""
✅ **SELL ORDER EXECUTED!**

🏷️ **Token:** {position.symbol}
📍 **Contract:** `{token_address}`
💎 **Amount:** {amount:.4f}
💰 **Price:** ${current_price:.8f} (Real-time)
💵 **Proceeds:** ${proceeds_usd:.2f} ({proceeds_sol:.6f} SOL)
📊 **PnL:** {pnl:+.6f} SOL
💰 **New Balance:** {account.sol_balance:.4f} SOL
⏰ **Executed:** {datetime.now().strftime('%H:%M:%S UTC')}
        """
        
        await self.bot.edit_message_text(
            text=success_text,
            chat_id=loading_msg.chat.id,
            message_id=loading_msg.message_id
        )
    
    def _create_post_buy_buttons(self, token_info, token_address):
        """Create buttons for after a successful buy"""
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton("📊 Token Info", callback_data=f"info_{token_address}"),
            types.InlineKeyboardButton("💰 Portfolio", callback_data="portfolio"),
            types.InlineKeyboardButton("📈 Market", callback_data="market")
        )
        markup.add(
            types.InlineKeyboardButton(f"🔄 Buy More {token_info.symbol}", callback_data=f"buy_more_{token_address}"),
            types.InlineKeyboardButton("💸 Quick Sell 25%", callback_data=f"sell_25_{token_address}")
        )
        markup.add(types.InlineKeyboardButton("🎯 Set Price Alert", callback_data=f"alert_{token_address}"))
        return markup
