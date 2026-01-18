"""
Configuration module for loading environment variables.

IMPORTANT: Never commit .env file to version control.
IMPORTANT: Never store private keys in this file or anywhere in code.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Application configuration loaded from environment variables.
    
    REQUIRED ENV VARS:
    - SEPOLIA_RPC_URL: RPC endpoint for Sepolia testnet
    - CONTRACT_ADDRESS: Address of deployed SubscriptionPayment contract
    
    OPTIONAL ENV VARS:
    - FLASK_ENV: development or production (default: development)
    - FLASK_DEBUG: True or False (default: True)
    """
    
    # Blockchain settings
    SEPOLIA_RPC_URL = os.getenv('SEPOLIA_RPC_URL')
    CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
    
    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    @staticmethod
    def validate():
        """
        Validate that all required configuration is present.
        Raises ValueError if any required config is missing.
        """
        if not Config.SEPOLIA_RPC_URL:
            raise ValueError("SEPOLIA_RPC_URL not set in .env file")
        
        if not Config.CONTRACT_ADDRESS:
            raise ValueError("CONTRACT_ADDRESS not set in .env file")
        
        if not Config.CONTRACT_ADDRESS.startswith('0x'):
            raise ValueError("CONTRACT_ADDRESS must be a valid Ethereum address")
        
        print("✓ Configuration validated successfully")