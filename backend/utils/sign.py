from hashlib import md5, sha1


def sign_md5(shop_id: int, amount: int|float, secret: str, order_id: int|str):
    return md5(f'{shop_id}:{amount}:{secret}:{order_id}'.encode('utf-8')).hexdigest()

# Crystalapi v1
# def sign_sha1(pay_id: str, currency: str, secret2: str):
#     return sha1(f'{pay_id}:{currency}:{secret2}'.encode('utf-8')).hexdigest()

def sign_sha1(pay_id: str, secret2: str):
    return sha1(f'{pay_id}:{secret2}'.encode('utf-8')).hexdigest()