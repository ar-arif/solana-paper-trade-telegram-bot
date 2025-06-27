"""Portfolio and balance command handlers"""
import logging
from telebot import types
from decimal import Decimal

from ..config import SOL_PRICE_USD

logger = logging.getLogger(__name__)


class PortfolioHandlers:
    """Handles portfolio-related commands"""
    
    def __init__(self, bot, solana_api, data_manager):
        self.bot = bot
        self.solana = solana_api
        self.data_manager = data_manager
    
    async def handle_balance_command(self, message):
        """Handle /balance command"""
        try:
            user_id = message.from_user.id
            account = self.data_manager.get_or_create_account(user_id)
            
            # Calculate total portfolio value
            total_value = account.sol_balance
            position_values = []
            
            for position in account.positions:
                current_price = await self.solana.get_token_price(position.token_address)
                if current_price:
                    position_value = position.amount * current_price
                    total_value += position_value / Decimal(str(SOL_PRICE_USD))
                    position_values.append(position_value)
            
            balance_text = f"""
💰 **ACCOUNT BALANCE**

💎 **SOL Balance:** {account.sol_balance:.4f} SOL
📊 **Positions:** {len(account.positions)}
💼 **Total Portfolio Value:** ~{total_value:.4f} SOL
📈 **Total Trades:** {account.total_trades}

💡 Use /portfolio for detailed position info
💡 Use /market to discover new tokens
            """
            
            # Add quick action buttons
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("💼 Portfolio", callback_data="portfolio"),
                types.InlineKeyboardButton("📈 Market", callback_data="market")
            )
            
            await self.bot.reply_to(message, balance_text, reply_markup=markup)
            
        except Exception as e:
            logger.error(f"Error in balance command: {e}")
            await self.bot.reply_to(message, "❌ Error fetching balance. Please try again.")
    
    async def handle_portfolio_command(self, message):
        """Handle /portfolio command"""
        try:
            user_id = message.from_user.id
            account = self.data_manager.get_or_create_account(user_id)
            
            if not account.positions:
                portfolio_text = f"""💼 <b>YOUR PORTFOLIO</b>

💰 <b>Balance:</b> {account.sol_balance:.4f} SOL
📊 <b>Positions:</b> None
📈 <b>Total Trades:</b> {account.total_trades}

💡 Use /search to find tokens to trade!
💡 Use /market to see trending tokens!
                """
                
                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(
                    types.InlineKeyboardButton("📈 Market", callback_data="market"),
                    types.InlineKeyboardButton("🔍 Search", callback_data="help_search")
                )
                
                await self.bot.reply_to(message, portfolio_text, parse_mode='HTML', reply_markup=markup)
                return
            
            # Build detailed portfolio with table format
            portfolio_text = f"""💼 <b>YOUR PORTFOLIO</b>

💰 <b>SOL Balance:</b> {account.sol_balance:.4f} SOL
📊 <b>Active Positions:</b> {len(account.positions)}
📈 <b>Total Trades:</b> {account.total_trades}

<b>📊 POSITIONS TABLE:</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            """
            
            total_value = Decimal('0')
            total_pnl = Decimal('0')
            
            for i, position in enumerate(account.positions, 1):
                current_price = await self.solana.get_token_price(position.token_address)
                if current_price:
                    current_value = position.amount * current_price
                    pnl = (current_price - position.entry_price) * position.amount
                    pnl_percent = ((current_price - position.entry_price) / position.entry_price) * 100
                    total_value += current_value / Decimal(str(SOL_PRICE_USD))
                    total_pnl += pnl / Decimal(str(SOL_PRICE_USD))
                    
                    pnl_emoji = "🟢" if pnl >= 0 else "🔴"
                    pnl_sign = "+" if pnl >= 0 else ""
                    
                    portfolio_text += f"""
<b>{i}. {position.symbol}</b>
┌ 💰 Amount: <code>{position.amount:.2f}</code>
├ 📈 Entry: <code>${position.entry_price:.8f}</code>
├ 💸 Current: <code>${current_price:.8f}</code>
├ 📊 PnL: {pnl_emoji} <code>{pnl_sign}${pnl:.2f} ({pnl_percent:+.2f}%)</code>
└ 📋 Contract: <code>{position.token_address}</code>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
                else:
                    portfolio_text += f"""
<b>{i}. {position.symbol}</b>
┌ 💰 Amount: <code>{position.amount:.2f}</code>
├ 📈 Entry: <code>${position.entry_price:.8f}</code>
├ 💸 Current: <code>❌ Price unavailable</code>
└ 📋 Contract: <code>{position.token_address}</code>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            total_pnl_emoji = "🟢" if total_pnl >= 0 else "🔴"
            total_pnl_sign = "+" if total_pnl >= 0 else ""
            
            portfolio_text += f"""
<b>💎 PORTFOLIO SUMMARY</b>
┌ 🏦 Total Value: <code>~{total_value + account.sol_balance:.4f} SOL</code>
└ 📊 Total P&amp;L: {total_pnl_emoji} <code>{total_pnl_sign}{total_pnl:.4f} SOL</code>

<i>💡 Commands:</i>
• <code>/buy &lt;address&gt; &lt;amount_in_sol&gt;</code>
• <code>/sell &lt;address&gt; &lt;percentage%&gt;</code>
            """
            
            # Add action buttons
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("📈 Market", callback_data="market"),
                types.InlineKeyboardButton("🔍 Search", callback_data="help_search")
            )
            
            await self.bot.reply_to(message, portfolio_text, parse_mode='HTML', reply_markup=markup)
            
        except Exception as e:
            logger.error(f"Error in portfolio command: {e}")
            await self.bot.reply_to(message, "❌ Error fetching portfolio. Please try again.")
    
    async def handle_positions_command(self, message):
        """Handle /positions command"""
        try:
            user_id = message.from_user.id
            account = self.data_manager.get_or_create_account(user_id)
            
            if not account.positions:
                await self.bot.reply_to(message, "📈 You have no open positions. Start trading with /search <token>!")
                return
            
            positions_text = "📋 **Your Open Positions:**\n\n"
            
            for i, position in enumerate(account.positions, 1):
                current_price = await self.solana.get_token_price(position.token_address)
                if current_price:
                    position_value = position.amount * current_price
                    pnl = (current_price - position.entry_price) * position.amount
                    pnl_percent = ((current_price - position.entry_price) / position.entry_price) * 100
                    
                    positions_text += f"""
**{i}. {position.symbol}**
Contract: `{position.token_address}`
Amount: {position.amount:.4f}
Entry: ${position.entry_price:.8f}
Current: ${current_price:.8f}
Value: ${position_value:.2f}
PnL: {pnl:+.2f} USD ({pnl_percent:+.2f}%)

"""
                else:
                    positions_text += f"""
**{i}. {position.symbol}**
Contract: `{position.token_address}`
Amount: {position.amount:.4f}
Entry: ${position.entry_price:.8f}
Current: ❌ Price unavailable

"""
            
            positions_text += "💡 Tap any contract address to copy for trading!"
            await self.bot.reply_to(message, positions_text)
            
        except Exception as e:
            logger.error(f"Error in positions command: {e}")
            await self.bot.reply_to(message, "❌ Error fetching positions. Please try again.")
