import os
import time
import logging
from hashlib import sha256

logger = logging.getLogger('server')


async def generate_token(string: str, timestamp: int):
    token_pre = f'{string}{os.environ.get("FEIMISIO_TOKEN")}{timestamp}'
    token = sha256(token_pre.encode('utf-8')).hexdigest()
    return token

async def validate_token(token: str, string: str, timestamp: int):
    if int(time.time()) > timestamp + 30:
        logger.debug(f'Timestamp is older than current timestamp (30+ seconds ago | api: {int(time.time())}, request: {timestamp + 30} )')
        return False
    token_generated = await generate_token(string, timestamp)
    if token == token_generated:
        logger.debug('The token matches')
        return True
    return False