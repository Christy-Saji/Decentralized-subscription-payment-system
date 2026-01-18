# Decentralized Subscription Payment System - Backend

Python Flask backend for reading subscription data from Ethereum Sepolia testnet.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and fill in:

- `SEPOLIA_RPC_URL`: Get from [Infura](https://infura.io) or [Alchemy](https://alchemy.com)
- `CONTRACT_ADDRESS`: Your deployed contract address (from Remix)

### 3. Add Contract ABI

After deploying your contract in Remix:

1. Copy the ABI from Remix (Compile tab → ABI button)
2. Save it as `contract_abi.json` in this directory

### 4. Run the Server
```bash
python app.py
```

Server runs at `http://localhost:5000`

## API Endpoints

### Health Check
```bash
GET /health
```

### Check Subscription Status
```bash
GET /status/<wallet_address>
```

Example:
```bash
curl http://localhost:5000/status/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
```

### Get Expiry Time
```bash
GET /expiry/<wallet_address>
```

### Get Remaining Time
```bash
GET /remaining/<wallet_address>
```

### Get Contract Stats
```bash
GET /stats
```

## Important Notes

- This backend is READ-ONLY
- It NEVER stores private keys
- It NEVER sends transactions
- All payments happen via MetaMask

## Extending This Backend

### Add Caching
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=60)
def get_subscription_status(wallet_address):
    # ... existing code
```

### Add Database for Analytics
```python
# Add SQLAlchemy
# Track subscription history
# Build analytics dashboard
```

### Add Real-time Notifications
```python
# Use event listeners
# Send emails when subscription expires
# Send Telegram/Discord alerts
```

### Add Authentication
```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@app.route('/admin/stats')
@auth.login_required
def admin_stats():
    # Protected endpoint
```