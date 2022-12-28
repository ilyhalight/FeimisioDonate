from pydantic import BaseModel


class Privillege(BaseModel):
    uid: int
    name: str
    price: int
    link: str
    duration: int
    discount: int
    short_description: str = None
    description: str = None