from pydantic import BaseModel


class Promocodes(BaseModel):
    uid: int
    key: str
    author: str
    discount: int
    expires: int
    uses: int
    min_price: int
    max_price: int