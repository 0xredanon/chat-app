from cryptography.fernet import Fernet
import os
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Crypto:
    # Load key from environment
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        logging.error("ENCRYPTION_KEY environment variable is not set")
        raise ValueError("ENCRYPTION_KEY environment variable must be set")
    logging.debug(f"Using ENCRYPTION_KEY: {key}")
    try:
        cipher = Fernet(key)
    except Exception as e:
        logging.error(f"Invalid ENCRYPTION_KEY: {e}")
        raise ValueError(f"Invalid ENCRYPTION_KEY: {e}")

    @staticmethod
    def encrypt_message(message):
        try:
            return Crypto.cipher.encrypt(message.encode())
        except Exception as e:
            logging.error(f"Encryption error: {e}")
            raise

    @staticmethod
    def decrypt_message(encrypted):
        try:
            return Crypto.cipher.decrypt(encrypted).decode()
        except Exception as e:
            logging.error(f"Decryption error: {e}")
            return None