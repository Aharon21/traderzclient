# positions.py
import requests
from typing import List, Dict, Optional
from accounts import Accounts
from config import *


class PositionAPIError(Exception):
    """Custom exception for positions API errors."""
    pass


class Positions:
    def __init__(self, account: Accounts):
        """
        Initialize with an Accounts instance (account must be selected).
        """
        if not account.selected_account:
            raise PositionAPIError("No trading account selected.")
        
        self.account = account
        self.token = account.token
        self.trading_api_token = account.selected_account["tradingApiToken"]

    def _headers(self) -> Dict[str, str]:
        return {
            "Auth-trading-api": self.trading_api_token,
            "Cookie": f"co-auth={self.token}",
            "Content-Type": "application/json"
        }

    def get_open_positions(self) -> List[Dict]:
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/open-positions"
        response = requests.get(url, headers=self._headers())
        if response.status_code != 200:
            raise PositionAPIError(f"Failed to fetch open positions: {response.text}")
        return response.json().get("positions", [])

    def get_closed_positions(self, from_date: str, to_date: str) -> List[Dict]:
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/closed-positions"
        payload = {"from": from_date, "to": to_date}
        response = requests.post(url, headers=self._headers(), json=payload)
        if response.status_code != 200:
            raise PositionAPIError(f"Failed to fetch closed positions: {response.text}")
        return response.json().get("operations", [])

    def open_position(self, instrument: str, order_side: str, volume: float, sl_price: float = 0, tp_price: float = 0, is_mobile: bool = False) -> str:
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/position/open"
        payload = {
            "instrument": instrument,
            "orderSide": order_side.upper(),
            "volume": volume,
            "slPrice": sl_price,
            "tpPrice": tp_price,
            "isMobile": is_mobile
        }
        response = requests.post(url, headers=self._headers(), json=payload)
        data = response.json()
        if response.status_code != 200 or data.get("status") != "OK":
            raise PositionAPIError(f"Failed to open position: {data}")
        return data.get("orderId")

    def edit_position(self, instrument: str, order_id: str, order_side: str, volume: float, sl_price: float, tp_price: float, is_mobile: bool = False) -> str:
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/position/edit"
        payload = {
            "instrument": instrument,
            "id": order_id,
            "orderSide": order_side.upper(),
            "volume": volume,
            "slPrice": sl_price,
            "tpPrice": tp_price,
            "isMobile": is_mobile
        }
        response = requests.post(url, headers=self._headers(), json=payload)
        data = response.json()
        if response.status_code != 200 or data.get("status") != "OK":
            raise PositionAPIError(f"Failed to edit position: {data}")
        return data.get("orderId")

    def partial_close(self, position_id: str, instrument: str, order_side: str, volume: float, is_mobile: bool = False) -> str:
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/position/close-partially"
        payload = {
            "positionId": position_id,
            "volume": volume,
            "instrument": instrument,
            "orderSide": order_side.upper(),
            "isMobile": is_mobile
        }
        response = requests.post(url, headers=self._headers(), json=payload)
        data = response.json()
        if response.status_code != 200 or data.get("status") != "OK":
            raise PositionAPIError(f"Failed to partially close position: {data}")
        return data.get("orderId")

    def close_position(self, position_id: str, instrument: str, order_side: str, volume: float) -> bool:
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/position/close"
        payload = {
            "positionId": position_id,
            "instrument": instrument,
            "orderSide": order_side.upper(),
            "volume": str(volume)
        }
        response = requests.post(url, headers=self._headers(), json=payload)
        data = response.json()
        if response.status_code != 200 or data.get("status") != "OK":
            raise PositionAPIError(f"Failed to close position: {data}")
        return True
