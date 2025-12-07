# TraderZ Client

Python client library for the TraderZ API, allowing easy access to accounts, market data, positions, and orders.

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Aharon21/traderzclient.git
cd traderzclient
pip install -r requirements.txt
```

# Usage
Using the high-level TraderZClient

```
from traderzclient import TraderZClient

EMAIL = "your.email@example.com"
PASSWORD = "yourpassword"

# Initialize client and login
client = TraderZClient(email=EMAIL, password=PASSWORD)

# List all trading accounts
for acc in client.accounts.list_accounts():
    print(acc["tradingAccountId"], acc["name"])

# Select a trading account
selected_id = client.accounts.list_accounts()[0]["tradingAccountId"]
client.select_account(selected_id)

# Market data
symbols = client.market.get_symbols()
print("Symbols:", [s["symbol"] for s in symbols[:5]])

quotes = client.market.market_watch(["EURUSD", "GBPUSD"])
print("Market quotes:", quotes)

candles = client.market.get_candles(
    symbol="EURUSD",
    interval="M15",
    start="2025-10-01T00:00:00Z",
    end="2025-10-02T00:00:00Z"
)
print("Candlestick data:", candles["candles"][:3])

# Positions
open_positions = client.positions.get_open_positions()
print("Open positions:", open_positions)

# Orders
active_orders = client.orders.get_active_orders()
print("Active orders:", active_orders)

# Create, edit, and cancel a pending order
new_order_id = client.orders.create_pending_order(
    instrument="EURUSD",
    order_side="BUY",
    volume=0.01,
    price=1.05,
    type="LIMIT"
)
print("New pending order ID:", new_order_id)

updated_order_id = client.orders.edit_pending_order(
    instrument="EURUSD",
    order_id=new_order_id,
    order_side="BUY",
    volume=0.02,
    price_order=1.06,
    sl_price=1.04,
    tp_price=1.08
)
print("Updated pending order ID:", updated_order_id)

cancelled_order_id = client.orders.cancel_pending_order(
    instrument="EURUSD",
    order_id=new_order_id,
    order_side="BUY"
)
print("Cancelled pending order ID:", cancelled_order_id)
```
# Features

- Accounts: Login, list accounts, select account, get headers

- Market: Retrieve symbols, market watch, account balance, candlestick data

- Positions: Get open/closed positions, open/edit/partial/close positions

- Orders: Get active orders, create/edit/cancel pending orders
