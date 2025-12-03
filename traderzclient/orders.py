# orders.py
import requests
from typing import List, Dict, Optional
from config import *
class OrdersAPIError(Exception):
    """Custom exception for orders API errors."""
    pass

class Orders:
    def __init__(self, account):
        """
        account: instance of Accounts class (must have selected_account)
        """
        if not account.selected_account:
            raise OrdersAPIError("No trading account selected. Call select_account() first.")
        self.account = account
        self.token = account.token
        self.trading_api_token = account.selected_account.get("tradingApiToken")

    def _headers(self):
        return {
            'Auth-trading-api': self.trading_api_token,
            'Cookie': f'co-auth={self.token}',
            'Content-Type': 'application/json'
        }

    def get_active_orders(self) -> List[Dict]:
        """Get all active/pending orders."""
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/active-orders"
        resp = requests.get(url, headers=self._headers())
        if resp.status_code != 200:
            raise OrdersAPIError(f"Failed to get active orders: {resp.status_code} - {resp.text}")
        return resp.json().get("orders", [])

    def create_pending_order(self, instrument: str, order_side: str, volume: float, price: float,
                             type: str = "LIMIT", sl_price: float = 0, tp_price: float = 0, is_mobile: bool = False) -> str:
        """Create a new pending order."""
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/pending-order/create"
        payload = {
            "instrument": instrument,
            "orderSide": order_side,
            "volume": volume,
            "price": price,
            "type": type,
            "slPrice": sl_price,
            "tpPrice": tp_price,
            "isMobile": is_mobile
        }
        resp = requests.post(url, json=payload, headers=self._headers())
        if resp.status_code != 200:
            raise OrdersAPIError(f"Failed to create pending order: {resp.status_code} - {resp.text}")
        data = resp.json()
        if data.get("status") != "OK":
            raise OrdersAPIError(f"Create pending order failed: {data.get('errorMessage')}")
        return data.get("orderId")

    def edit_pending_order(self, instrument: str, order_id: str, order_side: str, volume: float,
                           type: str = "LIMIT", sl_price: float = 0, tp_price: float = 0, price_order: float = 0,
                           is_mobile: bool = False) -> str:
        """Edit an existing pending order."""
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/pending-order/edit"
        payload = {
            "instrument": instrument,
            "id": order_id,
            "orderSide": order_side,
            "type": type,
            "volume": volume,
            "slPrice": sl_price,
            "tpPrice": tp_price,
            "priceOrder": price_order,
            "isMobile": is_mobile
        }
        resp = requests.post(url, json=payload, headers=self._headers())
        if resp.status_code != 200:
            raise OrdersAPIError(f"Failed to edit pending order: {resp.status_code} - {resp.text}")
        data = resp.json()
        if data.get("status") != "OK":
            raise OrdersAPIError(f"Edit pending order failed: {data.get('errorMessage')}")
        return data.get("orderId")

    def cancel_pending_order(self, instrument: str, order_id: str, order_side: str,
                             type: str = "LIMIT", is_mobile: bool = False) -> str:
        """Cancel a pending order."""
        url = f"{BASE_URL}/mtr-api/{SYSTEM_UUID}/pending-order/cancel"
        payload = {
            "instrument": instrument,
            "id": order_id,
            "orderSide": order_side,
            "type": type,
            "isMobile": is_mobile
        }
        resp = requests.post(url, json=payload, headers=self._headers())
        if resp.status_code != 200:
            raise OrdersAPIError(f"Failed to cancel pending order: {resp.status_code} - {resp.text}")
        data = resp.json()
        if data.get("status") != "OK":
            raise OrdersAPIError(f"Cancel pending order failed: {data.get('errorMessage')}")
        return data.get("orderId")
