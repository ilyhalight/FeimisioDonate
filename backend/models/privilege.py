from pydantic import BaseModel


class Privilege(BaseModel):
    uid: int
    name: str
    price: int
    link: str
    duration: int
    discount: int
    short_description: str = None
    bg_color: str = '#c0c6ff'
    image: str = None
    disabled: int = 0