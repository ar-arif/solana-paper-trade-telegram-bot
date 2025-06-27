"""Data management utilities"""
import json
import os
import logging
from typing import Dict
from datetime import datetime

from ..models import UserAccount
from ..config import DATA_FILE, STARTING_BALANCE

logger = logging.getLogger(__name__)


class DataManager:
    """Handles user data persistence"""
    
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.accounts: Dict[int, UserAccount] = {}
        self.load_data()
    
    def load_data(self):
        """Load user data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for user_id, account_data in data.items():
                        self.accounts[int(user_id)] = UserAccount.from_dict(account_data)
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    
    def save_data(self):
        """Save user data to file"""
        try:
            data = {
                str(user_id): account.to_dict()
                for user_id, account in self.accounts.items()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def get_or_create_account(self, user_id: int) -> UserAccount:
        """Get existing account or create new one"""
        if user_id not in self.accounts:
            self.accounts[user_id] = UserAccount(
                user_id=user_id,
                sol_balance=STARTING_BALANCE,
                positions=[],
                total_trades=0,
                created_at=datetime.now()
            )
            self.save_data()
        return self.accounts[user_id]
