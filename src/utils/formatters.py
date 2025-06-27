"""Message formatting utilities"""
from datetime import datetime
from typing import Dict, Any
from decimal import Decimal

from ..models import TokenInfo, UserAccount


class MessageFormatter:
    """Handles message formatting for the bot"""
    
    @staticmethod
    def format_buy_success_message(
        token_info: TokenInfo, 
        token_address: str, 
        amount: Decimal, 
        current_price_usd: Decimal, 
        total_cost_usd: Decimal, 
        account: UserAccount
    ) -> str:
        """Format the buy success message"""
        cap_info = token_info.get_market_cap_category()
        change_info = token_info.get_price_change_info()
        
        return f"""✅ <b>BUY ORDER EXECUTED</b>

🎉 <b>TRADE SUMMARY</b>
━━━━━━━━━━━━━━━━━━━━━
🏷️ <b>Token:</b> {token_info.symbol} - {token_info.name}
📍 <b>Contract:</b> <code>{token_address}</code>
💎 <b>Amount:</b> {amount:,.0f} tokens
💰 <b>Entry Price:</b> ${current_price_usd:.8f}
💸 <b>Total Cost:</b> ${total_cost_usd:.2f}

📊 <b>LIVE MARKET DATA</b>
━━━━━━━━━━━━━━━━━━━━━
{cap_info['emoji']} {cap_info['name']}
🏪 <b>Market Cap:</b> ${token_info.market_cap:,.0f}
{change_info['emoji']} <b>24h Change:</b> {change_info['color']} {change_info['text']}
📈 <b>24h Volume:</b> ${token_info.volume_24h:,.0f}
💧 <b>Liquidity:</b> ${token_info.liquidity_usd:,.0f}
🏦 <b>DEX:</b> {token_info.dex.title()}

🎯 <b>TRADING SIGNALS</b>
━━━━━━━━━━━━━━━━━━━━━
{token_info.get_liquidity_status()}
{token_info.get_volume_status()}
Volume/MC Ratio: {token_info.get_volume_mc_ratio():.2f}%

💼 <b>YOUR PORTFOLIO</b>
━━━━━━━━━━━━━━━━━━━━━
💰 <b>Remaining Balance:</b> {account.sol_balance:.4f} SOL
📊 <b>Total Trades:</b> {account.total_trades}
⏰ <b>Executed:</b> {datetime.now().strftime('%H:%M:%S UTC')}

🤖 <b>Data Source:</b> DexScreener (Real-time)
        """
    
    @staticmethod
    def format_token_info_message(token_info: TokenInfo, token_address: str) -> str:
        """Format comprehensive token info message"""
        cap_info = token_info.get_market_cap_category()
        change_info = token_info.get_price_change_info()
        
        return f"""📊 <b>COMPREHENSIVE TOKEN ANALYSIS</b>

🏷️ <b>{token_info.symbol}</b> - {token_info.name}
📍 Contract: <code>{token_info.address}</code>
🏪 Trading on: {token_info.dex.title()}

💰 <b>PRICE METRICS:</b>
Current Price: ${token_info.price_usd:.8f}
24h Change: {change_info['emoji']} {change_info['text']}

📈 <b>MARKET METRICS:</b>
{cap_info['emoji']} {cap_info['name']}
Market Cap: ${token_info.market_cap:,.0f}
Fully Diluted Value: ${token_info.fdv:,.0f}

📊 <b>TRADING METRICS:</b>
24h Volume: ${token_info.volume_24h:,.0f}
Liquidity (USD): ${token_info.liquidity_usd:,.0f}
Volume/Market Cap: {token_info.get_volume_mc_ratio():.2f}%

🎯 <b>TRADING SIGNALS:</b>
{token_info.get_liquidity_status()}
{token_info.get_volume_status()}

⏰ Last Updated: {datetime.now().strftime('%H:%M:%S UTC')}
🤖 Data Source: DexScreener (Real-time)
        """
    
    @staticmethod
    def format_price_message(token_info: TokenInfo, token_address: str) -> str:
        """Format price message"""
        change_info = token_info.get_price_change_info()
        
        return f"""💰 <b>REAL-TIME PRICE</b>

🏷️ {token_info.symbol} - {token_info.name}
📍 Contract: <code>{token_address}</code>

💵 <b>Current Price:</b> ${token_info.price_usd:.8f}
{change_info['emoji']} <b>24h Change:</b> {change_info['text']}
📊 <b>Market Cap:</b> ${token_info.market_cap:,.0f}
📈 <b>24h Volume:</b> ${token_info.volume_24h:,.0f}

⏰ Updated: {datetime.now().strftime('%H:%M:%S UTC')}
🤖 Source: DexScreener (Live)

💡 Tap buttons below for quick actions!
        """
    
    @staticmethod
    def format_search_results(tokens: list, query: str) -> str:
        """Format search results message"""
        if not tokens:
            return f"❌ No tokens found for '{query}'"
        
        search_text = f"🔍 **SEARCH RESULTS FOR '{query}':**\n\n"
        
        for i, token in enumerate(tokens[:5], 1):
            market_cap_formatted = f"${token.market_cap:,.0f}" if token.market_cap > 0 else "N/A"
            volume_formatted = f"${token.volume_24h:,.0f}" if token.volume_24h > 0 else "N/A"
            price_change = f"{token.price_change_24h:+.2f}%" if token.price_change_24h != 0 else "0%"
            
            # Market cap category emoji
            cap_info = token.get_market_cap_category()
            
            search_text += f"""
{cap_info['emoji']} **{i}. {token.symbol}** - {token.name}
💰 **Price:** ${token.price_usd:.8f} ({price_change})
📊 **Market Cap:** {market_cap_formatted}
📈 **24h Volume:** {volume_formatted}
💧 **Liquidity:** ${token.liquidity_usd:,.0f}
🏪 **DEX:** {token.dex.title()}
📍 `{token.address}`

"""
        
        search_text += "\n🚀 **Tap a token below for quick actions!**"
        search_text += "\n📊 **Results sorted by Market Cap (highest first)**"
        
        return search_text
