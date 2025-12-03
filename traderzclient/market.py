# market.py

import requests
from typing import List, Dict
from config import *


class MarketAPIError(Exception):
    pass


class Market:
    def __init__(self, accounts):
        self.accounts = accounts   # instance of Accounts

    # ----------------------------------------------
    # INTERNAL HEADERS
    # ----------------------------------------------
    def _headers(self):
        if not self.accounts.token:
            raise MarketAPIError("Client not logged in.")

        trading_api_token = self.accounts.selected_account.get("tradingApiToken")
        if not trading_api_token:
            raise MarketAPIError("No trading API token available. Select an account first.")

        return {
            "Accept": "application/json",
            "Auth-trading-api": trading_api_token,
            "Cookie": f"co-auth={self.accounts.token}",
            "Content-Type": "application/json"
        }

    # ----------------------------------------------
    # GET SYMBOLS
    # ----------------------------------------------
    def get_symbols(self) -> List[Dict]:
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/effective-instruments"

        response = requests.get(url, headers=self._headers())
        if response.status_code != 200:
            raise MarketAPIError(f"Error reading symbols: {response.status_code} - {response.text}")

        return response.json()

    # ----------------------------------------------
    # MARKET WATCH
    # ----------------------------------------------
    def market_watch(self, symbols: List[str]):
        """
        symbols must be a list like ["EURUSD", "XAUUSD"]
        """
        symbols_str = ",".join(symbols)
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/quotations?symbols={symbols_str}"

        response = requests.get(url, headers=self._headers())
        if response.status_code != 200:
            raise MarketAPIError(f"Error fetching quotations: {response.status_code} - {response.text}")

        return response.json()

    # ----------------------------------------------
    # GET CANDLES
    # ----------------------------------------------
    def get_candles(self, symbol: str, interval: str, start: str, end: str):
        """
        Example: get_candles("EURUSD", "M15", "2025-07-15T00:00:00Z", "2025-07-15T01:00:00Z")
        """
        url = (f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/candles?"
               f"symbol={symbol}&interval={interval}&from={start}&to={end}")

        response = requests.get(url, headers=self._headers())
        if response.status_code != 200:
            raise MarketAPIError(f"Error fetching candles: {response.status_code} - {response.text}")

        return response.json()

    # ----------------------------------------------
    # GET BALANCE
    # ----------------------------------------------
    def get_balance(self):
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/balance"

        response = requests.get(url, headers=self._headers())
        if response.status_code != 200:
            raise MarketAPIError(f"Error fetching balance: {response.status_code} - {response.text}")

        return response.json()
