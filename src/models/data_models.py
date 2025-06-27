"""Data models for the trading bot"""
from dataclasses import dataclass, asdict
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any
import json


@dataclass
class Position:
    """Represents a trading position"""
    symbol: str
    token_address: str
    amount: Decimal
    entry_price: Decimal
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'symbol': self.symbol,
            'token_address': self.token_address,
            'amount': str(self.amount),
            'entry_price': str(self.entry_price),
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Position':
        return cls(
            symbol=data['symbol'],
            token_address=data['token_address'],
            amount=Decimal(str(data['amount'])),
            entry_price=Decimal(str(data['entry_price'])),
            timestamp=datetime.fromisoformat(data['timestamp'])
        )


@dataclass 
class UserAccount:
    """Represents a user's trading account"""
    user_id: int
    sol_balance: Decimal
    positions: List[Position]
    total_trades: int
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'sol_balance': str(self.sol_balance),
            'positions': [pos.to_dict() for pos in self.positions],
            'total_trades': self.total_trades,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserAccount':
        return cls(
            user_id=data['user_id'],
            sol_balance=Decimal(str(data['sol_balance'])),
            positions=[Position.from_dict(pos) for pos in data['positions']],
            total_trades=data['total_trades'],
            created_at=datetime.fromisoformat(data['created_at'])
        )


@dataclass
class TokenInfo:
    """Represents comprehensive token information"""
    symbol: str
    name: str
    address: str
    price_usd: float
    price_change_24h: float
    volume_24h: float
    liquidity_usd: float
    market_cap: float
    fdv: float
    dex: str
    pair_address: str = ""
    pair_created_at: int = 0
    
    def get_market_cap_category(self) -> Dict[str, str]:
        """Get market cap category info"""
        from ..config import MARKET_CAP_CATEGORIES
        
        for category, info in MARKET_CAP_CATEGORIES.items():
            if self.market_cap >= info['min']:
                return {'emoji': info['emoji'], 'name': info['name']}
        
        return {'emoji': '🦐', 'name': 'Nano Cap'}
    
    def get_price_change_info(self) -> Dict[str, str]:
        """Get formatted price change info"""
        if self.price_change_24h > 0:
            return {
                'emoji': '📈',
                'color': '🟢', 
                'text': f'+{self.price_change_24h:.2f}%'
            }
        elif self.price_change_24h < 0:
            return {
                'emoji': '📉',
                'color': '🔴',
                'text': f'{self.price_change_24h:.2f}%'
            }
        else:
            return {
                'emoji': '➡️',
                'color': '⚪',
                'text': '0%'
            }
    
    def get_liquidity_status(self) -> str:
        """Get liquidity status"""
        from ..config import LIQUIDITY_THRESHOLDS
        
        if self.liquidity_usd > LIQUIDITY_THRESHOLDS['high']:
            return "🟢 High Liquidity"
        elif self.liquidity_usd > LIQUIDITY_THRESHOLDS['medium']:
            return "🟡 Medium Liquidity"
        else:
            return "🔴 Low Liquidity"
    
    def get_volume_status(self) -> str:
        """Get volume status"""
        from ..config import VOLUME_THRESHOLDS
        
        if self.volume_24h > VOLUME_THRESHOLDS['high']:
            return "🟢 Active Trading"
        elif self.volume_24h > VOLUME_THRESHOLDS['medium']:
            return "🟡 Moderate Trading"
        else:
            return "🔴 Low Trading"
    
    def get_volume_mc_ratio(self) -> float:
        """Get volume to market cap ratio"""
        return (self.volume_24h / max(self.market_cap, 1)) * 100
