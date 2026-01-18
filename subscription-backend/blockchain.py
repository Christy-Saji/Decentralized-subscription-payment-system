"""
Blockchain interaction layer using web3.py.

This module handles all interactions with the Ethereum blockchain.
It connects to Sepolia via RPC and reads smart contract state.

IMPORTANT: This module ONLY reads blockchain state.
IMPORTANT: It NEVER sends transactions or uses private keys.
IMPORTANT: All transactions happen via MetaMask in user's browser.
"""

import json
from web3 import Web3
from config import Config


class BlockchainService:
    """
    Service class for interacting with the SubscriptionPayment smart contract.
    
    This class provides read-only access to blockchain data.
    All write operations (subscribe, cancel) happen via MetaMask.
    
    SAFE TO EXTEND:
    - Add caching layer for frequently accessed data
    - Add event listener for real-time subscription tracking
    - Add batch queries for multiple addresses
    - Add historical data queries using event logs
    """
    
    def __init__(self):
        """
        Initialize Web3 connection and load smart contract.
        """
        # Connect to Sepolia via RPC
        self.w3 = Web3(Web3.HTTPProvider(Config.SEPOLIA_RPC_URL))
        
        # Verify connection
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Sepolia RPC")
        
        print(f"✓ Connected to Sepolia (Chain ID: {self.w3.eth.chain_id})")
        
        # Load contract ABI
        self.contract_address = Web3.to_checksum_address(Config.CONTRACT_ADDRESS)
        self.contract_abi = self._load_abi()
        
        # Create contract instance
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
        
        print(f"✓ Contract loaded at {self.contract_address}")
    
    def _load_abi(self):
        """
        Load contract ABI from JSON file.
        
        Returns:
            list: Contract ABI
        """
        try:
            with open('contract_abi.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                "contract_abi.json not found. "
                "Generate it after deploying your contract in Remix."
            )
    
    # ============ READ-ONLY CONTRACT METHODS ============
    
    def is_subscription_active(self, wallet_address: str) -> bool:
        """
        Check if a wallet has an active subscription.
        
        Args:
            wallet_address (str): Ethereum wallet address
        
        Returns:
            bool: True if subscription is active, False otherwise
        
        Raises:
            ValueError: If wallet address is invalid
        """
        try:
            # Convert to checksum address (required by Web3)
            checksum_address = Web3.to_checksum_address(wallet_address)
            
            # Call contract's isActive function
            is_active = self.contract.functions.isActive(checksum_address).call()
            
            return is_active
        
        except ValueError as e:
            raise ValueError(f"Invalid wallet address: {wallet_address}") from e
    
    def get_subscription_expiry(self, wallet_address: str) -> int:
        """
        Get subscription expiry timestamp for a wallet.
        
        Args:
            wallet_address (str): Ethereum wallet address
        
        Returns:
            int: Unix timestamp when subscription expires (0 if never subscribed)
        
        Raises:
            ValueError: If wallet address is invalid
        """
        try:
            checksum_address = Web3.to_checksum_address(wallet_address)
            expiry = self.contract.functions.getExpiry(checksum_address).call()
            return expiry
        
        except ValueError as e:
            raise ValueError(f"Invalid wallet address: {wallet_address}") from e
    
    def get_remaining_time(self, wallet_address: str) -> int:
        """
        Get remaining subscription time in seconds.
        
        Args:
            wallet_address (str): Ethereum wallet address
        
        Returns:
            int: Seconds remaining (0 if expired)
        
        Raises:
            ValueError: If wallet address is invalid
        """
        try:
            checksum_address = Web3.to_checksum_address(wallet_address)
            remaining = self.contract.functions.getRemainingTime(checksum_address).call()
            return remaining
        
        except ValueError as e:
            raise ValueError(f"Invalid wallet address: {wallet_address}") from e
    
    def get_contract_stats(self) -> dict:
        """
        Get overall contract statistics.
        
        Returns:
            dict: Contract stats including price, duration, subscribers, revenue
        
        SAFE TO EXTEND:
        - Add more analytics data
        - Add historical data from events
        - Add growth metrics
        """
        try:
            stats = {
                'subscription_price_wei': self.contract.functions.SUBSCRIPTION_PRICE().call(),
                'subscription_price_eth': self.w3.from_wei(
                    self.contract.functions.SUBSCRIPTION_PRICE().call(), 
                    'ether'
                ),
                'subscription_duration_seconds': self.contract.functions.SUBSCRIPTION_DURATION().call(),
                'subscription_duration_days': self.contract.functions.SUBSCRIPTION_DURATION().call() / 86400,
                'total_subscribers': self.contract.functions.totalSubscribers().call(),
                'total_revenue_wei': self.contract.functions.totalRevenue().call(),
                'total_revenue_eth': self.w3.from_wei(
                    self.contract.functions.totalRevenue().call(), 
                    'ether'
                ),
                'contract_balance_wei': self.contract.functions.getBalance().call(),
                'contract_balance_eth': self.w3.from_wei(
                    self.contract.functions.getBalance().call(), 
                    'ether'
                ),
                'contract_address': self.contract_address,
            }
            return stats
        
        except Exception as e:
            raise Exception(f"Error fetching contract stats: {str(e)}")
    
    # ============ FUTURE EXTENSIONS (EXAMPLES) ============
    
    def get_subscription_events(self, wallet_address: str, from_block: int = 0):
        """
        EXAMPLE: Get subscription events for a wallet.
        
        This function shows how to query historical events.
        Useful for building subscription history, analytics, etc.
        
        NOTE: This is just an example. Implement when needed.
        """
        checksum_address = Web3.to_checksum_address(wallet_address)
        
        # Query Subscribed events
        subscribed_filter = self.contract.events.Subscribed.create_filter(
            from_block=from_block,
            argument_filters={'user': checksum_address}
        )
        
        # Query Cancelled events
        cancelled_filter = self.contract.events.Cancelled.create_filter(
            from_block=from_block,
            argument_filters={'user': checksum_address}
        )
        
        subscribed_events = subscribed_filter.get_all_entries()
        cancelled_events = cancelled_filter.get_all_entries()
        
        return {
            'subscribed': subscribed_events,
            'cancelled': cancelled_events
        }


# Initialize blockchain service (singleton pattern)
try:
    blockchain_service = BlockchainService()
except Exception as e:
    print(f"ERROR: Failed to initialize blockchain service: {e}")
    print("Make sure .env file is configured correctly.")
    blockchain_service = None