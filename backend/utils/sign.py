from hashlib import md5


def sign(shop_id: int, amount: int|float, secret: str, order_id: int|str):
    return md5(f'{shop_id}:{amount}:{secret}:{order_id}'.encode('utf-8')).hexdigest()