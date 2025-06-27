"""Solana API integration for token data fetching"""
import aiohttp
import asyncio
import logging
from typing import Optional, List, Dict, Any
from decimal import Decimal

from ..config import DEXSCREENER_BASE_URL, REQUEST_TIMEOUT
from ..models import TokenInfo

logger = logging.getLogger(__name__)


class SolanaAPI:
    """Handles all Solana blockchain and DexScreener API interactions"""
    
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
        
    async def get_token_price(self, token_address: str) -> Optional[Decimal]:
        """Get current token price in USD"""
        try:
            token_info = await self.get_token_info(token_address)
            if token_info:
                return Decimal(str(token_info.price_usd))
            return None
        except Exception as e:
            logger.error(f"Error fetching token price for {token_address}: {e}")
            return None
    
    async def get_token_info(self, token_address: str) -> Optional[TokenInfo]:
        """Get comprehensive token information from DexScreener"""
        try:
            url = f"{DEXSCREENER_BASE_URL}/tokens/{token_address}"
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        pairs = data.get('pairs', [])
                        if not pairs:
                            return None
                        
                        # Filter for Solana pairs and find the best one (highest liquidity)
                        solana_pairs = [pair for pair in pairs if pair.get('chainId') == 'solana']
                        if not solana_pairs:
                            return None
                        
                        # Sort by liquidity and take the best pair
                        best_pair = max(solana_pairs, key=lambda x: float(x.get('liquidity', {}).get('usd', 0) or 0))
                        base_token = best_pair.get('baseToken', {})
                        
                        return TokenInfo(
                            symbol=base_token.get('symbol', 'Unknown'),
                            name=base_token.get('name', 'Unknown'),
                            address=base_token.get('address', token_address),
                            price_usd=float(best_pair.get('priceUsd', 0) or 0),
                            price_change_24h=float(best_pair.get('priceChange', {}).get('h24', 0) or 0),
                            volume_24h=float(best_pair.get('volume', {}).get('h24', 0) or 0),
                            liquidity_usd=float(best_pair.get('liquidity', {}).get('usd', 0) or 0),
                            market_cap=float(best_pair.get('marketCap', 0) or 0),
                            dex=best_pair.get('dexId', 'Unknown'),
                            pair_address=best_pair.get('pairAddress', ''),
                            pair_created_at=best_pair.get('pairCreatedAt', 0),
                            fdv=float(best_pair.get('fdv', 0) or 0),
                        )
                    else:
                        logger.warning(f"DexScreener API error: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error fetching token info from DexScreener: {e}")
            return None
    
    async def search_token(self, query: str) -> List[TokenInfo]:
        """Search for tokens using DexScreener API with comprehensive data"""
        try:
            # If it looks like a contract address, get info directly
            if len(query) == 44 and all(c in '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz' for c in query):
                token_info = await self.get_token_info(query)
                return [token_info] if token_info else []
            else:
                # Search by symbol/name
                url = f"{DEXSCREENER_BASE_URL}/search/?q={query}"
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        pairs = data.get('pairs', [])
                        tokens = []
                        
                        # Filter for Solana tokens and extract comprehensive info
                        for pair in pairs[:10]:  # Limit to first 10 results
                            if pair.get('chainId') == 'solana':
                                base_token = pair.get('baseToken', {})
                                
                                token_info = TokenInfo(
                                    symbol=base_token.get('symbol', 'Unknown'),
                                    name=base_token.get('name', 'Unknown'),
                                    address=base_token.get('address', ''),
                                    price_usd=float(pair.get('priceUsd', 0) or 0),
                                    price_change_24h=float(pair.get('priceChange', {}).get('h24', 0) or 0),
                                    volume_24h=float(pair.get('volume', {}).get('h24', 0) or 0),
                                    liquidity_usd=float(pair.get('liquidity', {}).get('usd', 0) or 0),
                                    market_cap=float(pair.get('marketCap', 0) or 0),
                                    fdv=float(pair.get('fdv', 0) or 0),
                                    dex=pair.get('dexId', 'Unknown'),
                                )
                                tokens.append(token_info)
                        
                        # Sort by market cap descending
                        tokens.sort(key=lambda x: x.market_cap, reverse=True)
                        return tokens
                    else:
                        logger.warning(f"DexScreener search API error: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error searching tokens: {e}")
            return []
    
    async def get_sol_price(self) -> Optional[float]:
        """Get current SOL price in USD (optional enhancement)"""
        try:
            # You can implement this to fetch real SOL price
            # For now, return the default value
            return 100.0
        except Exception as e:
            logger.error(f"Error fetching SOL price: {e}")
            return 100.0  # Default fallback
