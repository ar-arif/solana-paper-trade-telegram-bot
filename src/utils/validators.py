"""Validation utilities"""
import re


class Validator:
    """Validation utilities for bot inputs"""
    
    @staticmethod
    def is_valid_contract_address(address: str) -> bool:
        """Validate Solana contract address format"""
        if not address or len(address) != 44:
            return False
        
        # Base58 character set for Solana addresses
        base58_chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        return all(c in base58_chars for c in address)
    
    @staticmethod
    def is_positive_number(value: str) -> bool:
        """Check if string represents a positive number"""
        try:
            num = float(value)
            return num > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def sanitize_query(query: str) -> str:
        """Sanitize search query"""
        if not query:
            return ""
        
        # Remove potentially dangerous characters and limit length
        sanitized = re.sub(r'[<>"\']', '', query.strip())
        return sanitized[:50]  # Limit to 50 characters
