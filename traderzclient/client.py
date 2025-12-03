# client.py

from accounts import Accounts
from market import Market
from positions import Positions
from orders import Orders

class TraderzClient:
    """
    High-level client that aggregates Accounts, Market, Positions, and Orders.

    Example usage:
        client = TraderzClient(email="you@example.com", password="mypassword")
        client.select_account("123456")
        symbols = client.market.get_symbols()
        positions = client.positions.get_open_positions()
        orders = client.orders.get_active_orders()
    """

    def __init__(self, email: str, password: str):
        # Login and fetch accounts
        self.accounts = Accounts(email=email, password=password)

        # Market / Positions / Orders initialized after account selection
        self.market = None
        self.positions = None
        self.orders = None

    def init_trading_modules(self):
        """
        Initialize Market, Positions, and Orders modules after selecting an account.
        """
        if not self.accounts.selected_account:
            raise RuntimeError("You must select an account first using select_account().")

        self.market = Market(self.accounts)
        self.positions = Positions(self.accounts)
        self.orders = Orders(self.accounts)

    def select_account(self, trading_account_id: str):
        """
        Select a trading account and initialize all trading modules.
        """
        self.accounts.select_account(trading_account_id)
        self.init_trading_modules()
