import os
import django
from web3 import Web3
from datetime import datetime
from django.utils import timezone
import time
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eth_tracker_project.settings")
django.setup()

# Import models after Django setup
from tracker.models import Deposit

# Set up logging to both console and file
log_file_path = os.path.join(os.path.dirname(__file__), "eth_tracker.log")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[
                        logging.FileHandler(log_file_path),  # Log to file
                        logging.StreamHandler()  # Log to console
                    ])

# Set up Web3 connection
API_KEY = os.getenv("ALCHEMY_API_KEY")
provider_url = f"https://eth-mainnet.alchemyapi.io/v2/{API_KEY}"
try:
    web3 = Web3(Web3.HTTPProvider(provider_url))
    if web3.isConnected():
        logging.info("Connected to the Ethereum network successfully.")
    else:
        logging.error("Failed to connect to the Ethereum network.")
except Exception as e:
    logging.error(f"Error initializing Web3 connection: {str(e)}")

# Beacon Deposit Contract address
BEACON_CONTRACT_ADDRESS = "0x00000000219ab540356cBB839Cbe05303d7705Fa"

# Process deposit transaction
def process_deposit(tx, block_number):
    try:
        receipt = web3.eth.get_transaction_receipt(tx.hash)
        if receipt.status == 1:  # Only successful transactions
            tx_hash = tx.hash.hex()
            sender = tx['from']
            amount = web3.from_wei(tx['value'], 'ether')  # Convert from Wei to Ether
            fee = web3.from_wei(tx['gasPrice'] * receipt['gasUsed'], 'ether')  # Transaction fee
            timestamp = datetime.utcfromtimestamp(web3.eth.get_block(block_number)['timestamp'])

            # Make timestamp timezone-aware
            timestamp = timezone.make_aware(timestamp, timezone.get_current_timezone())

            # Avoid duplicate entries by using Django's get_or_create
            deposit, created = Deposit.objects.get_or_create(
                tx_hash=tx_hash,
                defaults={
                    'block_number': block_number,
                    'sender': sender,
                    'amount': amount,
                    'fee': fee,
                    'pubkey': None,
                    'timestamp': timestamp
                }
            )

            if created:
                logging.info(f"Deposit saved: {tx_hash} from {sender}, amount: {amount} ETH")
            else:
                logging.info(f"Deposit already exists: {tx_hash}")
    except Exception as e:
        logging.error(f"Error processing deposit for tx {tx.hash.hex()}: {str(e)}")


# Track and monitor deposits to the Beacon Deposit Contract
def track_deposits():
    latest_block = web3.eth.block_number
    
    while True:
        try:
            current_block = web3.eth.block_number
            logging.info(f"Scanning blocks from {latest_block + 1} to {current_block}...")

            for block_number in range(latest_block + 1, current_block + 1):
                logging.info(f"Scanning block {block_number}...")
                block = web3.eth.get_block(block_number, full_transactions=True)

                for tx in block.transactions:
                    tx_hash = tx.hash.hex()
                    tx_to = tx.to
                    tx_value = web3.from_wei(tx.value, 'ether')

                    # Only log relevant transactions and valid deposits to the Beacon Deposit Contract
                    if tx_to and tx_to.lower() == BEACON_CONTRACT_ADDRESS.lower() and tx.value > 0:
                        logging.info(f"Valid deposit detected: {tx_hash}, value: {tx_value} ETH")
                        process_deposit(tx, block_number)
                    else:
                        # Optionally, avoid logging non-relevant transactions to reduce noise
                        pass

            latest_block = current_block
            time.sleep(15)  # Sleep before checking for new blocks
        except Exception as e:
            logging.error(f"Error during block scanning: {str(e)}")
            time.sleep(10)  # Delay before retrying


# Test function to verify database connection
def test_database():
    try:
        timestamp = timezone.now()
        deposit, created = Deposit.objects.get_or_create(
            tx_hash="0xabcdef1234567890abcdef1234567890abcdef12",
            defaults={
                'block_number': 123457,
                'sender': "0xabcdef1234567890abcdef1234567890abcdef12",
                'amount': 1.23,
                'fee': 0.01,
                'pubkey': None,
                'timestamp': timestamp
            }
        )
        if created:
            logging.info("Test deposit saved successfully!")
        else:
            logging.info("Test deposit already exists.")
    except Exception as e:
        logging.error(f"Error during database test: {str(e)}")


if __name__ == "__main__":
    # Call test function to verify the database works
    test_database()

    # Start the deposit tracker
    track_deposits()