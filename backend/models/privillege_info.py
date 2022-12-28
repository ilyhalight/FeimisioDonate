from pydantic import BaseModel


class PrivillegeInfo(BaseModel):
    uid: int
    link: str
    name: str
    desc: str
    img_lin: str
    is_big_img: int|bool|None = 0
    img_reverse_side: int|bool|None = 0