"""
Flask REST API for Decentralized Subscription System.

This backend provides read-only access to subscription data on Ethereum.
All write operations (subscribe, cancel) happen via MetaMask.

ENDPOINTS:
- GET /status/<wallet_address>    - Check subscription status
- GET /expiry/<wallet_address>    - Get expiry timestamp
- GET /remaining/<wallet_address> - Get remaining time
- GET /stats                      - Get contract statistics
- GET /health                     - Health check

SAFE TO EXTEND:
- Add authentication/authorization
- Add rate limiting
- Add caching layer (Redis)
- Add analytics endpoints
- Add notification system
- Add admin dashboard
"""

from flask import Flask, jsonify, request
from config import Config
from blockchain import blockchain_service
from datetime import datetime
import traceback


# Initialize Flask app
app = Flask(__name__)

# Validate configuration on startup
try:
    Config.validate()
    print("✓ Flask app initialized successfully")
except ValueError as e:
    print(f"ERROR: Configuration error - {e}")
    exit(1)

# Check blockchain service is available
if blockchain_service is None:
    print("ERROR: Blockchain service not available")
    exit(1)


# ============ HELPER FUNCTIONS ============

def validate_address(address: str) -> tuple:
    """
    Validate Ethereum address format.
    
    Args:
        address (str): Address to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not address:
        return False, "Address is required"
    
    if not address.startswith('0x'):
        return False, "Address must start with 0x"
    
    if len(address) != 42:
        return False, "Address must be 42 characters long"
    
    return True, None


def format_timestamp(timestamp: int) -> str:
    """
    Convert Unix timestamp to human-readable format.
    
    Args:
        timestamp (int): Unix timestamp
    
    Returns:
        str: Formatted datetime string
    """
    if timestamp == 0:
        return "Never subscribed"
    
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')


def format_duration(seconds: int) -> str:
    """
    Convert seconds to human-readable duration.
    
    Args:
        seconds (int): Duration in seconds
    
    Returns:
        str: Formatted duration string
    """
    if seconds == 0:
        return "Expired"
    
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    
    return ", ".join(parts) if parts else "Less than a minute"


# ============ API ENDPOINTS ============

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns basic system status.
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Decentralized Subscription API',
        'blockchain': 'Sepolia Testnet',
        'contract_address': blockchain_service.contract_address
    }), 200


@app.route('/status/<wallet_address>', methods=['GET'])
def get_subscription_status(wallet_address: str):
    """
    Check if a wallet has an active subscription.
    
    Args:
        wallet_address (str): Ethereum wallet address
    
    Returns:
        JSON: Subscription status and details
    
    Example:
        GET /status/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
        
        Response:
        {
            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "is_active": true,
            "expiry_timestamp": 1737216000,
            "expiry_date": "2026-01-18 12:00:00 UTC",
            "remaining_seconds": 86400,
            "remaining_time": "1 day"
        }
    """
    try:
        # Validate address
        is_valid, error_msg = validate_address(wallet_address)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Get status from blockchain
        is_active = blockchain_service.is_subscription_active(wallet_address)
        expiry_timestamp = blockchain_service.get_subscription_expiry(wallet_address)
        remaining_seconds = blockchain_service.get_remaining_time(wallet_address)
        
        return jsonify({
            'wallet_address': wallet_address,
            'is_active': is_active,
            'expiry_timestamp': expiry_timestamp,
            'expiry_date': format_timestamp(expiry_timestamp),
            'remaining_seconds': remaining_seconds,
            'remaining_time': format_duration(remaining_seconds)
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        print(f"ERROR in get_subscription_status: {traceback.format_exc()}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/expiry/<wallet_address>', methods=['GET'])
def get_subscription_expiry(wallet_address: str):
    """
    Get subscription expiry timestamp for a wallet.
    
    Args:
        wallet_address (str): Ethereum wallet address
    
    Returns:
        JSON: Expiry timestamp and formatted date
    
    Example:
        GET /expiry/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
        
        Response:
        {
            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "expiry_timestamp": 1737216000,
            "expiry_date": "2026-01-18 12:00:00 UTC"
        }
    """
    try:
        # Validate address
        is_valid, error_msg = validate_address(wallet_address)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Get expiry from blockchain
        expiry_timestamp = blockchain_service.get_subscription_expiry(wallet_address)
        
        return jsonify({
            'wallet_address': wallet_address,
            'expiry_timestamp': expiry_timestamp,
            'expiry_date': format_timestamp(expiry_timestamp)
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        print(f"ERROR in get_subscription_expiry: {traceback.format_exc()}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/remaining/<wallet_address>', methods=['GET'])
def get_remaining_time(wallet_address: str):
    """
    Get remaining subscription time for a wallet.
    
    Args:
        wallet_address (str): Ethereum wallet address
    
    Returns:
        JSON: Remaining time in seconds and human-readable format
    
    Example:
        GET /remaining/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
        
        Response:
        {
            "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "remaining_seconds": 86400,
            "remaining_time": "1 day"
        }
    """
    try:
        # Validate address
        is_valid, error_msg = validate_address(wallet_address)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Get remaining time from blockchain
        remaining_seconds = blockchain_service.get_remaining_time(wallet_address)
        
        return jsonify({
            'wallet_address': wallet_address,
            'remaining_seconds': remaining_seconds,
            'remaining_time': format_duration(remaining_seconds)
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        print(f"ERROR in get_remaining_time: {traceback.format_exc()}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/stats', methods=['GET'])
def get_contract_stats():
    """
    Get overall contract statistics.
    
    Returns:
        JSON: Contract statistics including price, subscribers, revenue
    
    Example:
        GET /stats
        
        Response:
        {
            "subscription_price_eth": "0.001",
            "subscription_duration_days": 30,
            "total_subscribers": 42,
            "total_revenue_eth": "0.042",
            "contract_balance_eth": "0.042",
            "contract_address": "0x..."
        }
    
    SAFE TO EXTEND:
    - Add growth metrics (new subscribers per day)
    - Add churn rate
    - Add revenue trends
    - Add subscriber demographics
    """
    try:
        stats = blockchain_service.get_contract_stats()
        return jsonify(stats), 200
    
    except Exception as e:
        print(f"ERROR in get_contract_stats: {traceback.format_exc()}")
        return jsonify({'error': 'Internal server error'}), 500


# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'GET /health',
            'GET /status/<wallet_address>',
            'GET /expiry/<wallet_address>',
            'GET /remaining/<wallet_address>',
            'GET /stats'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


# ============ RUN APP ============

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Decentralized Subscription API")
    print("="*60)
    print(f"Contract: {blockchain_service.contract_address}")
    print(f"Network: Sepolia Testnet")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.FLASK_DEBUG
    )