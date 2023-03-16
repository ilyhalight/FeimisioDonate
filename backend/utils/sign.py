import hmac
import json
from hashlib import md5, sha1, sha256


def sign_md5(shop_id: int, amount: int|float, secret: str, order_id: int|str):
    return md5(f'{shop_id}:{amount}:{secret}:{order_id}'.encode('utf-8')).hexdigest()

def sign_md5_upper(amount: int|float, order_id: str, secret: str):
    return md5(f'{amount}:{order_id}:{secret}'.upper().encode('utf-8')).hexdigest()

def sign_sha1(pay_id: str, secret2: str):
    return sha1(f'{pay_id}:{secret2}'.encode('utf-8')).hexdigest()

def sign_hmac_sha256(data: dict, secret: str, use_separators = False):
    if use_separators:
        json_str = json.dumps(data, separators=(',', ':')).encode()
    else:
        json_str = json.dumps(data).encode()
    return hmac.new(bytes(secret, 'UTF-8'), json_str, sha256).hexdigest()