import config
from main import *
from base64 import urlsafe_b64decode, urlsafe_b64encode

# setup
from aiogram import types
from aiogram.types.message import ContentType

# this is for testing purposes only, we'll need to create a db table for this shit
referral_count = {}  # dictionary to keep track of the referral count
referred_users = []  # list to keep track of referred users

# helpers
def encode_payload(payload: str) -> str:
    """Encode payload with URL-safe base64url."""
    payload = str(payload)
    bytes_payload: bytes = urlsafe_b64encode(payload.encode())
    str_payload = bytes_payload.decode()
    return str_payload.replace("=", "")

def decode_payload(payload: str) -> str:
    """Decode payload with URL-safe base64url."""
    payload += "=" * (4 - len(payload) % 4)
    result: bytes = urlsafe_b64decode(payload)
    return result.decode()