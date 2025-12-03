# accounts.py
import requests
from config import *
from typing import List, Dict, Optional


class AccountAPIError(Exception):
    """Custom exception for account API errors."""
    pass

class Accounts:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.token: Optional[str] = None
        self.trading_accounts: List[Dict] = []
        self.selected_account: Optional[Dict] = None
        self.login()

    def login(self):
        """Login to the API and store the token and accounts."""
        url = f"{BASE_URL}/manager/mtr-login"
        payload = {
            "email": self.email,
            "password": self.password,
            "brokerId": BROKER_ID
        }
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            raise AccountAPIError(f"Login failed: {response.status_code} - {response.text}")

        data = response.json()
        self.token = data.get("token")
        self.trading_accounts = data.get("accounts", [])
        #self.selected_account = data.get("selectedTradingAccount")

    def list_accounts(self) -> List[Dict]:
        """
        Return all trading accounts in simplified format:
        [{
            "tradingAccountId": str,
            "tradingApiToken": str,
            "offerUuid": str,
            "name": str
        }, ...]
        """
        simplified = []
        for acc in self.trading_accounts:
            simplified.append({
                "tradingAccountId": acc.get("tradingAccountId"),
                "tradingApiToken": acc.get("tradingApiToken"),
                "offerUuid": acc.get("offer", {}).get("uuid"),
                "name": acc.get("offer", {}).get("name")
            })
        return simplified

    def select_account(self, trading_account_id: str):
        """
        Select a trading account by its tradingAccountId.
        """
        for acc in self.trading_accounts:
            if acc.get("tradingAccountId") == trading_account_id:
                self.selected_account = acc
                return 
        raise AccountAPIError(f"Trading account {trading_account_id} not found.")

    def get_selected_account(self) -> Optional[Dict]:
        """Return the currently selected account."""
        return self.selected_account

    def get_auth_headers(self) -> Dict[str, str]:
        """Return headers with authorization token for subsequent API calls."""
        if not self.token:
            raise AccountAPIError("No token available. Login first.")
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
