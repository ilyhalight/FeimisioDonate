import os
import time
from hashlib import sha256


async def generate_token(string: str, timestamp: int):
    token_pre = f'{string}{os.environ.get("FEIMISIO_TOKEN")}{timestamp}'
    token = sha256(token_pre.encode('utf-8')).hexdigest()
    return token

async def validate_token(token: str, string: str, timestamp: int):
    if int(time.time()) > timestamp + 12:
        return False
    token_generated = await generate_token(string, timestamp)
    if token == token_generated:
        return True
    return False